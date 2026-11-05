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

## 4. Dataset

The competition dataset is included in the repository under `data/raw/`.

The following files are already available:

- `train.csv`
- `test.csv`
- `sample_submission.csv`

No Kaggle authentication or additional download is required.

If you want to download the dataset again, you can optionally run:

```powershell
python src/data/data_download.py
```

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
- The raw competition CSV files are included in the repository under `data/raw/`.
- The `.gitignore` excludes Python cache files, Jupyter checkpoints, the virtual environment, and downloaded raw data.
- Never share your Kaggle API token or commit it to the repository.
