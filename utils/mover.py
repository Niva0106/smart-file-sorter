from pathlib import Path
import shutil

def move_file(file_path: Path, category: str, destination_folder: Path):
    category_folder = destination_folder / category
    category_folder.mkdir(parents=True, exist_ok=True)

    destination_path = category_folder / file_path.name

    shutil.move(str(file_path), str(destination_path))

    return destination_path