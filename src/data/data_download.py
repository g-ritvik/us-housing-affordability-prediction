from pathlib import Path

import kagglehub

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


console = Console()

PROJECT_ROOT = Path(__file__).resolve().parents[2]

COMPETITION = "predicting-housing-affordability-in-the-u-s"
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

EXPECTED_FILES = [
    "sample_submission.csv",
    "test.csv",
    "train.csv"
]


def download_data() -> Path:
    """Download competition data if the expected files are not already present."""

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    console.print(
        Panel(
            "[bold cyan]U.S. Housing Affordability[/bold cyan]\n"
            "Kaggle Data Download",
            border_style="cyan"
        )
    )

    # Check whether all expected files already exist
    missing_files = [
        file for file in EXPECTED_FILES
        if not (RAW_DATA_DIR / file).is_file()
    ]

    if not missing_files:
        console.print(
            "[green]✓[/green] All competition files already exist."
        )
        display_file_status()
        return RAW_DATA_DIR

    # Authenticate with Kaggle
    console.print("\n[bold]Authenticating with Kaggle...[/bold]")
    kagglehub.login()

    # Download competition data
    console.print(
        f"\n[bold]Downloading competition:[/bold] {COMPETITION}"
    )

    kagglehub.competition_download(
        COMPETITION,
        output_dir=str(RAW_DATA_DIR),
    )

    # Verify expected files after download
    missing_files = [
        file for file in EXPECTED_FILES
        if not (RAW_DATA_DIR / file).is_file()
    ]

    if missing_files:
        raise FileNotFoundError(
            f"Download incomplete. Missing files: {missing_files}"
        )

    console.print(
        "\n[bold green]✓ Download completed successfully![/bold green]"
    )

    display_file_status()

    return RAW_DATA_DIR


def display_file_status():
    """Display the availability and size of expected competition files."""

    table = Table(
        title="Competition Data Files",
        box=box.ROUNDED,
        header_style="bold cyan"
    )

    table.add_column("File")
    table.add_column("Status", justify="center")
    table.add_column("Size", justify="right")

    for file in EXPECTED_FILES:
        file_path = RAW_DATA_DIR / file

        if file_path.is_file():
            size_mb = file_path.stat().st_size / (1024 * 1024)

            table.add_row(
                file,
                "[green]Available[/green]",
                f"{size_mb:.2f} MB"
            )
        else:
            table.add_row(
                file,
                "[red]Missing[/red]",
                "-"
            )

    console.print(table)
    console.print(f"\n[dim]Data directory: {RAW_DATA_DIR}[/dim]")


if __name__ == "__main__":
    download_data()