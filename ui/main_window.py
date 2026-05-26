from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel,
    QLineEdit, QComboBox, QStackedWidget, QHBoxLayout,
    QFileDialog, QInputDialog,QTabWidget
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
        self.resize(1000, 650)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        self.title = QLabel("Smart Sorter")
        self.title.setObjectName("title")

        self.subtitle = QLabel("Organize your Downloads smartly")
        self.subtitle.setObjectName("subtitle")

        self.tabs = QTabWidget()

    # SORTER PAGE

        self.sorter_page = QWidget()

        self.sorter_layout = QVBoxLayout()
        self.sorter_layout.setSpacing(12)

        self.scan_button = QPushButton("Scan Downloads")
        self.scan_button.clicked.connect(self.load_files)

        self.sort_button = QPushButton("Sort Inside Downloads")
        self.sort_button.clicked.connect(self.sort_inside_downloads)

        self.sorter_layout.addWidget(self.scan_button)
        self.sorter_layout.addWidget(self.sort_button)
        self.sorter_layout.addStretch()

        self.sorter_page.setLayout(self.sorter_layout)

    # MOVER PAGE

        self.mover_page = QWidget()

        self.mover_layout = QVBoxLayout()
        self.mover_layout.setSpacing(12)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search files...")
        self.search_bar.textChanged.connect(self.filter_files)

        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.MultiSelection)
        self.file_list.setSpacing(4)
        self.file_list.setUniformItemSizes(True)

        self.dest_dropdown = QComboBox()

        self.move_button = QPushButton("Move Selected File(s)")
        self.move_button.setObjectName("primaryButton")
        self.move_button.clicked.connect(self.move_selected_file)

        self.add_dest_btn = QPushButton("Add")
        self.edit_dest_btn = QPushButton("Edit")
        self.delete_dest_btn = QPushButton("Delete")

        self.add_dest_btn.clicked.connect(self.add_destination)
        self.edit_dest_btn.clicked.connect(self.edit_destination)
        self.delete_dest_btn.clicked.connect(self.delete_destination)

        self.dest_buttons_layout = QHBoxLayout()
        self.dest_buttons_layout.setSpacing(10)

        self.dest_buttons_layout.addWidget(self.add_dest_btn)
        self.dest_buttons_layout.addWidget(self.edit_dest_btn)
        self.dest_buttons_layout.addWidget(self.delete_dest_btn)

        self.mover_layout.addWidget(self.search_bar)
        self.mover_layout.addWidget(self.file_list)
        self.mover_layout.addWidget(self.dest_dropdown)
        self.mover_layout.addWidget(self.move_button)
        self.mover_layout.addLayout(self.dest_buttons_layout)

        self.mover_page.setLayout(self.mover_layout)

        self.tabs.addTab(self.sorter_page, "Sorter")
        self.tabs.addTab(self.mover_page, "Mover")
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("statusLabel")

        # MAIN LAYOUT

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.subtitle)
        self.layout.addWidget(self.tabs)
        self.layout.addWidget(self.status_label)

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
        
        self.status_label.setText(f"{len(self.all_files)} files loaded")

    def filter_files(self, text):
        self.file_list.clear()

        for file in self.all_files:
            if text.lower() in file.name.lower():
                category = get_category(file)

                self.file_list.addItem(f"{file.name} → {category}")

    def sort_inside_downloads(self):
        files = scan_downloads()
        moved_count = 0

        downloads = Path.home() / "Downloads"

        for file in files:
            category = get_category(file)

            folder = downloads / category
            folder.mkdir(exist_ok=True)

            new_path = folder / file.name

            if not new_path.exists():
                file.rename(new_path)
                moved_count += 1

        self.load_files()
        
        self.status_label.setText(f"{moved_count} files sorted")

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

        name, ok = QInputDialog.getText(
            self,
            "Name",
            "Enter destination name:"
        )

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

        new_name, ok = QInputDialog.getText(
            self,
            "Edit Name",
            "New name:",
            text=old_name
        )

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
        
        moved_count = 0
        for item in selected:
            file_name = item.text().split(" → ")[0]

            for file in files:
                if file.name == file_name:
                    category = get_category(file)

                    move_file(
                        file,
                        category,
                        destination=destination
                    )
                    moved_count += 1
                    break

        self.load_files()
        self.status_label.setText(f"{moved_count} files moved")