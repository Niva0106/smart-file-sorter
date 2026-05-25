from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel,
    QLineEdit, QComboBox, QStackedWidget, QHBoxLayout,
    QFileDialog, QInputDialog, QMessageBox
)

import json
from utils.scanner import scan_downloads
from utils.file_info import get_file_info
from utils.category_manager import get_category
from utils.mover import move_file
from pathlib import Path


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart Sorter")

        self.layout = QVBoxLayout()

        self.title = QLabel("Smart Sorter")
        self.subtitle = QLabel("Organize your Downloads smartly")

        self.nav_layout = QHBoxLayout()

        self.sorter_btn = QPushButton("Sorter")
        self.mover_btn = QPushButton("Mover")

        self.nav_layout.addWidget(self.sorter_btn)
        self.nav_layout.addWidget(self.mover_btn)

        self.pages = QStackedWidget()
#sorter page
        self.sorter_page = QWidget()
        self.sorter_layout = QVBoxLayout()

        self.scan_button = QPushButton("Scan Downloads")
        self.scan_button.clicked.connect(self.load_files)

        self.sort_button = QPushButton("Sort Inside Downloads")
        self.sort_button.clicked.connect(self.sort_inside_downloads)

        self.sorter_layout.addWidget(self.scan_button)
        self.sorter_layout.addWidget(self.sort_button)

        self.sorter_page.setLayout(self.sorter_layout)
#mover page
        self.mover_page = QWidget()
        self.mover_layout = QVBoxLayout()

        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.MultiSelection)

        self.dest_dropdown = QComboBox()

        self.move_button = QPushButton("Move Selected File(s)")
        self.move_button.clicked.connect(self.move_selected_file)

        self.add_dest_btn = QPushButton("Add Destination")
        self.add_dest_btn.clicked.connect(self.add_destination)

        self.edit_dest_btn = QPushButton("Edit Destination")
        self.edit_dest_btn.clicked.connect(self.edit_destination)

        self.delete_dest_btn = QPushButton("Delete Destination")
        self.delete_dest_btn.clicked.connect(self.delete_destination)

        self.mover_layout.addWidget(self.file_list)
        self.mover_layout.addWidget(self.dest_dropdown)
        self.mover_layout.addWidget(self.move_button)
        self.mover_layout.addWidget(self.add_dest_btn)
        self.mover_layout.addWidget(self.edit_dest_btn)
        self.mover_layout.addWidget(self.delete_dest_btn)

        self.mover_page.setLayout(self.mover_layout)

        self.pages.addWidget(self.sorter_page)
        self.pages.addWidget(self.mover_page)

        self.sorter_btn.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.mover_btn.clicked.connect(lambda: self.pages.setCurrentIndex(1))

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.subtitle)
        self.layout.addLayout(self.nav_layout)
        self.layout.addWidget(self.pages)

        self.setLayout(self.layout)

        self.all_files = []
        self.load_destinations()
        self.load_files()

    def load_files(self):
        self.file_list.clear()
        self.all_files = scan_downloads()

        for file in self.all_files:
            info = get_file_info(file)
            category = get_category(file)
            self.file_list.addItem(f"{info['name']} → {category}")

    def sort_inside_downloads(self):
        files = scan_downloads()
        downloads = Path.home() / "Downloads"

        for file in files:
            category = get_category(file)

            folder = downloads / category
            folder.mkdir(exist_ok=True)

            new_path = folder / file.name

            if not new_path.exists():
                file.rename(new_path)

        self.load_files()

    def load_destinations(self):
        self.dest_dropdown.clear()

        data = self.read_json()

        for name in data:
            self.dest_dropdown.addItem(name)

    def read_json(self):
        try:
            with open("data/settings.json", "r") as f:
                content = f.read().strip()
                return json.loads(content) if content else {}
        except:
            return {}

    def write_json(self, data):
        Path("data").mkdir(exist_ok=True)
        with open("data/settings.json", "w") as f:
            json.dump(data, f, indent=4)

    def add_destination(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if not folder:
            return

        name, ok = QInputDialog.getText(self, "Name", "Enter destination name:")
        if not ok or not name:
            return

        data = self.read_json()
        data[name] = folder
        self.write_json(data)
        self.load_destinations()

    def edit_destination(self):
        old_name = self.dest_dropdown.currentText()
        if not old_name:
            return

        data = self.read_json()
        if old_name not in data:
            return

        new_name, ok = QInputDialog.getText(self, "Edit Name", "New name:", text=old_name)
        if not ok or not new_name:
            return

        data[new_name] = data.pop(old_name)
        self.write_json(data)
        self.load_destinations()

    def delete_destination(self):
        name = self.dest_dropdown.currentText()
        if not name:
            return

        data = self.read_json()

        if name in data:
            del data[name]
            self.write_json(data)

        self.load_destinations()

    def move_selected_file(self):
        selected = self.file_list.selectedItems()
        if not selected:
            return

        data = self.read_json()

        dest_name = self.dest_dropdown.currentText()
        if dest_name not in data:
            return

        destination = Path(data[dest_name])

        files = scan_downloads()

        for item in selected:
            file_name = item.text().split(" → ")[0]

            for file in files:
                if file.name == file_name:
                    category = get_category(file)
                    move_file(file, category, destination=destination)
                    break
        
        print("DESTINATION:", destination)
        print("FILE:", file)
        self.load_files()