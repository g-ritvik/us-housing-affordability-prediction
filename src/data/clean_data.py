from pathlib import Path

import pandas as pd

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


console = Console()

ROOT_PATH = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = ROOT_PATH / "data" / "raw"
CLEAN_DATA_PATH = ROOT_PATH / "data" / "clean"

TRAIN_PATH = RAW_DATA_PATH / "train.csv"
TEST_PATH = RAW_DATA_PATH / "test.csv"


def clean_data(df, state_rent_medians):
    """
    Clean housing affordability data.

    Cleaning steps:
    1. Standardize ZIP codes.
    2. Recover missing City values for ZIP 33194.
    3. Replace missing Metro values with 'Unknown'.
    4. Impute RentIndex using the same ZIP's other month.
    5. Use training-state medians for remaining RentIndex values.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset to clean.
    state_rent_medians : pandas.Series
        State-level RentIndex medians calculated from
        observed training data.

    Returns
    -------
    pandas.DataFrame
        Cleaned dataset.
    """

    df_clean = df.copy()

    # Standardize ZIP codes
    df_clean["Zip"] = (
        df_clean["Zip"]
        .astype(str)
        .str.zfill(5)
    )

    # Recover missing City values
    city_missing = (
        df_clean["City"].isna()
        & (df_clean["Zip"] == "33194")
    )
    df_clean.loc[city_missing, "City"] = "Miami"

    # Handle missing Metro values
    df_clean["Metro"] = df_clean["Metro"].fillna("Unknown")

    # Impute RentIndex using ZIP-level medians
    zip_rent_medians = (
        df_clean.groupby("Zip")["RentIndex"].transform("median")
    )
    df_clean["RentIndex"] = (
        df_clean["RentIndex"].fillna(zip_rent_medians)
    )

    # Impute remaining RentIndex values using training-state medians
    df_clean["RentIndex"] = (
        df_clean["RentIndex"].fillna(
            df_clean["State"].map(state_rent_medians)
        )
    )

    return df_clean


def validate_dataset(name, dataset):
    """Validate a cleaned dataset and display its summary."""

    exact_duplicates = dataset.duplicated().sum()
    zip_month_duplicates = dataset.duplicated(
        ["Zip", "Month"]
    ).sum()
    missing_count = dataset.isna().sum().sum()

    invalid_zip_count = (
        ~dataset["Zip"].str.len().eq(5)
    ).sum()

    table = Table(
        title=f"{name} Dataset Validation",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )

    table.add_column("Validation Check")
    table.add_column("Result", justify="right")
    table.add_column("Status", justify="center")

    checks = [
        ("Dataset shape", f"{dataset.shape[0]:,} × {dataset.shape[1]:,}", "INFO"),
        ("Missing values", f"{missing_count:,}", "PASS" if missing_count == 0 else "FAIL"),
        ("Exact duplicates", f"{exact_duplicates:,}", "PASS" if exact_duplicates == 0 else "FAIL"),
        ("Duplicate ZIP-Month pairs", f"{zip_month_duplicates:,}", "PASS" if zip_month_duplicates == 0 else "FAIL"),
        ("Unique ZIP codes", f"{dataset['Zip'].nunique():,}", "INFO"),
        ("Invalid ZIP lengths", f"{invalid_zip_count:,}", "PASS" if invalid_zip_count == 0 else "FAIL"),
    ]

    for check, result, status in checks:
        style = {
            "PASS": "green",
            "FAIL": "bold red",
            "INFO": "cyan"
        }[status]

        table.add_row(
            check,
            result,
            f"[{style}]{status}[/{style}]"
        )

    console.print(table)

    if missing_count > 0:
        raise ValueError(f"{name} dataset contains missing values.")

    if exact_duplicates > 0:
        raise ValueError(f"{name} dataset contains exact duplicate records.")

    if zip_month_duplicates > 0:
        raise ValueError(f"{name} dataset contains duplicate ZIP-Month pairs.")

    if invalid_zip_count > 0:
        raise ValueError(f"{name} dataset contains incorrectly formatted ZIP codes.")


def main():
    """Load, clean, validate, and save the datasets."""

    console.print(
        Panel(
            "[bold cyan]U.S. Housing Affordability[/bold cyan]\n"
            "Data Cleaning & Validation Pipeline",
            border_style="cyan"
        )
    )

    CLEAN_DATA_PATH.mkdir(parents=True, exist_ok=True)

    # Load raw datasets
    console.print("\n[bold]Loading raw datasets...[/bold]")

    train = pd.read_csv(TRAIN_PATH)
    test = pd.read_csv(TEST_PATH)

    console.print(
        f"[green]✓[/green] Training dataset loaded: "
        f"{train.shape[0]:,} rows × {train.shape[1]} columns"
    )
    console.print(
        f"[green]✓[/green] Test dataset loaded: "
        f"{test.shape[0]:,} rows × {test.shape[1]} columns"
    )

    # Calculate state medians from original training observations
    console.print("\n[bold]Preparing imputation values...[/bold]")

    state_rent_medians = (
        train.groupby("State")["RentIndex"].median()
    )

    console.print(
        f"[green]✓[/green] Calculated RentIndex medians for "
        f"{len(state_rent_medians)} states using training data."
    )

    # Clean datasets
    console.print("\n[bold]Cleaning datasets...[/bold]")

    train_clean = clean_data(train, state_rent_medians)
    test_clean = clean_data(test, state_rent_medians)

    console.print("[green]✓[/green] Training dataset cleaned.")
    console.print("[green]✓[/green] Test dataset cleaned.")

    # Validate datasets
    console.print("\n[bold]Running validation checks...[/bold]")

    validate_dataset("Training", train_clean)
    validate_dataset("Test", test_clean)

    # Save cleaned datasets
    console.print("\n[bold]Saving cleaned datasets...[/bold]")

    train_output = CLEAN_DATA_PATH / "train_clean.csv"
    test_output = CLEAN_DATA_PATH / "test_clean.csv"

    train_clean.to_csv(train_output, index=False)
    test_clean.to_csv(test_output, index=False)

    console.print(
        Panel(
            "[bold green]Cleaning completed successfully![/bold green]\n\n"
            f"Training: [cyan]{train_output}[/cyan]\n"
            f"Test: [cyan]{test_output}[/cyan]",
            title="Pipeline Complete",
            border_style="green"
        )
    )


if __name__ == "__main__":
    main()