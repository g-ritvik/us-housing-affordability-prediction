import joblib
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline

from src.utils.model_utils import (
    PROJECT_ROOT,
    RIDGE_ALPHA,
    SELECTED_FEATURES,
    create_pipeline,
    load_data,
    prepare_features,
)

from src.utils.display import (
    print_banner,
    print_table,
)

# ============================================================
# 1. CONFIGURATION
# ============================================================
MODEL_DIR = PROJECT_ROOT / "artifacts"
MODEL_PATH = MODEL_DIR / "ridge_housing_affordability.joblib"


# ============================================================
# 2. TRAINING
# ============================================================
def train_model(train: pd.DataFrame) -> Pipeline:
    """Fit the final Ridge pipeline on all training records."""
    X, y, _ = prepare_features(train)
    return create_pipeline(X, Ridge(alpha=RIDGE_ALPHA)).fit(X, y)


# ============================================================
# 3. MODEL EXPORT (JOBLIB)
# ============================================================
def save_model(model: Pipeline) -> None:
    """Save the fitted pipeline as a Joblib artifact."""
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)


def load_model() -> Pipeline:
    """Load the saved Joblib pipeline."""
    return joblib.load(MODEL_PATH)


# ============================================================
# 4. MAIN
# ============================================================
def main() -> None:
    """Train the final model, export it, and print a summary."""
    print_banner(
        "[bold cyan]Housing Affordability — Final Model Training[/bold cyan]\n"
        f"Ridge Regression | {len(SELECTED_FEATURES)} Features | Alpha = {RIDGE_ALPHA}"
    )

    train = load_data()
    save_model(train_model(train))

    print_table(
        "Final Training Summary",
        ["Property", "Value"],
        [
            ("Training Records", f"{len(train):,}"),
            ("Selected Features", len(SELECTED_FEATURES)),
            ("Model", "Ridge Regression"),
            ("Ridge Alpha", RIDGE_ALPHA),
        ],
    )
    print_banner(
        f"[bold green]Model saved:[/bold green]\n{MODEL_PATH}",
        style="green",
        title="Export Completed",
    )


if __name__ == "__main__":
    main()