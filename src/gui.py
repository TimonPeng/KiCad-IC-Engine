import easyeda2kicad
from PyQt6 import QtCore, QtGui, QtWidgets


class MainLayout(QtWidgets.QWidget):
    def __init__(self, window: QtWidgets.QWidget) -> None:
        super().__init__()

        # top to bottom layout
        layout = QtWidgets.QVBoxLayout()

        # search layout
        search_layout = SearchLayout(window)
        layout.addLayout(search_layout)

        # results layout
        result_layout = ResultLayout(window)
        layout.addLayout(result_layout)

        # layout.addStretch(1)

        self.setLayout(layout)


class SearchLayout(QtWidgets.QHBoxLayout):
    # left to right layout
    def __init__(self, window: QtWidgets.QWidget) -> None:
        super().__init__()

        # parent window
        self.window = window

        # search keyword
        self.keyword = QtWidgets.QLineEdit()
        self.addWidget(self.keyword)
        # search button
        button = QtWidgets.QPushButton("Search")
        button.clicked.connect(self.on_button_clicked)
        self.addWidget(button)

    def on_button_clicked(self):
        if len(self.keyword.text()) < 2:
            QtWidgets.QMessageBox.warning(self.window, "Error", "Keyword must be at least 2 characters")
            return


class ResultLayout(QtWidgets.QHBoxLayout):
    # left to right layout
    def __init__(self, window: QtWidgets.QWidget) -> None:
        super().__init__()

        table = ResultTable(window)
        self.addWidget(table)


# QTableView or QTableWidget?
class ResultTable(QtWidgets.QTableWidget):
    def __init__(self, window: QtWidgets.QWidget) -> None:
        super().__init__()

        titles = ["Device", "Footprint", "Symbol", "Value", "Supplier Part", "Manufacturer"]
        # must set column count first
        self.setColumnCount(len(titles))
        self.setHorizontalHeaderLabels(titles)

        # select full row
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        # can't edit
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)


class Window(QtWidgets.QMainWindow):
    def __init__(self, settings: QtCore.QSettings) -> None:
        super().__init__()

        self.settings = settings

        # set the window size
        screen_size = self.screen().size()
        # default width is 2/3 of the screen width
        width = settings.value("UI/width", type=int, defaultValue=int(screen_size.width() / 3 * 2))
        # default width is 1/2 of the screen width
        height = settings.value("UI/height", type=int, defaultValue=int(screen_size.height() / 2))
        self.resize(width, height)

        # set menu bar
        menu_bar = self.menuBar()
        # file menu
        file_menu = menu_bar.addMenu("File")
        # settings will be merged when running on macOS
        settings_action = file_menu.addAction("Settings")
        close_action = file_menu.addAction("Close")
        close_action.triggered.connect(self.close)
        # help menu
        help_menu = menu_bar.addMenu("Help")
        # about will be merged when running on macOS
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about_dialog)

        # main layout
        self.setCentralWidget(MainLayout(self))

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        new_size = event.size()

        width = new_size.width()
        height = new_size.height()

        self.settings.setValue("UI/width", width)
        self.settings.setValue("UI/height", height)

    def show_about_dialog(self):
        text = (
            "<center>"
            f"<h1>{self.windowTitle()}</h1>"
            f"<p>PyQt {QtCore.PYQT_VERSION_STR}</p>"
            f"<p>Qt {QtCore.QT_VERSION_STR}</p>"
            "<p>Version 31.4.159.265358</p>"
            "</center>"
        )
        QtWidgets.QMessageBox.about(self, "About", text)
