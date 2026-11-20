import pandas as pd

from typing import Literal

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def print_banner(
    text: str,
    style: str = "cyan",
    title: str | None = None,
) -> None:
    """Print a Rich panel; style controls the border color."""

    console.print(Panel(text, title=title, border_style=style))


def print_table(
    title: str,
    headers: list[str],
    rows: list[tuple],
    first_justify: Literal["left", "center", "right", "full", "default"] = "left",
) -> None:
    """Print a rounded Rich table."""

    table = Table(title=title, box=box.ROUNDED, header_style="bold cyan")

    for i, header in enumerate(headers):
        table.add_column(
            header,
            justify=first_justify if i == 0 else "right",
        )

    for row in rows:
        table.add_row(*map(str, row))

    console.print()
    console.print(table)


def print_dataframe(
    df: pd.DataFrame,
    title: str,
    decimals: int = 4,
) -> None:
    """Print a DataFrame as a Rich table, rounding float columns."""

    rows = [
        tuple(
            f"{v:.{decimals}f}" if isinstance(v, float) else v
            for v in row
        )
        for row in df.itertuples(index=False)
    ]

    print_table(title, df.columns.tolist(), rows)
