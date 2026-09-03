import json
from pathlib import Path

from PIL import Image
import pandas as pd


nb = json.loads(Path("NovaMart_Final_Project.ipynb").read_text(encoding="utf-8"))
errors, warnings = [], []
image_outputs = 0
for i, cell in enumerate(nb["cells"]):
    for output in cell.get("outputs", []):
        if output.get("output_type") == "error":
            errors.append((i, output.get("ename"), output.get("evalue")))
        if output.get("name") == "stderr" and output.get("text", "").strip():
            warnings.append((i, output["text"]))
        if "image/png" in output.get("data", {}):
            image_outputs += 1

figures = sorted(Path("outputs/figures").glob("*.png"))
figure_info = []
for path in figures:
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        figure_info.append((path.name, image.size, path.stat().st_size))

df = pd.read_csv("outputs/Clean_Historical_Customers.csv")
task4_cells = ["".join(c.get("source", [])) for c in nb["cells"] if "# Task 4" in "".join(c.get("source", []))]

print("notebook_cells", len(nb["cells"]))
print("executed_code_cells", sum(c.get("cell_type") == "code" and c.get("execution_count") is not None for c in nb["cells"]))
print("error_outputs", errors)
print("warning_streams", warnings)
print("embedded_png_outputs", image_outputs)
print("figures", figure_info)
print("task4", task4_cells)
print("shape", df.shape)
print("churn", df.Churn.value_counts().sort_index().to_dict())
print("churn_rate", round(df.Churn.mean()*100, 2))
print("complaint_rates", (df.groupby("Complaint_Flag").Churn.mean()*100).round(2).to_dict())
print("campaign_rates", (df.groupby("Last_Campaign_Response").Churn.mean()*100).round(2).to_dict())
print("membership_rates", (df.groupby("Membership_Level").Churn.mean()*100).round(2).to_dict())
print("VALIDATION PASSED")

assert not errors and not warnings
assert image_outputs == 9 and len(figures) == 9
assert len(task4_cells) == 1 and "To be completed next" in task4_cells[0]
assert df.shape == (1200, 20)
