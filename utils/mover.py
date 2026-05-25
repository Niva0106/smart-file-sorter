from pathlib import Path
import shutil


def move_file(file_path: Path, category: str, destination: Path = None, mode="custom"):
    if mode == "system":
        home = Path.home()

        mapping = {
            "Documents": home / "Documents",
            "Music": home / "Music",
            "Images": home / "Pictures",
            "Videos": home / "Videos"
        }

        destination = mapping.get(category, home / "Downloads")

    if destination is None:
        return "no_destination"

    destination.mkdir(parents=True, exist_ok=True)

    target = destination / file_path.name

    if target.exists():
        return "duplicate"

    shutil.move(str(file_path), str(target))
    return "moved"