from pathlib import Path
import shutil


def get_system_folder(category: str):
    home = Path.home()

    mapping = {
        "Documents": home / "Documents",
        "Music": home / "Music",
        "Images": home / "Pictures",
        "Videos": home / "Videos"
    }

    return mapping.get(category, home / "Downloads")


def move_file(file_path: Path, category: str, mode="out"):
    """
    mode:
    - "out" → move to system folders
    - "keep" → do nothing (just sorting stage)
    """

    if mode == "keep":
        return "kept"

    dest_folder = get_system_folder(category)
    dest_folder.mkdir(parents=True, exist_ok=True)

    destination = dest_folder / file_path.name

    # avoid overwrite
    if destination.exists():
        return "duplicate"

    shutil.move(str(file_path), str(destination))
    return "moved"