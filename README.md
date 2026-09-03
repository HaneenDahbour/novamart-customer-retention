# NovaMart Customer Retention and Campaign Optimization

Applied Analytical Models final project for an end-to-end churn analytics and retention optimization workflow.

## Business Objective

NovaMart wants to understand historical customer churn, identify risk patterns, predict which current customers may leave, and allocate a limited retention budget to customers with the strongest expected business value.

## Data

- `NovaMart_Historical_Customers.csv`: 1,215 raw records with the `Churn` target.
- `NovaMart_Current_Customers.csv`: 300 current customers without a churn label.
- Clean historical data: 1,200 unique customer records after quality preparation.
- Historical churn rate after cleaning: 20.83%.

## Analytical Workflow

1. Data understanding and attribute classification
2. Data preparation and quality assessment
3. Descriptive analytics and exploratory data analysis
4. Baseline predictive modelling
5. Model improvement and final model selection
6. Current-customer scoring
7. Prescriptive retention campaign and what-if analysis

## Key Historical Findings

- Customers with complaints had a 33.71% churn rate vs 15.40% without complaints.
- Previous campaign non-responders had 24.03% churn vs 15.97% among responders.
- Basic members had 24.20% churn vs 13.53% for Platinum members.
- Customers in the highest purchase-recency quartile had 37.67% churn vs 13.67% in the most recent-purchase quartile.
- The lowest email-engagement quartile had 28.67% churn vs 17.33% in the highest quartile.
- Satisfaction score 2 had 41.90% churn vs 12.87% for score 5.

These are associations in observational data and should not be interpreted as causal effects.

## Predictive Models

Two baseline classifiers were compared:

- Logistic Regression
- Random Forest

### Baseline Test Performance

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.8042 | 0.5714 | 0.2400 | 0.3380 | 0.7792 |
| Random Forest | 0.7875 | 0.4444 | 0.0800 | 0.1356 | 0.7211 |

## Model Improvement

Two justified improvement techniques were applied:

- class weighting for the imbalanced churn target;
- training-only hyperparameter tuning using five-fold stratified cross-validation.

### Improved Test Performance

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Class-weighted Logistic Regression | 0.7208 | 0.4000 | 0.6800 | 0.5037 | 0.7822 |
| Tuned Random Forest | 0.8042 | 0.5319 | 0.5000 | 0.5155 | 0.7799 |

The final model is **class-weighted Logistic Regression** because it achieved stronger churn recall, slightly higher ROC-AUC, better generalization stability, and greater interpretability for the size and purpose of the dataset.

## Probability Calibration Limitation

The final weighted Logistic Regression had a held-out mean predicted churn probability of 43.87% while the observed churn rate was 20.83%. Sigmoid calibration improved Brier score from 0.1923 to 0.1383, but recall at the required 0.50 threshold fell from 68% to 12%. The uncalibrated weighted model was therefore retained for the assignment workflow.

Because Task 6 uses probabilities directly in expected-value calculations, campaign financial outputs should be interpreted as **model-based estimates under the supplied assumptions**, not guaranteed outcomes.

## Retention Recommendation

The final model scored all 300 current customers.

- Predicted to churn at the required 0.50 threshold: 105 customers (35.0%)
- Eligible for retention after the positive-net-benefit rule: 105
- Final selected campaign: top 50 by expected net benefit

### What-if Comparison

| Scenario | Contacted | Cost (JD) | Expected Retained | Expected Saved Profit (JD) | Expected Net Benefit (JD) |
|---|---:|---:|---:|---:|---:|
| Top 25 | 25 | 500.00 | 6.70 | 5,346.51 | 4,846.51 |
| Top 50 | 50 | 1,000.00 | 13.35 | 8,609.35 | 7,609.35 |

**Recommendation: Top 50.** Expanding from 25 to 50 customers costs an additional JD 500 but adds approximately JD 2,762.84 in expected net benefit under the project assumptions.

## Project Structure

```text
NovaMart_Final_Project/
├── NovaMart_Final_Project.ipynb
├── NovaMart_Historical_Customers.csv
├── NovaMart_Current_Customers.csv
├── README.md
├── requirements.txt
├── outputs/
│   ├── Clean_Historical_Customers.csv
│   ├── Clean_Current_Customers.csv
│   ├── NovaMart_Scored_Current_Customers.csv
│   └── figures/
└── report/
    └── NovaMart_Final_Report.pdf
```

## Setup

Python 3.14 was used for the project.

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run the Notebook

From the project directory:

```powershell
jupyter lab
```

Open `NovaMart_Final_Project.ipynb` and run all cells from top to bottom.

The notebook should recreate the cleaned data, model outputs, scored current-customer file, figures, campaign calculations, and validation checks.

## Main Deliverables

- `NovaMart_Final_Project.ipynb`
- `outputs/Clean_Historical_Customers.csv`
- `outputs/Clean_Current_Customers.csv`
- `outputs/NovaMart_Scored_Current_Customers.csv`
- `report/NovaMart_Final_Report.pdf`

## Limitations

- The cleaned historical sample contains 1,200 records.
- Observational relationships are not causal evidence.
- Absolute churn probabilities are imperfectly calibrated.
- Profit margin, campaign cost, and retention effectiveness are supplied assumptions.
- Expected financial values are estimates and should be validated against real campaign outcomes.

## Repository

https://github.com/HaneenDahbour/novamart-customer-retention
