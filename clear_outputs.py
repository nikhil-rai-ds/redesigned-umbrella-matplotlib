import nbformat
from pathlib import Path
import sys
import subprocess

def clear_output(notebook_path):
    """Clear outputs of a Jupyter notebook."""
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    # Clear outputs for each code cell
    modified = False
    for cell in notebook.cells:
        if cell.cell_type == "code":
            if cell.outputs or cell.execution_count is not None:
                cell.outputs = []
                cell.execution_count = None
                modified = True

    # Write back the changes only if outputs were cleared
    if modified:
        with open(notebook_path, "w", encoding="utf-8") as f:
            nbformat.write(notebook, f)
        print(f"Cleared outputs for {notebook_path}")
    else:
        print(f"No outputs to clear in {notebook_path}")
    return modified

def main():
    modified_files = []
    for notebook in sys.argv[1:]:
        notebook_path = Path(notebook)
        if notebook_path.exists() and notebook_path.suffix == ".ipynb":
            if clear_output(notebook_path):
                modified_files.append(notebook_path)

    # Automatically re-add modified files to git staging
    if modified_files:
        subprocess.run(["git", "add"] + [str(file) for file in modified_files], check=True)

if __name__ == "__main__":
    main()
