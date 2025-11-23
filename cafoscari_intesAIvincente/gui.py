from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QWidget, QSizePolicy, QVBoxLayout, QStackedWidget
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QFile, QTextStream

from cafoscari_intesAIvincente.fsm import StateMachine

import rc_images
import rc_icons
import rc_styles

class MainWindow(QMainWindow):

    __MAIN_WINDOW_TITLE         = "CaFoscari IntesAI Vincente"
    __MAIN_WINDOW_WIDTH         = 1280
    __MAIN_WINDOW_HEIGHT        = 720
    
    @staticmethod
    def _load_stylesheet(path):
        """Carica uno stylesheet da Qt Resource"""
        file = QFile(path)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            file.close()
            return stylesheet
        return ""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.__MAIN_WINDOW_TITLE)
        self.setGeometry(100, 100, self.__MAIN_WINDOW_WIDTH, self.__MAIN_WINDOW_HEIGHT)
        self.setFixedSize(self.__MAIN_WINDOW_WIDTH, self.__MAIN_WINDOW_HEIGHT)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        self._background_label = QLabel(self)
        self._background_label.setScaledContents(True)
        self._background_label.setAlignment(Qt.AlignCenter)
        self._background_pixmap = QPixmap(":/images/background.png")
        self._background_label.setGeometry(0, 0, self.__MAIN_WINDOW_WIDTH, self.__MAIN_WINDOW_HEIGHT)
        self._background_label.setPixmap(self._background_pixmap.scaled(
            self.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        ))

        self._icon_pixmap = QPixmap(":/icons/icon.ico")
        self.setWindowIcon(QIcon(self._icon_pixmap))

        self._stacked_widget = QStackedWidget(self)
        self._stacked_widget.setGeometry(0, 0, self.__MAIN_WINDOW_WIDTH, self.__MAIN_WINDOW_HEIGHT)
        
        self._fsm = StateMachine(self)
        
        self._main_menu_widget  = self._create_main_menu_widget()
        self._settings_widget   = self._create_settings_widget()
        self._gamerules_widget  = self._create_gamerules_widget()
        self._gameplay_widget   = self._create_gameplay_widget()
        
        self._stacked_widget.addWidget(self._main_menu_widget)  # index 0
        self._stacked_widget.addWidget(self._settings_widget)   # index 1
        self._stacked_widget.addWidget(self._gamerules_widget)  # index 2
        self._stacked_widget.addWidget(self._gameplay_widget)   # index 3
        
        self._fsm.state_main_menu.entered.connect(self.on_main_menu_entered)
        self._fsm.state_settings.entered.connect(self.on_settings_entered)
        self._fsm.state_gamerules.entered.connect(self.on_gamerules_entered)
        self._fsm.state_gameplay.entered.connect(self.on_gameplay_entered)
        
        self._fsm.start()
    
    def _create_main_menu_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        
        btn_start = QPushButton("Start Game")
        btn_start.setObjectName("btnStartGame")
        btn_start.setMinimumSize(200, 50)
        btn_start.clicked.connect(self._fsm.go_to_gamerules.emit)
        
        btn_settings = QPushButton("Settings")
        btn_settings.setObjectName("btnSettings")
        btn_settings.setMinimumSize(200, 50)
        btn_settings.clicked.connect(self._fsm.go_to_settings.emit)
        
        btn_exit = QPushButton("Exit")
        btn_exit.setObjectName("btnExit")
        btn_exit.setMinimumSize(200, 50)
        btn_exit.clicked.connect(self.close)
        
        layout.addWidget(btn_start)
        layout.addWidget(btn_settings)
        layout.addWidget(btn_exit)
        
        return widget
    
    def _create_settings_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        layout.setContentsMargins(20, 20, 20, 20)
        
        btn_back = QPushButton("Back")
        btn_back.setObjectName("btnBack")
        btn_back.setMinimumSize(120, 50)
        btn_back.clicked.connect(self._fsm.go_to_main_menu.emit)
        
        layout.addWidget(btn_back)
        
        return widget
    
    def _create_gamerules_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        
        container = QWidget()
        container.setObjectName("whiteContainer")
        container.setStyleSheet(self._load_stylesheet(":/styles/container.qss"))
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(20)
        container_layout.setAlignment(Qt.AlignCenter)
        
        label_rules = QLabel("La parola segreta verrà mostrata in alto. Per comporre la frase indizio inserisci una parola nell'apposito spazio e inviala. L'AI aggiungerà la sua. Continuate a turno finché il compagno indovina.")
        label_rules.setAlignment(Qt.AlignCenter)
        label_rules.setWordWrap(True)
        label_rules.setFixedWidth(600)
        label_rules.setStyleSheet("color: #333; font-size: 16px;")

        btn_start_gameplay = QPushButton("Start Playing")
        btn_start_gameplay.setObjectName("btnStartGame")
        btn_start_gameplay.setFixedSize(200, 50)
        btn_start_gameplay.clicked.connect(self._fsm.go_to_gameplay.emit)
        
        btn_back = QPushButton("Back")
        btn_back.setObjectName("btnBack")
        btn_back.setFixedSize(200, 50)
        btn_back.clicked.connect(self._fsm.go_to_main_menu.emit)
        
        container_layout.addWidget(label_rules)
        container_layout.addWidget(btn_start_gameplay)
        container_layout.addWidget(btn_back)
        
        layout.addWidget(container)
        
        return widget
    
    def _create_gameplay_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        
        container = QWidget()
        container.setObjectName("whiteContainer")
        container.setStyleSheet(self._load_stylesheet(":/styles/container.qss"))
        container_layout = QVBoxLayout(container)
        container.setFixedSize(800, 500)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(20)
        
        # WIDGETS' GAMEPLAY HERE
        
        btn_back = QPushButton("Back to Menu")
        btn_back.setObjectName("btnBack")
        btn_back.setMinimumSize(120, 50)
        btn_back.clicked.connect(self._fsm.go_to_main_menu.emit)
        
        container_layout.addStretch()
        container_layout.addWidget(btn_back, alignment=Qt.AlignLeft)
        
        layout.addWidget(container)
        
        return widget

    def on_main_menu_entered(self):
        self._stacked_widget.setCurrentIndex(0)

    def on_settings_entered(self):
        self._stacked_widget.setCurrentIndex(1)
    
    def on_gamerules_entered(self):
        self._stacked_widget.setCurrentIndex(2)

    def on_gameplay_entered(self):
        self._stacked_widget.setCurrentIndex(3)