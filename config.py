from pathlib import Path

# Windows paths (keep raw string style compatible)
BASE_DIR = Path(r"E:\数值模拟")
SURFACE_DIR = BASE_DIR / "训练数据"
INTERNAL_DIR = BASE_DIR / "完全数据"
CASE_INFO_PATH = BASE_DIR / "case_info.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
PRED_DIR = OUTPUT_DIR / "predictions"
FIG_DIR = OUTPUT_DIR / "figures"

# case split (case-level only)
TEST_CASES = ["case46", "case47", "case48"]
VAL_CASES = ["case37", "case38", "case39"]
ALL_CASES = [
    "case1", "case2", "case3", "case10", "case11", "case12",
    "case19", "case20", "case21", "case28", "case29", "case30",
    "case37", "case38", "case39", "case46", "case47", "case48",
]
TRAIN_CASES = [c for c in ALL_CASES if c not in TEST_CASES + VAL_CASES]

# sampling & training
RANDOM_SEED = 42
SAMPLE_POINTS_PER_CASE = 20000
EPOCHS = 300
BATCH_SIZE = 8192
LR = 1e-3
WEIGHT_DECAY = 1e-5

# target column
TARGET_COL = "solid_mises_n_m2"

# case_info column mapping (edit as needed)
CASE_INFO_COLUMN_MAPPING = {
    "case": ["case", "案例", "工况", "case_id"],
    "angle": ["angle", "弱化带角度", "倾角"],
    "width": ["width", "弱化带宽度", "宽度"],
    "weaken_E": ["weaken_E", "弱化带弹性模量", "弱化带E"],
    "confining_pressure": ["confining_pressure", "围压"],
    "axial_pressure": ["axial_pressure", "轴压"],
    "weaken_nu": ["weaken_nu", "弱化带泊松比"],
    "density": ["density", "密度"],
    "rock_E": ["rock_E", "岩石弹性模量", "岩石E"],
    "rock_nu": ["rock_nu", "岩石泊松比"],
}
GLOBAL_FEATURES = [
    "angle", "width", "weaken_E", "confining_pressure", "axial_pressure",
    "weaken_nu", "density", "rock_E", "rock_nu",
]

# PINN v1 loss weights
LAMBDA_DATA = 1.0
LAMBDA_VM_CONSISTENCY = 0.2
LAMBDA_EQUILIBRIUM = 1e-10
