# NovaMart Customer Retention and Campaign Optimization

## Business problem

NovaMart wants to reduce customer churn and use its retention budget more effectively. The business needs to understand which customer characteristics and behaviours are associated with churn, estimate churn risk for current customers, and prioritize customers for a targeted retention campaign.

## Project objective

The project applies descriptive, predictive, and prescriptive analytics to:

- understand and prepare NovaMart customer data;
- identify meaningful churn patterns and business insights;
- build and validate binary classification models;
- score current customers by predicted churn risk; and
- recommend a financially justified retention campaign.

## Datasets

- `NovaMart_Historical_Customers.csv`: 1,215 historical customer records and 20 variables, including the binary target `Churn`.
- `NovaMart_Current_Customers.csv`: 300 current customer records and 19 variables. It excludes `Churn` and will be scored after the final model is selected.

Each record represents one NovaMart customer. `Customer_ID` is the intended identifier. The raw CSV files are source data and must remain unchanged; all prepared or scored data will be written to `outputs/`.

## Analytical workflow

The notebook follows seven project tasks:

1. Data understanding and attribute classification
2. Data preparation and quality assessment
3. Descriptive analytics and exploratory data analysis
4. Predictive model development and validation
5. Model improvement and final selection
6. Current-customer scoring and prescriptive retention planning
7. Final conclusions and deliverable preparation

Task 1 is complete. Later tasks remain intentionally unstarted until they are addressed in sequence.

## Planned deliverables

- `NovaMart_Final_Project.ipynb`: documented, executable analysis
- `outputs/`: prepared datasets, scored customers, retention lists, tables, and figures
- `report/`: final written report
- `presentation/`: final presentation deck

## Repository structure

```text
NovaMart_Final_Project/
├── NovaMart_Final_Project.ipynb
├── NovaMart_Historical_Customers.csv
├── NovaMart_Current_Customers.csv
├── README.md
├── .gitignore
├── outputs/
├── report/
└── presentation/
```

