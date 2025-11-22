from PySide6.QtWidgets import QMainWindow, QLabel
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt

import rc_images
import rc_icons

class MainWindow(QMainWindow):

    __MAIN_WINDOW_TITLE = "CaFoscari IntesAI Vincente"
    __MAIN_WINDOW_WIDTH = 1280
    __MAIN_WINDOW_HEIGHT = 720
    __MAIN_WINDOW_WIDTH_MIN = 640
    __MAIN_WINDOW_HEIGHT_MIN = 360

    __ASPECT_RATIO = __MAIN_WINDOW_WIDTH / __MAIN_WINDOW_HEIGHT

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.__MAIN_WINDOW_TITLE)
        self.setGeometry(100, 100, self.__MAIN_WINDOW_WIDTH, self.__MAIN_WINDOW_HEIGHT)
        
        self.setMinimumSize(self.__MAIN_WINDOW_WIDTH_MIN, self.__MAIN_WINDOW_HEIGHT_MIN)
        
        self._background_label = QLabel(self)
        self._background_label.setScaledContents(True)
        self._background_label.setAlignment(Qt.AlignCenter)

        self._background_pixmap = QPixmap(":/images/background.png")
        self.update_background()

        self._icon_pixmap = QPixmap(":/icons/icon.ico")
        self.setWindowIcon(QIcon(self._icon_pixmap))

    def resizeEvent(self, event):
        super().resizeEvent(event)

        new_width = event.size().width()
        new_height = int(new_width / self.__ASPECT_RATIO)
        if new_height > event.size().height():
            new_height = event.size().height()
            new_width = int(new_height * self.__ASPECT_RATIO)

        self.resize(new_width, new_height)
        self.update_background()
    
    def update_background(self):
        self._background_label.setGeometry(self.rect())
        scaled_pixmap = self._background_pixmap.scaled(
            self.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        self._background_label.setPixmap(scaled_pixmap)