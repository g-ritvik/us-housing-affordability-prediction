from typing import Any

import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import root_mean_squared_error

from src.utils.model_utils import (
    PROJECT_ROOT,
    RIDGE_ALPHA,
    SELECTED_FEATURES,
    TARGET,
    CVSplits,
    create_cv_splits,
    create_pipeline,
    load_data,
    prepare_features,
    split_feature_types,
)

from src.utils.display import (
    print_banner,
    print_dataframe,
    print_table,
)

# ============================================================
# 1. EVALUATION CONFIGURATION
# ============================================================
LASSO_ALPHA = 0.01
MONTH_MAY, MONTH_JUNE = "5/1/2026", "6/1/2026"

SeenData = tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]

# ============================================================
# 2. VALIDATION AND SEEN-ZIP DATA
# ============================================================
def validate_group_splits(cv_splits: CVSplits, groups: pd.Series) -> None:
    """Print per-fold ZIP counts and raise if any ZIP appears in both train and validation."""
    rows, leaked = [], []
    for fold, (train_idx, val_idx) in enumerate(cv_splits, start=1):
        train_zips, val_zips = groups.iloc[train_idx], groups.iloc[val_idx]
        overlap = len(set(train_zips) & set(val_zips))
        rows.append((fold, f"{train_zips.nunique():,}", f"{val_zips.nunique():,}", overlap))
        if overlap:
            leaked.append(fold)

    print_table(
        f"Group CV Validation ({len(cv_splits)} folds)",
        ["Fold", "Train ZIPs", "Validation ZIPs", "Overlap"],
        rows,
        first_justify="center",
    )
    if leaked:
        raise ValueError(f"ZIP leakage detected in fold(s): {leaked}")


def prepare_seen_zip_data(train: pd.DataFrame) -> SeenData:
    """Split May (train) and June (validation) observations; ZIP sets must match."""
    may, june = train["Month"].eq(MONTH_MAY), train["Month"].eq(MONTH_JUNE)

    may_zips, june_zips = set(train.loc[may, "Zip"]), set(train.loc[june, "Zip"])
    if may_zips != june_zips:
        raise ValueError("May and June ZIP codes do not match.")

    print_table(
        "Seen ZIP Data",
        ["Property", "Value"],
        [
            ("May Records", f"{may.sum():,}"),
            ("June Records", f"{june.sum():,}"),
            ("Matching ZIPs", f"{len(may_zips):,}"),
        ],
    )
    return (
        train.loc[may, SELECTED_FEATURES].copy(), train.loc[may, TARGET],
        train.loc[june, SELECTED_FEATURES].copy(), train.loc[june, TARGET],
    )

# ============================================================
# 3. MODEL DEFINITIONS AND EVALUATION
# ============================================================
def create_models() -> dict[str, Any]:
    """Define the models to compare."""
    return {
        "Dummy": DummyRegressor(strategy="mean"),
        "Linear Regression": LinearRegression(),
        "Ridge": Ridge(alpha=RIDGE_ALPHA),
        "Lasso": Lasso(alpha=LASSO_ALPHA, max_iter=10000),
    }

def evaluate_new_zip(
    X: pd.DataFrame, y: pd.Series, cv_splits: CVSplits, model: Any
) -> tuple[float, float]:
    """Grouped CV on unseen ZIPs; returns (mean, std) of clipped RMSE."""
    scores = []
    for train_idx, val_idx in cv_splits:
        pipeline = create_pipeline(X, model).fit(X.iloc[train_idx], y.iloc[train_idx])
        pred = np.clip(pipeline.predict(X.iloc[val_idx]), 0, 100)
        scores.append(root_mean_squared_error(y.iloc[val_idx], pred))
    return float(np.mean(scores)), float(np.std(scores))

def evaluate_seen_zip(seen_data: SeenData, model: Any) -> float:
    """Train on May, predict June for known ZIPs; returns clipped RMSE."""
    X_may, y_may, X_june, y_june = seen_data
    pipeline = create_pipeline(X_may, model).fit(X_may, y_may)
    pred = np.clip(pipeline.predict(X_june), 0, 100)
    return float(root_mean_squared_error(y_june, pred))

def calculate_weighted_rmse(new_zip_rmse: float, seen_zip_rmse: float) -> float:
    """Competition-weighted RMSE: 80% new ZIP, 20% seen ZIP."""
    return 0.80 * new_zip_rmse + 0.20 * seen_zip_rmse

def compare_models(
    models: dict[str, Any], X: pd.DataFrame, y: pd.Series,
    cv_splits: CVSplits, seen_data: SeenData,
) -> pd.DataFrame:
    """Evaluate every model and return results sorted by weighted RMSE."""
    results = []
    for name, model in models.items():
        new_rmse, new_std = evaluate_new_zip(X, y, cv_splits, model)
        seen_rmse = evaluate_seen_zip(seen_data, model)
        results.append({
        "Model": name,
        "Configuration": (
            f"alpha = {RIDGE_ALPHA}" if name == "Ridge"
            else f"alpha = {LASSO_ALPHA}" if name == "Lasso"
            else "—"
        ),
        "New ZIP RMSE": new_rmse,
        "New ZIP Std": new_std,
        "Seen ZIP RMSE": seen_rmse,
        "Weighted RMSE": calculate_weighted_rmse(new_rmse, seen_rmse),
    })
    return pd.DataFrame(results).sort_values("Weighted RMSE").reset_index(drop=True)

# ============================================================
# 4. MAIN
# ============================================================
def main() -> None:
    """Load data, validate splits, compare models, and print the results."""
    print_banner("[bold cyan]Housing Affordability — Model Comparison[/bold cyan]")

    train = load_data()
    X, y, groups = prepare_features(train)
    numeric, categorical = split_feature_types(X)

    print_table(
        "Feature Types",
        ["Type", "Features"],
        [("Numeric", ", ".join(numeric)), ("Categorical", ", ".join(categorical))],
    )

    cv_splits = create_cv_splits(X, y, groups)
    validate_group_splits(cv_splits, groups)
    seen_data = prepare_seen_zip_data(train)

    results = compare_models(create_models(), X, y, cv_splits, seen_data)

    print_dataframe(results, "Model Comparison")

    output_path = load_data.__globals__["PROJECT_ROOT"] / "reports" / "model_comparison.csv"
    results.to_csv(output_path, index=False)

    print_banner(f"Model comparison exported to:\n{output_path}", style="green")


if __name__ == "__main__":
    main()
