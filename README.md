# US Housing Affordability Prediction

## Repository Structure

```text
us-housing-affordability-prediction/
│
├── .gitignore
├── README.md
├── requirements.txt
│
├── data/
│
├── notebooks/
│   └── 01_eda.ipynb
│
├── reports/
│   ├── data_dictionary.csv
│   └── figures/
│       └── [EDA visualizations]
│
└── src/
    └── data/
        └── data_download.py
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/g-ritvik/us-housing-affordability-prediction.git
cd us-housing-affordability-prediction
```

### 2. Create and Activate a Virtual Environment

This project uses Python's built-in `venv` module to manage dependencies. Python 3.12 is recommended.

Create the virtual environment:

```powershell
py -3.12 -m venv .venv
```

**A. Configure PowerShell Execution Policy (Windows)**

If PowerShell prevents the virtual environment activation script from running, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

This temporarily allows scripts to run in the current PowerShell session. It does not permanently change your system's execution policy.

**B. Activate the Virtual Environment**

```powershell
.\.venv\Scripts\Activate.ps1
```

Once activated, `(.venv)` should appear in your terminal prompt.

### 3. Install Dependencies

With the virtual environment activated, install the required packages:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Download the Dataset

The dataset is hosted on Kaggle and requires authentication before downloading.

**A. Generate a Kaggle API Token**

1. Create or sign in to your Kaggle account.
2. Visit [Kaggle API Settings](https://www.kaggle.com/settings/api).
3. Under **API Tokens**, select **Generate New Token**.
4. Copy the generated API token.

**B. Download the Dataset**

From the repository root, run:

```bash
python src/data/data_download.py
```

When prompted, paste your Kaggle API token. The script will authenticate with KaggleHub and download the competition dataset.

If prompted, visit the [Kaggle competition page](https://www.kaggle.com/competitions/predicting-housing-affordability-in-the-u-s/overview) and accept the competition rules before downloading.

The downloaded files should be available under `data/raw/`:

- `train.csv`
- `test.csv`
- `sample_submission.csv`

**Security:** Never share your Kaggle API token or commit it to GitHub.

### 5. Run the EDA Notebook

Register the virtual environment as a Jupyter kernel:

```powershell
python -m ipykernel install --user --name housing-afford --display-name "Python (housing-afford)"
```

Start Jupyter Notebook from the repository root:

```bash
jupyter notebook
```

Open `notebooks/01_eda.ipynb` and select **Python (housing-afford)** as the notebook kernel.

If the Jupyter Notebook command is unavailable, verify that `notebook` and `ipykernel` are included in `requirements.txt` and installed in the active virtual environment.

## Notes

- Run commands from the repository root directory.
- Activate the `.venv` environment before installing dependencies, downloading data, or running the notebook.
- Raw CSV files are excluded from Git and must be downloaded locally.
- The `.gitignore` excludes Python cache files, Jupyter checkpoints, the virtual environment, and downloaded raw data.
- Never share your Kaggle API token or commit it to the repository.