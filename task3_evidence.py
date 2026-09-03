import pandas as pd


df = pd.read_csv("outputs/Clean_Historical_Customers.csv")
continuous = [
    "Tenure_Months", "Monthly_Income_JD", "Monthly_Spend_JD", "Total_Orders",
    "Average_Order_Value_JD", "Days_Since_Last_Purchase",
    "Website_Visits_Last_30_Days", "Email_Engagement_Rate",
    "Discount_Usage_Rate", "Satisfaction_Score",
    "Support_Tickets_Last_6_Months", "Complaint_Flag",
    "Last_Campaign_Response"
]

print("SHAPE", df.shape)
print("CHURN", df.Churn.value_counts().sort_index().to_dict(), (df.Churn.value_counts(normalize=True).sort_index()*100).round(2).to_dict())
print("\nDESCRIPTIVE")
print(df[continuous].describe(percentiles=[.25,.5,.75]).T.to_string())
print("\nCHURN GROUP MEANS MEDIANS")
means = df.groupby("Churn")[continuous].mean().T
medians = df.groupby("Churn")[continuous].median().T
comp = pd.concat({"mean": means, "median": medians}, axis=1)
print(comp.to_string())
print("\nMEMBERSHIP")
print(df.groupby("Membership_Level", observed=True).agg(Customers=("Customer_ID","size"),Churned=("Churn","sum"),Churn_Rate=("Churn","mean"),Avg_Spend=("Monthly_Spend_JD","mean")).sort_values("Churn_Rate",ascending=False).assign(Churn_Rate=lambda x:x.Churn_Rate*100).to_string())
for col in ["Complaint_Flag","Last_Campaign_Response","Gender","Region","Payment_Method","Satisfaction_Score"]:
    print("\nGROUP",col)
    print(df.groupby(col, observed=True).agg(Customers=("Customer_ID","size"),Churned=("Churn","sum"),Churn_Rate=("Churn","mean")).assign(Churn_Rate=lambda x:x.Churn_Rate*100).sort_values("Churn_Rate",ascending=False).to_string())
print("\nCORR CHURN")
corr=df[continuous+["Churn"]].corr(numeric_only=True)
print(corr["Churn"].sort_values(ascending=False).to_string())
print("\nSELECTED CORR")
print(corr.loc[["Monthly_Spend_JD","Days_Since_Last_Purchase","Tenure_Months","Satisfaction_Score","Complaint_Flag","Email_Engagement_Rate"],["Monthly_Spend_JD","Days_Since_Last_Purchase","Tenure_Months","Satisfaction_Score","Complaint_Flag","Email_Engagement_Rate","Churn"]].round(4).to_string())

for col in ["Days_Since_Last_Purchase","Monthly_Spend_JD","Tenure_Months","Email_Engagement_Rate"]:
    q=pd.qcut(df[col],4,duplicates="drop")
    print("\nQUARTILES",col)
    print(df.groupby(q, observed=True).Churn.agg(["size","sum","mean"]).assign(mean=lambda x:x["mean"]*100).to_string())
