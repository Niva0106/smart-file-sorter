from pathlib import Path

def get_file_info(file_path: Path):
    return {
        "name": file_path.name,
        "extension": file_path.suffix,
        "size": file_path.stat().st_size
    }