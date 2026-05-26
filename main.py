from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
import sys


app = QApplication(sys.argv)

with open("ui/styles.qss", "r") as f:
    app.setStyleSheet(f.read())

window = MainWindow()
window.show()

sys.exit(app.exec())