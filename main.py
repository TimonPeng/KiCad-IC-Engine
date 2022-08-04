import signal
import sys

from PyQt6.QtWidgets import QApplication

from src.config import Config
from src.gui import Window


def main() -> None:
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    title = "KiCad IC Engine"

    config = Config()

    app = QApplication(sys.argv)
    app.setApplicationName(title)
    app.setApplicationDisplayName(title)

    window = Window(config)
    window.setWindowTitle(title)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
