import base64
import contextlib
import io
import json
import traceback
from pathlib import Path


path = Path("NovaMart_Final_Project.ipynb")
notebook = json.loads(path.read_text(encoding="utf-8"))
namespace = {"__name__": "__main__"}
execution_count = 0

for cell in notebook["cells"]:
    if cell.get("cell_type") != "code":
        continue
    execution_count += 1
    outputs = []

    def display(*objects):
        for obj in objects:
            if hasattr(obj, "savefig"):
                image_buffer = io.BytesIO()
                obj.savefig(image_buffer, format="png", dpi=120, bbox_inches="tight")
                outputs.append({
                    "data": {"image/png": base64.b64encode(image_buffer.getvalue()).decode("ascii"), "text/plain": repr(obj)},
                    "metadata": {}, "output_type": "display_data",
                })
                continue
            data = {"text/plain": repr(obj)}
            if hasattr(obj, "to_html"):
                data["text/html"] = obj.to_html()
            outputs.append({"data": data, "metadata": {}, "output_type": "display_data"})

    namespace["display"] = display
    stdout = io.StringIO()
    stderr = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exec(compile("".join(cell.get("source", [])), "<notebook-cell>", "exec"), namespace)
    except Exception as exc:
        for name, stream in [("stdout", stdout), ("stderr", stderr)]:
            if stream.getvalue():
                outputs.insert(0, {"name": name, "output_type": "stream", "text": stream.getvalue()})
        outputs.append({"ename": type(exc).__name__, "evalue": str(exc), "output_type": "error", "traceback": traceback.format_exc().splitlines()})
        cell["outputs"], cell["execution_count"] = outputs, execution_count
        path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        raise

    for name, stream in [("stdout", stdout), ("stderr", stderr)]:
        if stream.getvalue():
            outputs.insert(0, {"name": name, "output_type": "stream", "text": stream.getvalue()})
    cell["outputs"], cell["execution_count"] = outputs, execution_count

path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Executed {execution_count} code cells successfully and saved all outputs.")
