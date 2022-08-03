from PyQt6.QtCore import PYQT_VERSION, QT_VERSION
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from config import Config


class Window(QMainWindow):
    def __init__(self, config: Config) -> None:
        super().__init__()

        # set the window size
        screen_size = self.screen().size()
        width = screen_size.width()
        height = screen_size.height()
        self.resize(1000, 800)
