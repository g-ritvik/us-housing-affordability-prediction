import joblib
import numpy as np
import pandas as pd

from src.utils.model_utils import (
    PROJECT_ROOT,
    SELECTED_FEATURES
)

from src.utils.display import print_banner, print_table, console, Panel

DATA_PATH = PROJECT_ROOT / "data" / "clean"
TEST_DATA = DATA_PATH / "test_clean.csv"

OUTPUT_PATH = PROJECT_ROOT / "reports" / "test_predictions.csv"

ARTIFACT_PATH = PROJECT_ROOT / "artifacts"
RIDGE_JOBLIB = ARTIFACT_PATH / "ridge_housing_affordability.joblib"

NUMERIC_FEATURES = [
    "OwnerPercent",
    "MedianHomeLengthofResidence",
    "AvgNumberofChildren",
    "AvgHouseholdSize",
    "AvgGenerationsinHousehold",
    "YoungAdultinHouseholdPercent",
    "SeniorAdultinHouseholdPercent"
]

FEATURE_DETAILS = {
    "Month": (
        "Observation month and year",
        "Date (MM/DD/YYYY)",
        "e.g., 5/1/2026"
    ),
    "State": (
        "Two-letter state abbreviation",
        "Text",
        "e.g., CA"
    ),
    "City": (
        "Primary city associated with the ZIP code",
        "Text",
        "e.g., Sacramento"
    ),
    "Metro": (
        "Associated metropolitan area",
        "Text",
        "e.g., Sacramento-Roseville-Folsom"
    ),
    "OwnerPercent": (
        "Percentage of households classified as homeowners",
        "Percentage (0–100)",
        "e.g., 65.5"
    ),
    "MedianHomeLengthofResidence": (
        "Median number of years households have lived at their current residence",
        "Years (decimal allowed)",
        "e.g., 8.5"
    ),
    "AvgNumberofChildren": (
        "Average number of children per household",
        "Children per household (decimal allowed)",
        "e.g., 0.8"
    ),
    "AvgHouseholdSize": (
        "Average number of people living in each household",
        "People per household (decimal allowed)",
        "e.g., 2.6"
    ),
    "AvgGenerationsinHousehold": (
        "Average number of generations living in each household",
        "Generations per household (decimal allowed)",
        "e.g., 1.2"
    ),
    "YoungAdultinHouseholdPercent": (
        "Percentage of households with at least one young adult",
        "Percentage (0–100)",
        "e.g., 24.5"
    ),
    "SeniorAdultinHouseholdPercent": (
        "Percentage of households with at least one senior adult",
        "Percentage (0–100)",
        "e.g., 32.0"
    )
}


def load_model():
    return joblib.load(RIDGE_JOBLIB)


def predict_kaggle_test(model):
    df = pd.read_csv(TEST_DATA, dtype={"Zip": str})
    X_test = df[SELECTED_FEATURES].copy()

    raw_predictions = model.predict(X_test)
    clipped_count = ((raw_predictions < 0) | (raw_predictions > 100)).sum()
    predictions = np.clip(raw_predictions, 0, 100)

    predictions_df = pd.DataFrame(
        {
            "Zip": df["Zip"],
            "State": df["State"],
            "AffordabilityPercentageTrue": predictions
        }
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    predictions_df.to_csv(OUTPUT_PATH, index=False)

    print_banner(
        "US Housing Affordability — Kaggle Test Predictions Completed",
        style="green",
    )

    print_table(
        "Prediction Summary",
        ["Property", "Value"],
        [
            ("Test Dataset", TEST_DATA.name),
            ("Records Predicted", f"{len(predictions_df):,}"),
            ("Predictions Clipped", f"{clipped_count:,}"),
            ("Clipping Percentage", f"{clipped_count / len(predictions) * 100:.2f}%"),
            ("Predictions Saved To", str(OUTPUT_PATH)),
        ],
    )


def predict_custom(model):
    values = {}

    print_banner(
        "US Housing Affordability — Custom Prediction",
        style="cyan",
    )

    for feature in SELECTED_FEATURES:
        description, input_format, example = FEATURE_DETAILS[feature]

        print()
        print(f"{feature}: {description}")
        print(f"Expected format: {input_format}")

        while True:
            value = input(f"Enter value ({example}): ").strip()

            if not value:
                print("A value is required.")
                continue

            if feature in NUMERIC_FEATURES:
                try:
                    values[feature] = float(value)
                    break
                except ValueError:
                    print("Please enter a valid numeric value.")
            else:
                values[feature] = value
                break

    X_custom = pd.DataFrame(
        [values],
        columns=SELECTED_FEATURES
    )

    raw_prediction = model.predict(X_custom)[0]
    prediction = np.clip(raw_prediction, 0, 100)

    print_banner(
        "US Housing Affordability — Custom Prediction Completed",
        style="green",
    )

    print_table(
        "Prediction Result",
        ["Property", "Value"],
        [
            ("Original Prediction", f"{raw_prediction:.2f}%"),
            ("Final Prediction", f"{prediction:.2f}%"),
            ("Prediction Clipped", "Yes" if raw_prediction != prediction else "No"),
        ],
    )


def main():
    print_banner(
        "US Housing Affordability — Prediction",
        style="cyan",
    )

    console.print(
        Panel(
            "[bold yellow]Important Notice[/bold yellow]\n\n"
            "The model predicts the percentage of households whose housing "
            "costs are at or below 30% of their household income. "
            "Predictions represent groups of households at the ZIP-code level "
            "and are intended for regional analysis, not individual household "
            "or property assessments.",
            border_style="yellow",
            padding=(1, 2)
        )
    )

    print_table(
        "Prediction Modes",
        ["Option", "Description"],
        [
            ("1", "Predict using Kaggle test dataset"),
            ("2", "Make a custom prediction")
        ],
    )

    choice = input("Select an option (1 or 2): ").strip()

    if choice not in {"1", "2"}:
        print("Invalid option.")
        return

    model = load_model()

    if choice == "1":
        predict_kaggle_test(model)
    else:
        predict_custom(model)


if __name__ == "__main__":
    main()
