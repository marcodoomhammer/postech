"""Execute os dois notebooks de revisão usando o Python deste comando.

Uso: python scripts/run_review_notebooks.py
Por padrão, cada notebook tem um kernel próprio. --in-process dispensa sockets.
Qualquer erro interrompe a execução.
"""
import argparse
import json
import sys
import tempfile
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager

ROOT = Path(__file__).resolve().parents[1]


def execute_in_process(notebook):
    """Alternativa explícita para ambientes que bloqueiam sockets de kernels."""
    from IPython.core.interactiveshell import InteractiveShell
    from IPython.utils.capture import capture_output
    InteractiveShell.clear_instance()
    shell = InteractiveShell.instance()
    import matplotlib
    matplotlib.use("Agg", force=True)
    count = 0
    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue
        count += 1
        with capture_output() as captured:
            result = shell.run_cell(cell.source, store_history=True)
        if result.error_before_exec or result.error_in_exec:
            raise RuntimeError(f"Falha na célula {count}") from (result.error_before_exec or result.error_in_exec)
        cell.execution_count = count
        cell.outputs = []
        for name, text in [("stdout", captured.stdout), ("stderr", captured.stderr)]:
            if text:
                cell.outputs.append(nbformat.v4.new_output("stream", name=name, text=text))
        for output in captured.outputs:
            cell.outputs.append(nbformat.v4.new_output("display_data", data=output.data,
                                                      metadata=output.metadata or {}))
    notebook.metadata["review_execution"] = {"mode": "in-process", "python": sys.version.split()[0]}
    InteractiveShell.clear_instance()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in-process", action="store_true", help="Executa sem sockets de kernel")
    args = parser.parse_args()

    # O kernel temporário evita executar com outro Python instalado no computador.
    with tempfile.TemporaryDirectory() as directory:
        kernel = Path(directory) / "churn-review"
        kernel.mkdir()
        (kernel / "kernel.json").write_text(json.dumps({
            "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
            "display_name": "Churn review", "language": "python"}), encoding="utf-8")
        for name in ["02_erros_e_limiares.ipynb", "03_cenarios_da_api.ipynb"]:
            path = ROOT / "notebooks" / name
            notebook = nbformat.read(path, as_version=4)
            if args.in_process:
                import os
                previous = Path.cwd()
                try:
                    os.chdir(ROOT)
                    execute_in_process(notebook)
                finally:
                    os.chdir(previous)
                nbformat.validate(notebook)
                nbformat.write(notebook, path)
                print(f"Executado em processo: {name}", flush=True)
                continue
            manager = KernelManager(kernel_name="churn-review",
                kernel_spec_manager=KernelSpecManager(kernel_dirs=[directory]))
            client = NotebookClient(notebook, km=manager, timeout=180,
                                    resources={"metadata": {"path": str(ROOT)}})
            client.execute()
            notebook.metadata["review_execution"] = {"mode": "jupyter-kernel", "python": sys.version.split()[0]}
            nbformat.validate(notebook)
            nbformat.write(notebook, path)
            print(f"Executado: {name}", flush=True)


if __name__ == "__main__":
    main()
