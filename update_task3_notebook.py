import json
from pathlib import Path


path = Path("NovaMart_Final_Project.ipynb")
nb = json.loads(path.read_text(encoding="utf-8"))


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip("\n").splitlines(keepends=True)}


def code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": text.strip("\n").splitlines(keepends=True)}


task3 = [
md("""
# Task 3 — Descriptive Analytics and Exploratory Data Analysis

### Objective
Describe the cleaned historical customers, compare churned and non-churned groups, visualize important patterns, and quantify associations. This section uses `outputs/Clean_Historical_Customers.csv` only. It performs no train/test splitting, model encoding, feature selection, or predictive modelling.
"""),
code(r'''
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

eda = pd.read_csv("outputs/Clean_Historical_Customers.csv")
assert eda.shape == (1200, 20)
assert eda.isna().sum().sum() == 0

figure_dir = Path("outputs/figures")
figure_dir.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", context="notebook")
COLORS = {0: "#4C78A8", 1: "#E45756"}

def save_and_display(fig, filename):
    fig.tight_layout()
    path = figure_dir / filename
    fig.savefig(path, dpi=160, bbox_inches="tight")
    display(fig)
    plt.close(fig)
    print(f"Saved: {path}")

print("Task 3 dataset loaded:", eda.shape)
'''),
md("""
## 3.1 Focused descriptive statistics

The summary emphasizes customer value, activity, engagement, experience, and recency variables. It includes frequency, mean, median, standard deviation, minimum, quartiles, and maximum. Frequency and percentage tables are shown separately for important categorical and binary attributes.
"""),
code(r'''
business_numeric = [
    "Tenure_Months", "Monthly_Income_JD", "Monthly_Spend_JD",
    "Total_Orders", "Average_Order_Value_JD",
    "Days_Since_Last_Purchase", "Website_Visits_Last_30_Days",
    "Email_Engagement_Rate", "Discount_Usage_Rate",
    "Satisfaction_Score", "Support_Tickets_Last_6_Months"
]

descriptive_statistics = eda[business_numeric].describe(percentiles=[0.25, 0.50, 0.75]).T
descriptive_statistics = descriptive_statistics.rename(columns={
    "count": "Frequency", "std": "Std_Dev", "25%": "Q1",
    "50%": "Median", "75%": "Q3", "min": "Minimum", "max": "Maximum"
})[["Frequency", "mean", "Median", "Std_Dev", "Minimum", "Q1", "Q3", "Maximum"]]
descriptive_statistics = descriptive_statistics.rename(columns={"mean": "Mean"}).round(3)
display(descriptive_statistics)

frequency_variables = [
    "Churn", "Membership_Level", "Complaint_Flag",
    "Last_Campaign_Response", "Satisfaction_Score"
]
frequency_tables = {}
for column in frequency_variables:
    table = eda[column].value_counts(dropna=False).rename("Frequency").to_frame()
    table["Percentage"] = (table["Frequency"] / len(eda) * 100).round(2)
    frequency_tables[column] = table
    print(f"\n{column}")
    display(table)
'''),
md("""
### Descriptive interpretation

The cleaned historical sample contains **1,200 customers**: **950 (79.17%)** did not churn and **250 (20.83%)** churned. Median tenure is **27 months**, median monthly income is **JD 1,792.63**, and median monthly spend is **JD 180.52**. Purchase recency is right-skewed: the median is **29 days**, the upper quartile is **58.25 days**, and the maximum is **600 days**. The unusually large maxima in income, spending, visits, and tickets are the legitimate outliers retained after the Task 2 review, so means should be interpreted alongside medians and quartiles.
"""),
md("""
## 3.2 Churned versus non-churned group comparisons

Means and medians are calculated for every requested numeric or binary attribute. For binary flags, the mean is the proportion equal to 1. Membership level is compared separately using counts, churn counts, churn percentages, and sorted average spending.
"""),
code(r'''
comparison_variables = [
    "Tenure_Months", "Monthly_Income_JD", "Monthly_Spend_JD",
    "Total_Orders", "Average_Order_Value_JD",
    "Days_Since_Last_Purchase", "Website_Visits_Last_30_Days",
    "Email_Engagement_Rate", "Discount_Usage_Rate",
    "Satisfaction_Score", "Support_Tickets_Last_6_Months",
    "Complaint_Flag", "Last_Campaign_Response"
]

group_means = eda.groupby("Churn")[comparison_variables].mean().T
group_medians = eda.groupby("Churn")[comparison_variables].median().T
churn_comparison = pd.DataFrame({
    "Non_Churn_Mean": group_means[0],
    "Churn_Mean": group_means[1],
    "Mean_Difference_Churn_Minus_NonChurn": group_means[1] - group_means[0],
    "Non_Churn_Median": group_medians[0],
    "Churn_Median": group_medians[1],
}).round(3)
display(churn_comparison)

membership_comparison = (
    eda.groupby("Membership_Level", observed=True)
       .agg(Customers=("Customer_ID", "size"), Churned=("Churn", "sum"),
            Churn_Rate=("Churn", "mean"), Average_Monthly_Spend_JD=("Monthly_Spend_JD", "mean"))
       .assign(Churn_Rate_Percent=lambda x: (x["Churn_Rate"] * 100).round(2))
       .drop(columns="Churn_Rate")
       .sort_values("Churn_Rate_Percent", ascending=False)
)
membership_comparison["Average_Monthly_Spend_JD"] = membership_comparison["Average_Monthly_Spend_JD"].round(2)
display(membership_comparison)

binary_group_comparison = pd.concat({
    column: eda.groupby(column).agg(
        Customers=("Customer_ID", "size"), Churned=("Churn", "sum"), Churn_Rate=("Churn", "mean")
    ).assign(Churn_Rate_Percent=lambda x: (x["Churn_Rate"] * 100).round(2)).drop(columns="Churn_Rate")
    for column in ["Complaint_Flag", "Last_Campaign_Response"]
})
display(binary_group_comparison)
'''),
md("""
### Group-comparison interpretation

Evidence is mixed across variables, so no importance is assumed. Churned customers show longer mean purchase recency (**66.61 vs 36.28 days**) and more support tickets (**2.54 vs 1.58**), while non-churned customers show higher satisfaction (**3.66 vs 3.34**), tenure (**31.66 vs 27.55 months**), and campaign response prevalence (**42.11% vs 30.40%**). Monthly income, spend, visits, and discount use have smaller group differences and should not be overstated.
"""),
md("""
## 3.3 Visualizations

Nine figures cover distributions, group comparisons, numerical relationships, and churn-specific rates. All figures are displayed here and saved under `outputs/figures/`.
"""),
code(r'''
# Figure 1 — churn frequency and percentage
counts = eda["Churn"].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.bar(["Non-churned (0)", "Churned (1)"], counts.values, color=[COLORS[0], COLORS[1]])
for bar, count in zip(bars, counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, count + 15, f"{count:,}\n({count/len(eda):.1%})", ha="center")
ax.set_title("Historical Customer Churn Distribution")
ax.set_xlabel("Churn status")
ax.set_ylabel("Number of customers")
ax.set_ylim(0, counts.max() * 1.15)
save_and_display(fig, "01_churn_distribution.png")
'''),
code(r'''
# Figure 2 — spend distribution; log x-axis keeps retained outliers visible
fig, ax = plt.subplots(figsize=(8, 4.8))
positive_spend = eda["Monthly_Spend_JD"]
bins = np.geomspace(positive_spend.min(), positive_spend.max(), 35)
ax.hist(positive_spend, bins=bins, color="#59A14F", edgecolor="white")
ax.set_xscale("log")
ax.axvline(positive_spend.median(), color="#B22222", linestyle="--", label=f"Median = JD {positive_spend.median():.2f}")
ax.set_title("Distribution of Monthly Customer Spend")
ax.set_xlabel("Monthly spend (JD, logarithmic scale)")
ax.set_ylabel("Number of customers")
ax.legend()
save_and_display(fig, "02_monthly_spend_distribution.png")
'''),
code(r'''
# Figure 3 — recency by churn
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=eda, x="Churn", y="Days_Since_Last_Purchase", hue="Churn", palette=COLORS, legend=False, ax=ax)
ax.set_yscale("symlog", linthresh=10)
ax.set_title("Purchase Recency by Churn Status")
ax.set_xlabel("Churn status (0 = non-churned, 1 = churned)")
ax.set_ylabel("Days since last purchase (symlog scale)")
save_and_display(fig, "03_purchase_recency_by_churn.png")
'''),
code(r'''
# Figure 4 — membership churn rate
membership_rates = membership_comparison["Churn_Rate_Percent"].sort_values()
fig, ax = plt.subplots(figsize=(8, 4.8))
bars = ax.barh(membership_rates.index, membership_rates.values, color="#F28E2B")
for bar, value in zip(bars, membership_rates.values):
    ax.text(value + 0.3, bar.get_y() + bar.get_height()/2, f"{value:.1f}%", va="center")
ax.set_title("Churn Rate by Membership Level")
ax.set_xlabel("Churn rate (%)")
ax.set_ylabel("Membership level")
ax.set_xlim(0, membership_rates.max() * 1.18)
save_and_display(fig, "04_churn_rate_by_membership.png")
'''),
code(r'''
# Figure 5 — complaints and churn
complaint_rates = eda.groupby("Complaint_Flag")["Churn"].mean().mul(100)
fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.bar(["No complaint (0)", "Complaint (1)"], complaint_rates.values, color=["#76B7B2", "#E15759"])
for bar, value in zip(bars, complaint_rates.values):
    ax.text(bar.get_x()+bar.get_width()/2, value+0.6, f"{value:.1f}%", ha="center")
ax.set_title("Churn Rate by Complaint Status")
ax.set_xlabel("Complaint status")
ax.set_ylabel("Churn rate (%)")
ax.set_ylim(0, complaint_rates.max() * 1.18)
save_and_display(fig, "05_churn_rate_by_complaint.png")
'''),
code(r'''
# Figure 6 — prior campaign response and churn
campaign_rates = eda.groupby("Last_Campaign_Response")["Churn"].mean().mul(100)
fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.bar(["No response (0)", "Responded (1)"], campaign_rates.values, color=["#E15759", "#59A14F"])
for bar, value in zip(bars, campaign_rates.values):
    ax.text(bar.get_x()+bar.get_width()/2, value+0.5, f"{value:.1f}%", ha="center")
ax.set_title("Churn Rate by Last Campaign Response")
ax.set_xlabel("Last campaign response")
ax.set_ylabel("Churn rate (%)")
ax.set_ylim(0, campaign_rates.max() * 1.20)
save_and_display(fig, "06_churn_rate_by_campaign_response.png")
'''),
code(r'''
# Figure 7 — satisfaction and churn
satisfaction_rates = eda.groupby("Satisfaction_Score").agg(Customers=("Customer_ID", "size"), Churn_Rate=("Churn", "mean"))
fig, ax = plt.subplots(figsize=(8, 4.8))
bars = ax.bar(satisfaction_rates.index.astype(str), satisfaction_rates["Churn_Rate"]*100, color="#B07AA1")
for bar, rate, n in zip(bars, satisfaction_rates["Churn_Rate"]*100, satisfaction_rates["Customers"]):
    ax.text(bar.get_x()+bar.get_width()/2, rate+1, f"{rate:.1f}%\n(n={n})", ha="center", fontsize=9)
ax.set_title("Churn Rate by Satisfaction Score")
ax.set_xlabel("Satisfaction score (1 = lowest, 5 = highest)")
ax.set_ylabel("Churn rate (%)")
ax.set_ylim(0, 75)
save_and_display(fig, "07_churn_rate_by_satisfaction.png")
'''),
code(r'''
# Figure 8 — strongest non-target numerical relationship
fig, ax = plt.subplots(figsize=(8, 5.2))
sns.scatterplot(data=eda, x="Tenure_Months", y="Total_Orders", hue="Churn", palette=COLORS, alpha=0.65, ax=ax)
ax.set_title("Relationship Between Customer Tenure and Total Orders")
ax.set_xlabel("Tenure (months)")
ax.set_ylabel("Total orders")
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, ["Non-churned", "Churned"], title="Churn status")
save_and_display(fig, "08_tenure_vs_total_orders.png")
'''),
md("""
## 3.4 Correlation and relationship analysis

Pearson correlations summarize linear association among numerical measures. Binary `Churn`, complaint, and campaign-response indicators can be included numerically, but their correlations should still be interpreted as associations rather than causal effects.

**Correlation indicates statistical association and does not by itself establish causation.**
"""),
code(r'''
correlation_variables = comparison_variables + ["Churn"]
correlation_matrix = eda[correlation_variables].corr()
churn_correlations = (
    correlation_matrix["Churn"].drop("Churn")
    .sort_values(key=lambda values: values.abs(), ascending=False)
    .rename("Correlation_with_Churn").to_frame().round(3)
)
display(churn_correlations)

selected_corr_variables = [
    "Tenure_Months", "Total_Orders", "Monthly_Spend_JD",
    "Average_Order_Value_JD", "Days_Since_Last_Purchase",
    "Email_Engagement_Rate", "Satisfaction_Score",
    "Support_Tickets_Last_6_Months", "Complaint_Flag",
    "Last_Campaign_Response", "Churn"
]
selected_correlation_matrix = eda[selected_corr_variables].corr().round(3)
display(selected_correlation_matrix)

fig, ax = plt.subplots(figsize=(11, 8))
sns.heatmap(selected_correlation_matrix, cmap="vlag", center=0, vmin=-1, vmax=1, annot=True, fmt=".2f", linewidths=0.4, ax=ax)
ax.set_title("Selected Numerical Correlation Matrix")
ax.set_xlabel("Variable")
ax.set_ylabel("Variable")
save_and_display(fig, "09_selected_correlation_matrix.png")
'''),
md("""
### Correlation interpretation

The largest positive correlations with churn are purchase recency (**r = 0.269**), support tickets (**r = 0.219**), and complaint status (**r = 0.206**). The largest negative associations are satisfaction (**r = −0.149**), last campaign response (**r = −0.097**), email engagement (**r = −0.086**), and tenure (**r = −0.085**). Website visits (**r = 0.008**) and discount usage (**r = −0.011**) have almost no linear association with churn in this sample.

Among non-target variables, tenure and total orders are strongly positively related (**r = 0.841**); monthly spending and average order value are moderately positively related (**r = 0.451**); and satisfaction and support tickets are negatively related (**r = −0.224**). These are descriptive associations, not proof of cause and effect.
"""),
md("""
## 3.5 Evidence-based business findings

1. **Overall churn:** The historical data contains **250 churned customers out of 1,200**, a churn rate of **20.83%**.
2. **Purchase recency:** Churned customers averaged **66.61 days** since their last purchase versus **36.28 days** for non-churned customers. Customers in the highest-recency quartile had a **37.67%** churn rate, compared with **13.67%** in the lowest quartile.
3. **Complaints:** Customers with a complaint had a **33.71%** churn rate (**120 of 356**) compared with **15.40%** (**130 of 844**) among customers without a complaint.
4. **Support demand:** Churned customers averaged **2.54 support tickets** in six months versus **1.58** for non-churned customers; support tickets were positively associated with churn (**r = 0.219**).
5. **Satisfaction:** Customers scoring 2 had a **41.90%** churn rate (**44 of 105**), compared with **12.87%** (**22 of 171**) for customers scoring 5. Satisfaction was negatively associated with churn (**r = −0.149**).
6. **Campaign response:** Customers who responded to the last campaign showed a **15.97%** churn rate (**76 of 476**) versus **24.03%** (**174 of 724**) among non-responders.
7. **Membership:** Basic members showed the highest membership-level churn rate at **24.20%** (**113 of 467**), while Platinum members showed the lowest at **13.53%** (**18 of 133**).
8. **Email engagement:** The lowest email-engagement quartile showed a **28.67%** churn rate (**86 of 300**) versus **17.33%** (**52 of 300**) in the highest quartile. Churned customers also had lower mean engagement (**0.392 vs 0.433**).

All findings describe relationships in the historical data. They do not establish that any attribute causes churn.
"""),
md("""
## Task 3 Conclusion

The EDA identifies the clearest churn patterns around purchase recency, customer-service friction, satisfaction, previous campaign response, membership level, tenure, and email engagement. Income, monthly spend, discount use, and website visits show comparatively weak direct linear associations with churn. These results provide evidence to guide later modelling, but Task 4 has not been started.
"""),
]

nb["cells"] = nb["cells"][:37] + task3 + nb["cells"][38:]
path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
