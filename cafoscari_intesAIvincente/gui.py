from PySide6.QtWidgets import QMainWindow

class MainWindow(QMainWindow):

    __MAIN_WINDOW_TITLE = "CaFoscari IntesAI Vincente"
    __MAIN_WINDOW_WIDTH = 800
    __MAIN_WINDOW_HEIGHT = 600

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.__MAIN_WINDOW_TITLE)
        self.setGeometry(100, 100, self.__MAIN_WINDOW_WIDTH, self.__MAIN_WINDOW_HEIGHT)