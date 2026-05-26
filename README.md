# Smart Sorter

Smart Sorter is a small desktop utility made with Python and PySide6 that helps organize messy Downloads folders faster and more comfortably.

Instead of manually opening many folders and moving files one by one using the normal file explorer, Smart Sorter focuses on quick file organization and saved destinations.

This project was made mainly for personal use and learning desktop application development.

---

# What Makes It Different From File Explorer?

File Explorer already allows moving and sorting files manually.

Smart Sorter tries to make that process quicker by:

- Automatically sorting files by type
- Allowing multiple files to be moved quickly
- Saving frequently used destinations
- Reducing repeated folder navigation
- Focusing mainly on Downloads management

Example:

## Normal File Explorer Workflow

- Open Downloads
- Select files
- Right click
- Click Move
- Browse folders again
- Repeat every time

## Smart Sorter Workflow

- Open app
- Select files
- Choose saved destination
- Move instantly

The goal is not to replace File Explorer, but to make repetitive organization tasks easier.

---

# Features

## Sorter
- Scan Downloads folder
- Automatically categorize files
- Sort files into folders like:
  - Documents
  - Images
  - Videos
  - Audios
  - Others

## Mover
- Select multiple files
- Move files quickly
- Save custom destinations
- Add/Edit/Delete saved destinations
- Search files easily

## UI
- Dark themed interface
- Tab based navigation
- Status feedback messages

---

# Tech Used

- Python
- PySide6
- JSON
- QSS Styling

---

# Project Structure

```text
smart-sorter/
│
├── main.py
├── data/
│   └── settings.json
│
├── ui/
│   ├── main_window.py
│   └── styles.qss
│
├── utils/
│   ├── scanner.py
│   ├── mover.py
│   ├── category_manager.py
│   └── file_info.py
```

# How To Run

## Clone Repository

```bash
git clone https://github.com/Niva0106/smart-file-sorter
cd smart-sorter
```

## Create Virtual Environment

```bash
python3 -m venv venv
```

## Activate Virtual Environment

### Linux/macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install PySide6
```

## Run Application

```bash
python main.py
```

---

# Future Ideas

- Better duplicate handling
- Drag and drop support
- Automatic sorting after downloads
- Mobile version
- Better file previews

---

# License

Personal learning and utility project.
