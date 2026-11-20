# US Housing Affordability Prediction

## Project Overview

This project uses machine learning to predict the percentage of households whose housing costs are at or below 30% of household income across U.S. ZIP codes.

The project explores geographic, demographic, economic, and housing-related characteristics to estimate housing affordability and evaluate how well models generalize to previously unseen ZIP codes.

## Repository Structure

```text
housing_affordability_US/
│
├── .gitignore
├── README.md
├── Report.pdf
├── Report.html
├── requirements.txt
│
├── artifacts/
│   └── ridge_housing_affordability.joblib
│
├── data/
│   ├── raw/
│   │   ├── train.csv
│   │   ├── test.csv
│   │   └── sample_submission.csv
│   │
│   └── clean/
│       ├── train_clean.csv
│       └── test_clean.csv
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_data_quality_and_imputation.ipynb
│   └── 03_baseline_model.ipynb
│
├── reports/
│   ├── data_dictionary.csv
│   ├── model_comparison.csv
│   └── figures/
│
└── src/
    ├── __init__.py
    │
    ├── data/
    │   ├── __init__.py
    │   ├── data_download.py
    │   └── clean_data.py
    │
    ├── models/
    │   ├── __init__.py
    │   ├── evaluate_models.py
    │   ├── train_model.py
    │   └── predict_test.py
    │
    └── utils/
        ├── __init__.py
        ├── model_utils.py
        └── display.py
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

## Dataset Acquisition

## Dataset Acquisition

### 4. Dataset Source and Availability

This project uses the [Predicting Housing Affordability in the U.S. competition dataset](https://www.kaggle.com/competitions/predicting-housing-affordability-in-the-u-s).

The dataset is included in the repository under `data/raw/`, so downloading it separately is not necessary when the files are already available.

The raw dataset contains:

- `train.csv`
- `test.csv`
- `sample_submission.csv`

**If the dataset is missing**, follow these steps to download it:

1. Create or sign in to your [Kaggle account](https://www.kaggle.com/).
2. Open the competition page and accept its rules.
3. Navigate to your Kaggle account settings and generate an API token.
4. From the repository root, execute:

```powershell
python -m src.data.data_download
```

5. Follow the script's prompts to provide your Kaggle API credentials.
6. The dataset will be downloaded into `data/raw/`.

**Data attribution:** The dataset is sourced from the Kaggle competition linked above. Please refer to the competition page for its original source information and applicable usage terms.

Never commit or share your Kaggle API credentials.

## Analysis and Modeling Workflow

### 5. Exploratory Data Analysis

Open and run:

```text
notebooks/01_eda.ipynb
```

This notebook explores the dataset's structure, distributions, relationships, and initial patterns. It also provides an initial understanding of the target variable and potential predictors.

### 6. Data Quality and Imputation

Open and run:

```text
notebooks/02_data_quality_and_imputation.ipynb
```

This notebook investigates missing values, duplicate records, data inconsistencies, and potential imputation strategies.

### 7. Prepare the Clean Dataset

From the repository root, run:

```powershell
python -m src.data.clean_data
```

This script applies the finalized data-cleaning and preparation steps and generates the cleaned datasets under `data/clean/`.

### 8. Baseline Model Development and Evaluation

Open and run:

```text
notebooks/03_baseline_model.ipynb
```

This notebook explores different regression models, feature-selection approaches, preprocessing strategies, and model configurations.

It evaluates model performance using grouped cross-validation to prevent ZIP-code overlap between training and validation folds.

### 9. Final Model Comparison

Run:

```powershell
python -m src.models.evaluate_models
```

This script evaluates and compares the selected model configurations using the finalized feature set, preprocessing pipeline, and evaluation strategy.

It reports performance for previously seen and unseen ZIP codes and calculates the competition-weighted RMSE. The comparison results are saved to:

```text
reports/model_comparison.csv
```

### 10. Train and Save the Final Model

Run:

```powershell
python -m src.models.train_model
```

This script trains the finalized Ridge Regression model using the complete cleaned training dataset and saves the fitted preprocessing and model pipeline as:

```text
artifacts/ridge_housing_affordability.joblib
```

### 11. Generate Predictions

Run:

```powershell
python -m src.models.predict_test
```

The prediction script loads the saved model artifact and provides two prediction modes:

- **Kaggle Test Predictions:** Generates predictions for the competition test dataset and saves the results under `reports/`.
- **Custom Prediction:** Accepts user-provided geographic, demographic, and housing-related characteristics to generate an area-level affordability estimate.

## Additional Notes

- Run all Python module commands from the repository root.
- Activate the `.venv` environment before installing dependencies or executing scripts.
- Downloaded datasets are not included in the Git repository. Use the provided download script to obtain them.
- The fitted model artifact is stored under `artifacts/`.
- Generated reports and figures are stored under `reports/`.
- Never commit Kaggle API credentials or other sensitive information.