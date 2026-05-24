from pathlib import Path

def get_category(file_path: Path):
    extension = file_path.suffix.lower()

    if extension in [".mp3", ".wav", ".flac"]:
        return "Audios"

    elif extension in [".mp4", ".mkv", ".mov"]:
        return "Videos"

    elif extension in [".jpg", ".jpeg", ".png"]:
        return "Images"

    elif extension in [".pdf", ".docx", ".txt"]:
        return "Documents"

    else:
        return "Others"