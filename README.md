# US Housing Affordability Prediction

## Repository Structure

```text
us-housing-affordability-prediction/
│
├── .gitignore
├── README.md
├── requirements.txt
│
├── data/### 4. Download the Dataset

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

**C. Accept the Competition Rules**

Visit the [Kaggle competition page](https://www.kaggle.com/competitions/predicting-housing-affordability-in-the-u-s/overview) and accept the competition rules if prompted. Your Kaggle account must have access to the competition data.

**D. Run the Download Script**

From the repository root, execute:

```bash
python src/data/data_download.py
```

The downloaded files should be available under `data/raw/`:

- `train.csv`
- `test.csv`
- `sample_submission.csv`

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