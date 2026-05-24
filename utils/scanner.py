from pathlib import Path

def scan_downloads():
    downloads = Path.home() / "Downloads"

    if not downloads.exists():
        return []

    files = []

    for item in downloads.rglob("*"):
        if item.is_file():
            files.append(item)

    return files