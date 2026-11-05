import kagglehub
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

COMPETITION = 'predicting-housing-affordability-in-the-u-s'
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

EXPECTED_FILES = [
    "sample_submission.csv",
    "test.csv",
    "train.csv"
]

def download_data() -> Path:
    """Downloads the kaggle competition data unless the expected files already exist."""

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    if all((RAW_DATA_DIR / file).is_file() for file in EXPECTED_FILES):
        print(F"[!] Competition files already exist at {RAW_DATA_DIR}")
        return RAW_DATA_DIR
    
    kagglehub.login()

    print(f"[!] Downloading competition: {COMPETITION}")

    path = kagglehub.competition_download(
        COMPETITION,
        output_dir=str(RAW_DATA_DIR),
    )

    print(f"[+] Download complete: {path}")

    return RAW_DATA_DIR


if __name__ == "__main__":
    download_data()