from pathlib import Path
import os
import shutil
import subprocess
import webbrowser

APP_DIR = Path(__file__).resolve().parent
HTML_FILE = APP_DIR / "index.html"


def find_browser():
    candidates = [
        "chrome", "google-chrome", "chromium", "chromium-browser",
        "msedge", "microsoft-edge", "firefox"
    ]
    for name in candidates:
        path = shutil.which(name)
        if path:
            return path, Path(path).name.lower()

    # Common Windows installation locations (browsers are not always on PATH).
    local = Path(os.environ.get("LOCALAPPDATA", ""))
    program_files = Path(os.environ.get("PROGRAMFILES", ""))
    program_files_x86 = Path(os.environ.get("PROGRAMFILES(X86)", ""))
    windows_candidates = [
        local / "Google/Chrome/Application/chrome.exe",
        program_files / "Google/Chrome/Application/chrome.exe",
        program_files_x86 / "Google/Chrome/Application/chrome.exe",
        local / "Microsoft/Edge/Application/msedge.exe",
        program_files / "Microsoft/Edge/Application/msedge.exe",
        program_files_x86 / "Microsoft/Edge/Application/msedge.exe",
    ]
    for path in windows_candidates:
        if path.exists():
            return str(path), path.name.lower()

    return None, None


def launch():
    if not HTML_FILE.exists():
        raise FileNotFoundError(f"Missing interface file: {HTML_FILE}")

    browser, name = find_browser()
    url = HTML_FILE.as_uri()

    if browser and name not in {"firefox"}:
        # Chromium/Chrome/Edge app mode creates a separate, clean application window.
        subprocess.Popen([
            browser,
            "--app=" + url,
            "--start-maximized",
            "--disable-session-crashed-bubble",
        ])
        return

    if browser == "firefox":
        subprocess.Popen([browser, "-new-window", url])
        return

    # Last-resort fallback: use the user's default browser.
    if not webbrowser.open(url, new=1):
        raise RuntimeError(
            "No supported browser was found. Install Google Chrome, Microsoft Edge, "
            "Chromium, or Firefox, then run python main.py again."
        )


if __name__ == "__main__":
    launch()
