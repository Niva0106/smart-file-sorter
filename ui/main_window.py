from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel
from utils.scanner import scan_downloads
from utils.file_info import get_file_info
from utils.category_manager import get_category
from utils.mover import move_file
from pathlib import Path


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart Sorter")
        self.resize(800, 600)

        self.layout = QVBoxLayout()

        self.title = QLabel("Smart Sorter")
        self.subtitle = QLabel("Organize your Downloads smartly")

        self.scan_button = QPushButton("Scan Downloads")
        self.scan_button.clicked.connect(self.load_files)

        self.file_list = QListWidget()

        self.sort_button = QPushButton("Sort Files")
        self.sort_button.clicked.connect(self.sort_files)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.subtitle)
        self.layout.addWidget(self.scan_button)
        self.layout.addWidget(self.file_list)
        self.layout.addWidget(self.sort_button)


        self.setLayout(self.layout)
    
    def load_files(self):
        self.file_list.clear()

        files = scan_downloads()

        for file in files:
            info = get_file_info(file)
            category = get_category(file)

            self.file_list.addItem(f"{info['name']} → {category}")

    def sort_files(self):
        files = scan_downloads()
        destination = Path.home() / "Downloads"

        for file in files:
            category = get_category(file)
            move_file(file, category, destination)

        self.load_files()