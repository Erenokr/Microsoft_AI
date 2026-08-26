import subprocess
import shlex
from pathlib import Path


def open_terminal():
    project_path = Path(__file__).resolve().parent

    python_path = project_path / ".venv" / "bin" / "python"

    if not python_path.exists():
        raise RuntimeError("Python ortamı bulunamadı. Önce setup.sh dosyasını çalıştırın.")

    command = (
        f"cd {shlex.quote(str(project_path))} && "
        f"{shlex.quote(str(python_path))} main.py"
    )

    apple_script = f'''
    tell application "Terminal"
        activate
        do script "{command}"
    end tell
    '''

    subprocess.run(
        ["osascript", "-e", apple_script]
    )


if __name__ == "__main__":
    open_terminal()
