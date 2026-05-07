import random

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader

from config import *
from data_utils import TabularTensorDataset, build_case_dataframe, compute_normalizer, resolve_case_info, sample_case_points
from model import LightPINN
from plot_utils import plot_loss_curve


def set_seed(seed=RANDOM_SEED):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def grad_of(y, x):
    return torch.autograd.grad(y, x, grad_outputs=torch.ones_like(y), create_graph=True, retain_graph=True)[0]


def physics_losses(xb, pred, feature_names, x_mean, x_std, y_mean, y_std):
    idx = {n: i for i, n in enumerate(feature_names)}
    xi, yi, zi = idx["x"], idx["y"], idx["z"]
    e_i, nu_i = idx["rock_E"], idx["rock_nu"]

    u = pred[:, 0:1]
    v = pred[:, 1:2]
    w = pred[:, 2:3]
    mises_pred_pa = pred[:, 3:4] * y_std + y_mean

    du = grad_of(u, xb)
    dv = grad_of(v, xb)
    dw = grad_of(w, xb)

    s_x, s_y, s_z = x_std[xi], x_std[yi], x_std[zi]
    du_dx, du_dy, du_dz = du[:, xi:xi+1] / s_x, du[:, yi:yi+1] / s_y, du[:, zi:zi+1] / s_z
    dv_dx, dv_dy, dv_dz = dv[:, xi:xi+1] / s_x, dv[:, yi:yi+1] / s_y, dv[:, zi:zi+1] / s_z
    dw_dx, dw_dy, dw_dz = dw[:, xi:xi+1] / s_x, dw[:, yi:yi+1] / s_y, dw[:, zi:zi+1] / s_z

    exx, eyy, ezz = du_dx, dv_dy, dw_dz
    exy = 0.5 * (du_dy + dv_dx)
    exz = 0.5 * (du_dz + dw_dx)
    eyz = 0.5 * (dv_dz + dw_dy)

    E = xb[:, e_i:e_i+1] * x_std[e_i] + x_mean[e_i]
    nu = xb[:, nu_i:nu_i+1] * x_std[nu_i] + x_mean[nu_i]
    E = torch.clamp(E, min=1e6)
    nu = torch.clamp(nu, min=1e-3, max=0.49)

    lam = E * nu / ((1 + nu) * (1 - 2 * nu))
    mu = E / (2 * (1 + nu))
    tr = exx + eyy + ezz

    sxx = lam * tr + 2 * mu * exx
    syy = lam * tr + 2 * mu * eyy
    szz = lam * tr + 2 * mu * ezz
    sxy = 2 * mu * exy
    sxz = 2 * mu * exz
    syz = 2 * mu * eyz

    mises_from_sigma = torch.sqrt(0.5 * ((sxx - syy) ** 2 + (syy - szz) ** 2 + (szz - sxx) ** 2) + 3 * (sxy ** 2 + sxz ** 2 + syz ** 2) + 1e-12)

    vm_cons = torch.mean((mises_pred_pa - mises_from_sigma) ** 2)

    dsxx = grad_of(sxx, xb); dsyy = grad_of(syy, xb); dszz = grad_of(szz, xb)
    dsxy = grad_of(sxy, xb); dsxz = grad_of(sxz, xb); dsyz = grad_of(syz, xb)
    rx = dsxx[:, xi:xi+1] / s_x + dsxy[:, yi:yi+1] / s_y + dsxz[:, zi:zi+1] / s_z
    ry = dsxy[:, xi:xi+1] / s_x + dsyy[:, yi:yi+1] / s_y + dsyz[:, zi:zi+1] / s_z
    rz = dsxz[:, xi:xi+1] / s_x + dsyz[:, yi:yi+1] / s_y + dszz[:, zi:zi+1] / s_z
    eq = torch.mean(rx ** 2 + ry ** 2 + rz ** 2)

    return vm_cons, eq


def main():
    set_seed(); OUTPUT_DIR.mkdir(parents=True, exist_ok=True); PRED_DIR.mkdir(parents=True, exist_ok=True); FIG_DIR.mkdir(parents=True, exist_ok=True)
    case_info = resolve_case_info(CASE_INFO_PATH); ci = {r["case"]: r for _, r in case_info.iterrows()}

    def build_split(cases):
        return pd.concat([sample_case_points(build_case_dataframe(c, ci[c]), SAMPLE_POINTS_PER_CASE, RANDOM_SEED) for c in cases], ignore_index=True)

    train_df, val_df = build_split(TRAIN_CASES), build_split(VAL_CASES)
    feature_names = [c for c in train_df.columns if c not in ["case", TARGET_COL]]
    x_train, y_train = train_df[feature_names].to_numpy(float), train_df[TARGET_COL].to_numpy(float)
    x_val, y_val = val_df[feature_names].to_numpy(float), val_df[TARGET_COL].to_numpy(float)

    x_mean, x_std, y_mean, y_std = compute_normalizer(x_train, y_train)
    x_train_n, x_val_n = (x_train - x_mean) / x_std, (x_val - x_mean) / x_std
    y_train_n, y_val_n = (y_train - y_mean) / y_std, (y_val - y_mean) / y_std

    train_loader = DataLoader(TabularTensorDataset(x_train_n, y_train_n), batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(TabularTensorDataset(x_val_n, y_val_n), batch_size=BATCH_SIZE, shuffle=False)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = LightPINN(len(feature_names), out_dim=4).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY)

    x_mean_t = torch.tensor(x_mean, dtype=torch.float32, device=device)
    x_std_t = torch.tensor(x_std, dtype=torch.float32, device=device)
    y_mean_t = torch.tensor(y_mean, dtype=torch.float32, device=device)
    y_std_t = torch.tensor(y_std, dtype=torch.float32, device=device)

    best_val = float("inf"); logs = []
    for ep in range(1, EPOCHS + 1):
        model.train(); tl = 0.0
        for xb, yb in train_loader:
            xb, yb = xb.to(device), yb.to(device)
            xb.requires_grad_(True)
            opt.zero_grad()
            pred = model(xb)
            data_loss = torch.mean((pred[:, 3:4] - yb) ** 2)
            vm_cons, eq = physics_losses(xb, pred, feature_names, x_mean_t, x_std_t, y_mean_t, y_std_t)
            loss = LAMBDA_DATA * data_loss + LAMBDA_VM_CONSISTENCY * vm_cons + LAMBDA_EQUILIBRIUM * eq
            loss.backward(); opt.step(); tl += loss.item() * len(xb)
        tl /= len(train_loader.dataset)

        model.eval(); vl = 0.0
        with torch.no_grad():
            for xb, yb in val_loader:
                xb, yb = xb.to(device), yb.to(device)
                vl += torch.mean((model(xb)[:, 3:4] - yb) ** 2).item() * len(xb)
        vl /= len(val_loader.dataset)

        logs.append({"epoch": ep, "train_loss": tl, "val_loss": vl}); print(ep, tl, vl)
        if vl < best_val:
            best_val = vl
            torch.save({"model_state_dict": model.state_dict(), "normalizer": {"x_mean": x_mean, "x_std": x_std, "y_mean": y_mean, "y_std": y_std}, "feature_names": feature_names, "train_cases": TRAIN_CASES, "val_cases": VAL_CASES, "test_cases": TEST_CASES, "config": {"epochs": EPOCHS, "batch_size": BATCH_SIZE, "lr": LR, "weight_decay": WEIGHT_DECAY, "sample_points_per_case": SAMPLE_POINTS_PER_CASE, "lambda_data": LAMBDA_DATA, "lambda_vm_consistency": LAMBDA_VM_CONSISTENCY, "lambda_equilibrium": LAMBDA_EQUILIBRIUM}}, OUTPUT_DIR / "best_model.pt")

    log_df = pd.DataFrame(logs); log_df.to_csv(OUTPUT_DIR / "train_log.csv", index=False); plot_loss_curve(log_df, OUTPUT_DIR / "loss_curve.png")


if __name__ == "__main__":
    main()
