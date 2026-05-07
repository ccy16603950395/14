import torch.nn as nn


class LightPINN(nn.Module):
    """PINN v1: outputs [u_mm, v_mm, w_mm, mises_pa_norm]."""

    def __init__(self, in_dim: int, out_dim: int = 4):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, 256),
            nn.SiLU(),
            nn.Linear(256, 256),
            nn.SiLU(),
            nn.Linear(256, 256),
            nn.SiLU(),
            nn.Linear(256, 128),
            nn.SiLU(),
            nn.Linear(128, out_dim),
        )

    def forward(self, x):
        return self.net(x)
