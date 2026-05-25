from PySide6.QtWidgets import (QWidget,QVBoxLayout,QPushButton,QListWidget,QLabel,QLineEdit)
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

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search files...")
        self.search_bar.textChanged.connect(self.filter_files)

        self.scan_button = QPushButton("Scan Downloads")
        self.scan_button.clicked.connect(self.load_files)

        self.sort_button = QPushButton("Move Selected File")
        self.sort_button.clicked.connect(self.move_selected_file)

        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.MultiSelection)

        self.all_files = []

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.subtitle)
        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.scan_button)
        self.layout.addWidget(self.file_list)
        self.layout.addWidget(self.sort_button)

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

   
    def move_selected_file(self):
        selected_items = self.file_list.selectedItems()

        if not selected_items:
            return

        files = scan_downloads()

        for item in selected_items:
            file_name = item.text().split(" → ")[0]

            for file in files:
                if file.name == file_name:
                    category = get_category(file)
                    move_file(file, category, Path.home() / "Downloads")
                    break

        self.load_files()