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

### 2. Create and Activate a Conda Environment

Create a Conda environment using Python 3.12:

```bash
conda create -n housing-afford python=3.12 -y
conda activate housing-afford
```

### 3. Install Dependencies

With the Conda environment activated, install the required packages:

```bash
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

Start Jupyter Notebook:

```bash
jupyter notebook
```

Open:

`notebooks/01_eda.ipynb`

Select the `housing-afford` Conda kernel if prompted, then run the notebook cells.

If the environment is not available as a Jupyter kernel, install and register it:

```bash
python -m pip install ipykernel
python -m ipykernel install --user --name housing-afford --display-name "Python (housing-afford)"
```

## Notes

- Run commands from the repository root directory.
- Activate the Conda environment before installing dependencies or running the notebook.
- Raw CSV files are excluded from Git and must be downloaded locally.
- The `.gitignore` excludes Python cache files, Jupyter checkpoints, and downloaded raw data.
- Never share your Kaggle API token or commit it to the repository.