import asyncio
import signal
import sys

from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

from src.gui import Window
from src.version import name


def main() -> None:
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    settings = QSettings("config.ini", QSettings.Format.IniFormat)

    app = QApplication(sys.argv)
    app.setApplicationName(name)
    app.setApplicationDisplayName(name)

    window = Window(settings)
    window.setWindowTitle(name)
    window.show()

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    with loop:
        try:
            loop.run_forever()
        except asyncio.exceptions.CancelledError:
            pass


if __name__ == "__main__":
    main()
