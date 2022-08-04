from PyQt6 import QtCore, QtGui, QtWidgets

from .config import Config


class MainLayout(QtWidgets.QVBoxLayout):
    # top to bottom layout
    def __init__(self, window: QtWidgets.QWidget) -> None:
        super().__init__()

        # search layout
        search_layout = SearchLayout(window)
        self.addLayout(search_layout)

        result_layout = ResultLayout(window)
        self.addLayout(result_layout)
        # layout.addStretch(1)


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
        if len(self.keyword.text()) < 3:
            QtWidgets.QMessageBox.warning(self.window, "Error", "Keyword must be at least 3 characters")
            return


class ResultModel(QtCore.QAbstractTableModel):
    def __init__(self):
        super().__init__()

        self.headers = ["Scientist name", "Birthdate", "Contribution"]
        self.rows = [
            ("Newton", "1643-01-04", "Classical mechanics"),
            ("Einstein", "1879-03-14", "Relativity"),
            ("Darwin", "1809-02-12", "Evolution"),
        ]

    def rowCount(self, parent):
        return len(self.rows)

    def columnCount(self, parent):
        return len(self.headers)

    def data(self, index, role):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return QtCore.QVariant()
        return self.rows[index.row()][index.column()]

    def headerData(self, section, orientation, role):
        if role != QtCore.Qt.ItemDataRole.DisplayRole or orientation != QtCore.Qt.Orientation.Horizontal:
            return QtCore.QVariant()
        return self.headers[section]


class ResultLayout(QtWidgets.QHBoxLayout):
    # left to right layout
    def __init__(self, window: QtWidgets.QWidget) -> None:
        super().__init__()

        # parent window
        self.window = window

        view = QtWidgets.QTableView()
        result = ResultModel()
        view.setModel(result)

        self.addWidget(view)


class Window(QtWidgets.QWidget):
    def __init__(self, config: Config) -> None:
        super().__init__()

        self.config = config

        # set the window size
        screen_size = self.screen().size()
        # default width is 2/3 of the screen width
        width = config.width or int(screen_size.width() / 3 * 2)
        # default width is 1/2 of the screen width
        height = config.height or int(screen_size.height() / 2)
        self.resize(width, height)

        self.setLayout(MainLayout(self))

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        new_size = event.size()

        width = new_size.width()
        height = new_size.height()

        self.config.width = width
        self.config.height = height
        self.config.save()
