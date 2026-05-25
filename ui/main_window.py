from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel,
    QLineEdit, QGroupBox, QComboBox
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

        # main layout
        self.layout = QVBoxLayout()

        self.title = QLabel("Smart Sorter")
        self.subtitle = QLabel("Organize your Downloads smartly")

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search files...")
        self.search_bar.textChanged.connect(self.filter_files)

        self.all_files = []

        #sorter section
        self.sorter_box = QGroupBox("Sorter")
        self.sorter_layout = QVBoxLayout()

        self.scan_button = QPushButton("Scan Downloads")
        self.scan_button.clicked.connect(self.load_files)

        self.sort_button = QPushButton("Sort Inside Downloads")
        self.sort_button.clicked.connect(self.sort_inside_downloads)

        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.MultiSelection)

        self.sorter_layout.addWidget(self.scan_button)
        self.sorter_layout.addWidget(self.sort_button)
        self.sorter_layout.addWidget(self.file_list)

        self.sorter_box.setLayout(self.sorter_layout)

        #mover section
        self.mover_box = QGroupBox("Mover")
        self.mover_layout = QVBoxLayout()

        self.dest_dropdown = QComboBox()
        self.load_destinations()

        self.move_button = QPushButton("Move Selected File(s)")
        self.move_button.clicked.connect(self.move_selected_file)

        self.mover_layout.addWidget(self.dest_dropdown)
        self.mover_layout.addWidget(self.move_button)

        self.mover_box.setLayout(self.mover_layout)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.subtitle)
        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.sorter_box)
        self.layout.addWidget(self.mover_box)

        self.setLayout(self.layout)

    def load_files(self):
        self.file_list.clear()

        self.all_files = scan_downloads()

        for file in self.all_files:
            info = get_file_info(file)
            category = get_category(file)

            self.file_list.addItem(f"{info['name']} → {category}")

    def filter_files(self, text):
        self.file_list.clear()

        for file in self.all_files:
            if text.lower() in file.name.lower():
                category = get_category(file)
                self.file_list.addItem(f"{file.name} → {category}")

    def sort_inside_downloads(self):
        files = scan_downloads()
        downloads = Path.home() / "Downloads"

        for file in files:
            category = get_category(file)

            category_folder = downloads / category
            category_folder.mkdir(exist_ok=True)

            new_path = category_folder / file.name

            if not new_path.exists():
                file.rename(new_path)

        self.load_files()

    def load_destinations(self):
        self.dest_dropdown.clear()

        try:
            with open("data/settings.json", "r") as f:
                data = json.load(f)

            for name in data:
                self.dest_dropdown.addItem(name)

        except FileNotFoundError:
            pass

    def move_selected_file(self):
        selected_items = self.file_list.selectedItems()

        if not selected_items:
            return

        try:
            with open("data/settings.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return

        dest_name = self.dest_dropdown.currentText()

        if dest_name not in data:
            return

        destination = Path(data[dest_name])

        files = scan_downloads()

        for item in selected_items:
            file_name = item.text().split(" → ")[0]

            for file in files:
                if file.name == file_name:
                    category = get_category(file)
                    move_file(file, category, destination)
                    break

        self.load_files()