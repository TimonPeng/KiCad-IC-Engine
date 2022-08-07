from PyQt6 import QtCore, QtGui, QtWidgets
from qasync import asyncSlot

from .api import SZLCSC


class Window(QtWidgets.QMainWindow):
    # search keyword
    keyword: QtWidgets.QLineEdit

    def __init__(self, settings: QtCore.QSettings) -> None:
        super().__init__()

        """
        global settings
        """
        self.settings = settings
        # search source
        source = SZLCSC
        self.source = source

        """
        window size
        """
        screen_size = self.screen().size()
        # default width is 2/3 of the screen width
        width = settings.value("UI/width", type=int, defaultValue=int(screen_size.width() / 3 * 2))
        # default width is 1/2 of the screen width
        height = settings.value("UI/height", type=int, defaultValue=int(screen_size.height() / 2))
        self.resize(width, height)

        """
        dialog
        """
        # about dialog
        about_dialog = Dialog("About")
        self.about_dialog = about_dialog

        """
        menu bar
        """
        menu_bar = self.menuBar()

        # file menu
        file_menu = menu_bar.addMenu("File")
        # settings will be merged when running on macOS
        # settings_action = file_menu.addAction("Settings")
        close_action = file_menu.addAction("Close")
        close_action.triggered.connect(self.close)  # type: ignore

        # help menu
        help_menu = menu_bar.addMenu("Help")
        # about will be merged when running on macOS
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about_dialog)  # type: ignore

        """
        main layout widget
        """
        main_widget = MainWidget(window=self)
        self.setCentralWidget(main_widget)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        new_size = event.size()

        width = new_size.width()
        height = new_size.height()

        self.settings.setValue("UI/width", width)
        self.settings.setValue("UI/height", height)

    def show_about_dialog(self):
        # text = (
        #     "<center>"
        #     f"<h1>{self.windowTitle()}</h1>"
        #     f"<p>PyQt {QtCore.PYQT_VERSION_STR}</p>"
        #     f"<p>Qt {QtCore.QT_VERSION_STR}</p>"
        #     "<p>Version 31.4.159.265358</p>"
        #     "</center>"
        # )
        # QtWidgets.QMessageBox.about(self, "About", text)
        self.about_dialog.show()


class Dialog(QtWidgets.QDialog):
    def __init__(self, title: str):
        super().__init__()

        self.setWindowTitle(title)
        # can't close main window until close dialog
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)


class HLayout(QtWidgets.QHBoxLayout):
    """left to right layout"""


class VLayout(QtWidgets.QVBoxLayout):
    """top to bottom layout"""


class MainWidget(QtWidgets.QWidget):
    def __init__(self, window: Window) -> None:
        super().__init__()

        # search layout
        search_layout = SearchLayout(window=window)

        # result layout
        result_layout = ResultLayout(window=window)

        # main layout
        main_layout = VLayout()
        main_layout.addLayout(search_layout)
        main_layout.addLayout(result_layout)

        self.setLayout(main_layout)


class SearchLayout(HLayout):
    def __init__(self, window: Window) -> None:
        super().__init__()

        self.window = window

        # search keyword
        keyword = QtWidgets.QLineEdit()
        window.keyword = keyword

        # search button
        search_button = QtWidgets.QPushButton("Search")
        search_button.clicked.connect(self.on_search_button_clicked)  # type: ignore

        # search layout
        self.addWidget(keyword)
        self.addWidget(search_button)

    @asyncSlot()
    async def on_search_button_clicked(self):
        keyword = self.window.keyword.text()
        if len(keyword) < 2:
            QtWidgets.QMessageBox.warning(self, "Error", "Keyword must be at least 2 characters")
            return

        results = await self.window.source.search(keyword)

        self.window.result_table.setModel(TableModel(headers=self.window.source.TABLE_HEADERS, rows=results))
        self.window.result_table.update()


class ResultLayout(HLayout):
    def __init__(self, window: Window) -> None:
        super().__init__()

        self.window = window

        # result model
        result_model = TableModel(headers=window.source.TABLE_HEADERS)

        # result table
        result_table = TableView(window=window)
        result_table.setModel(result_model)
        self.window.result_table = result_table  # type: ignore

        # result layout
        self.addWidget(result_table)


class TableView(QtWidgets.QTableView):
    def __init__(self, window: Window) -> None:
        super().__init__()

        # disable header hightlight
        self.horizontalHeader().setHighlightSections(False)
        # select full row
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        # disable edit row
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, headers={}, rows=[]) -> None:
        super().__init__()

        # display name -> key
        self.headers = headers
        self.header_keys = list(self.headers.keys())
        self.rows = rows

    def columnCount(self, parent):
        return len(self.headers)

    def rowCount(self, parent):
        return len(self.rows)

    def headerData(self, section, orientation, role):
        if role != QtCore.Qt.ItemDataRole.DisplayRole or orientation != QtCore.Qt.Orientation.Horizontal:
            return QtCore.QVariant()

        return self.header_keys[section]

    def data(self, index, role):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return QtCore.QVariant()

        row = self.rows[index.row()]
        header_display = self.header_keys[index.column()]
        header_key = self.headers.get(header_display)

        return row.get(header_key)
