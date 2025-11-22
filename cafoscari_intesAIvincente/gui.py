from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt

from cafoscari_intesAIvincente.fsm import StateMachine

import rc_images
import rc_icons

class MainWindow(QMainWindow):

    __MAIN_WINDOW_TITLE         = "CaFoscari IntesAI Vincente"
    __MAIN_WINDOW_WIDTH         = 1280
    __MAIN_WINDOW_HEIGHT        = 720
    __MAIN_WINDOW_WIDTH_MIN     = 640
    __MAIN_WINDOW_HEIGHT_MIN    = 360

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

        self._icon_pixmap = QPixmap(":/icons/icon.ico")
        self.setWindowIcon(QIcon(self._icon_pixmap))

        self._btn_start_game = QPushButton("Start Game", self)
        self._btn_start_game.setMinimumSize(200, 50)
        
        self._btn_settings = QPushButton("Settings", self)
        self._btn_settings.setMinimumSize(200, 50)
        
        self._btn_exit = QPushButton("Exit", self)
        self._btn_exit.setMinimumSize(200, 50)
        self._btn_exit.clicked.connect(self.close)

        self._btn_back_from_settings = QPushButton("Back", self)
        self._btn_back_from_settings.setMinimumSize(200, 50)
        
        self._btn_back_from_gameplay = QPushButton("Back to Menu", self)
        self._btn_back_from_gameplay.setMinimumSize(200, 50)

        self._hide_all_buttons()

        self._fsm = StateMachine(self)
        self._fsm.state_main_menu.entered.connect(self.on_main_menu_entered)
        self._fsm.state_settings.entered.connect(self.on_settings_entered)
        self._fsm.state_gameplay.entered.connect(self.on_gameplay_entered)
        
        self._btn_start_game.clicked.connect(self._fsm.go_to_gameplay.emit)
        self._btn_settings.clicked.connect(self._fsm.go_to_settings.emit)
        self._btn_back_from_settings.clicked.connect(self._fsm.go_to_main_menu.emit)
        self._btn_back_from_gameplay.clicked.connect(self._fsm.go_to_main_menu.emit)
        
        self.update_background()
        
        self._fsm.start()

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
        
        self._position_buttons()
    
    def _hide_all_buttons(self):
        self._btn_start_game.hide()
        self._btn_settings.hide()
        self._btn_exit.hide()
        self._btn_back_from_settings.hide()
        self._btn_back_from_gameplay.hide()
    
    def _position_buttons(self):
        btn_width = 200
        btn_height = 50
        
        center_x = (self.width() - btn_width) // 2
        
        start_y = int(self.height() * 0.55)
        
        spacing = int(self.height() * 0.1)
        
        self._btn_start_game.move(center_x, start_y)
        self._btn_settings.move(center_x, start_y + spacing)
        self._btn_exit.move(center_x, start_y + spacing * 2)
        
        back_margin = 20
        back_x = back_margin
        back_y = self.height() - btn_height - back_margin
        self._btn_back_from_settings.move(back_x, back_y)
        self._btn_back_from_gameplay.move(back_x, back_y)

    def on_main_menu_entered(self):
        self._hide_all_buttons()
        self._btn_start_game.show()
        self._btn_settings.show()
        self._btn_exit.show()
        self._position_buttons()

    def on_settings_entered(self):
        self._hide_all_buttons()
        self._btn_back_from_settings.show()
        self._position_buttons()

    def on_gameplay_entered(self):
        self._hide_all_buttons()
        self._btn_back_from_gameplay.show()
        self._position_buttons()