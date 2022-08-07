import easyeda2kicad
from PyQt6 import QtCore, QtGui, QtWidgets
from qasync import asyncSlot

from .api import SZLCSC


class Window(QtWidgets.QMainWindow):
    def __init__(self, settings: QtCore.QSettings) -> None:
        super().__init__()

        """
        global settings
        """
        self.settings = settings

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
        menu bar
        """
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

        """
        search source
        """
        source = SZLCSC
        self.source = source

        """
        layout
        """
        # search keyword
        keyword = QtWidgets.QLineEdit()
        self.keyword = keyword

        # search button
        search_button = QtWidgets.QPushButton("Search")
        search_button.clicked.connect(self.on_search_button_clicked)

        # search layout
        search_layout = QtWidgets.QHBoxLayout()
        search_layout.addWidget(keyword)
        search_layout.addWidget(search_button)

        # result model
        result_model = ResultModel(headers=source.TABLE_HEADERS)

        # result table
        # result_table = QtWidgets.QTableWidget()
        result_table = QtWidgets.QTableView()
        self.result_table = result_table
        # disable header hightlight
        result_table.horizontalHeader().setHighlightSections(False)
        # select full row
        result_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        # disable edit row
        result_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        result_table.setModel(result_model)

        # result layout
        result_layout = QtWidgets.QHBoxLayout()
        result_layout.addWidget(result_table)

        # main layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(search_layout)
        main_layout.addLayout(result_layout)

        # main widget
        main_widget = QtWidgets.QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        new_size = event.size()

        width = new_size.width()
        height = new_size.height()

        self.settings.setValue("UI/width", width)
        self.settings.setValue("UI/height", height)

    @asyncSlot()
    async def on_search_button_clicked(self):
        keyword = self.keyword.text()
        if len(keyword) < 2:
            QtWidgets.QMessageBox.warning(self, "Error", "Keyword must be at least 2 characters")
            return

        results = await self.source.search(keyword)

        self.result_table.setModel(ResultModel(headers=self.source.TABLE_HEADERS, rows=results))
        self.result_table.update()

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


class ResultModel(QtCore.QAbstractTableModel):
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
