from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# ============================================================
# 1. SHARED CONFIGURATION
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]
TRAIN_PATH = PROJECT_ROOT / "data" / "clean" / "train_clean.csv"

TARGET = "AffordabilityPercentageTrue"
RIDGE_ALPHA = 5.0
RANDOM_STATE = 42
N_SPLITS = 5

SELECTED_FEATURES = [
    "Month", "State", "City", "Metro", "OwnerPercent",
    "MedianHomeLengthofResidence", "AvgNumberofChildren", "AvgHouseholdSize",
    "AvgGenerationsinHousehold", "YoungAdultinHouseholdPercent",
    "SeniorAdultinHouseholdPercent",
]

CVSplits = list[tuple[np.ndarray, np.ndarray]]

# ============================================================
# 2. DATA LOADING AND PREPARATION
# ============================================================
def load_data(path: Path = TRAIN_PATH) -> pd.DataFrame:
    """Load the cleaned training data and verify required columns exist."""
    df = pd.read_csv(path, dtype={"Zip": str})
    missing = [c for c in [TARGET, "Zip", *SELECTED_FEATURES] if c not in df.columns]
    if missing:
        raise ValueError(f"{path} data is missing columns: {missing}")
    return df


def split_feature_types(X: pd.DataFrame) -> tuple[list[str], list[str]]:
    """Return (numeric columns, categorical columns) of the predictor frame."""
    numeric = X.select_dtypes(include=np.number).columns.tolist()
    categorical = X.select_dtypes(exclude=np.number).columns.tolist()
    return numeric, categorical


def prepare_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """Split the dataset into predictors (X), target (y), and ZIP groups."""
    return df[SELECTED_FEATURES].copy(), df[TARGET], df["Zip"]


# ============================================================
# 3. PIPELINE AND CROSS-VALIDATION
# ============================================================
def create_pipeline(X: pd.DataFrame, model: Any) -> Pipeline:
    """Build preprocessing + model pipeline; column types are inferred from X."""
    numeric, categorical = split_feature_types(X)
    preprocessor = ColumnTransformer([
        ("numerical", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]), numeric),
        ("categorical", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]), categorical),
    ])
    return Pipeline([("preprocessor", preprocessor), ("model", clone(model))])


def create_cv_splits(X: pd.DataFrame, y: pd.Series, groups: pd.Series) -> CVSplits:
    """Create target-stratified, ZIP-grouped CV splits."""
    y_bins = pd.qcut(y, q=10, labels=False, duplicates="drop")
    splitter = StratifiedGroupKFold(
        n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE
    )
    return list(splitter.split(X, y_bins, groups=groups))