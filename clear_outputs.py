import subprocess
import sys
import nbformat
from pathlib import Path

def clear_output(notebook_path):
    """Clear the output of a Jupyter notebook."""
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)
    for cell in notebook.cells:
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None
    with open(notebook_path, "w", encoding="utf-8") as f:
        nbformat.write(notebook, f)
    print(f"Cleared outputs for {notebook_path}")

def main():
    modified_files = []
    for path in sys.argv[1:]:
        notebook_path = Path(path)
        if notebook_path.exists() and notebook_path.suffix == ".ipynb":
            clear_output(notebook_path)
            modified_files.append(notebook_path)

    # Automatically re-add modified files to git
    for file in modified_files:
        subprocess.run(["git", "add", str(file)], check=True)

if __name__ == "__main__":
    main()
