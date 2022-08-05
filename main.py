import signal
import sys

from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QApplication

from src.gui import Window


def main() -> None:
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    title = "KiCad IC Engine"

    app = QApplication(sys.argv)
    app.setApplicationName(title)
    app.setApplicationDisplayName(title)

    settings = QSettings("config.ini", QSettings.Format.IniFormat)

    window = Window(settings)
    window.setWindowTitle(title)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
