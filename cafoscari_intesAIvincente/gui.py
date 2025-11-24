from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QWidget, QSizePolicy, QVBoxLayout, QStackedWidget, QLineEdit, QGridLayout, QMessageBox, QTextEdit, QComboBox, QHBoxLayout
from PySide6.QtGui import QIcon, QPixmap, QRegularExpressionValidator
from PySide6.QtCore import Qt, QFile, QTextStream, QRegularExpression, QTimer
from PySide6.QtTextToSpeech import QTextToSpeech
from PySide6.QtCore import QLocale

from cafoscari_intesAIvincente.fsm import StateMachine
from cafoscari_intesAIvincente.api.ai_client import AIClient, RateLimitError
from cafoscari_intesAIvincente.word_generator import WordGenerator
from cafoscari_intesAIvincente.rate_limit_dialog import RateLimitDialog

import rc_images
import rc_icons
import rc_styles
import rc_data

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
        
        self._word_generator = WordGenerator()
        self._ai_client = AIClient("AIzaSyAmFz8g-tJDFL4h1ByIcN0vB3N0aSMFTgc")
        
        self._tts = QTextToSpeech(self)
        for locale in self._tts.availableLocales():
            if locale.language() == QLocale.Language.Italian:
                self._tts.setLocale(locale)
                break

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
        
        self._logo_label = QLabel(self)
        logo_pixmap = QPixmap(":/images/testa.png")
        scaled_logo = logo_pixmap.scaledToHeight(300, Qt.SmoothTransformation)
        self._logo_label.setPixmap(scaled_logo)
        logo_x = (self.__MAIN_WINDOW_WIDTH - scaled_logo.width()) // 2
        self._logo_label.setGeometry(logo_x, 0, scaled_logo.width(), scaled_logo.height())
        self._logo_label.raise_()
        
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
        
        layout.addStretch(3)
        layout.addWidget(btn_start)
        layout.addWidget(btn_settings)
        layout.addWidget(btn_exit)
        layout.addStretch(1)
        
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
        container_layout = QGridLayout(container)
        container.setFixedSize(800, 400)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(20)

        self.__init_game_variables()

        sequence_label = QLabel("Sequenza corrente:")
        sequence_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self._ql_sequence_display = QTextEdit()
        self._ql_sequence_display.setReadOnly(True)
        self._ql_sequence_display.setFixedHeight(80)
        self._ql_sequence_display.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._ql_sequence_display.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._ql_sequence_display.setLineWrapMode(QTextEdit.WidgetWidth)
        self._ql_sequence_display.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                color: #333;
            }
        """)

        self._ql_target_word = QLabel("Parola segreta: ")
        self._ql_target_word.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._ql_target_word.setFixedHeight(30)

        self._line_edit_input = QLineEdit()
        self._line_edit_input.setPlaceholderText("Inserisci la tua parola...")
        self._line_edit_input.setFixedSize(400, 50)
        
        regex = QRegularExpression("^[a-zA-ZàèéìòùÀÈÉÌÒÙ]+$")
        validator = QRegularExpressionValidator(regex)
        self._line_edit_input.setValidator(validator)

        self._line_edit_input.returnPressed.connect(self.on_user_input)

        btn_yes = QPushButton("Yes")
        btn_yes.setObjectName("btnYes")
        btn_yes.setFixedSize(80, 50)
        btn_yes.clicked.connect(self.on_yes_clicked)
        
        btn_no = QPushButton("No")
        btn_no.setObjectName("btnNo")
        btn_no.setFixedSize(80, 50)
        btn_no.clicked.connect(self.on_no_clicked)

        self._ql_score = QLabel(f"Score: {self._score}")
        self._ql_score.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._ql_score.setFixedSize(100, 30)

        btn_back = QPushButton("Back to Menu")
        btn_back.setObjectName("btnBack")
        btn_back.setMinimumSize(120, 50)
        btn_back.clicked.connect(self._fsm.go_to_main_menu.emit)
        
        container_layout.addWidget(sequence_label, 0, 0, 1, 3)
        container_layout.addWidget(self._ql_sequence_display, 1, 0, 1, 3)
        container_layout.addWidget(self._ql_target_word, 2, 0, 1, 3)
        container_layout.addWidget(self._line_edit_input, 3, 0, alignment=Qt.AlignCenter)
        container_layout.addWidget(btn_yes, 3, 1, alignment=Qt.AlignCenter)
        container_layout.addWidget(btn_no, 3, 2, alignment=Qt.AlignCenter)
        container_layout.addWidget(self._ql_score, 4, 0, alignment=Qt.AlignLeft)
        container_layout.addWidget(btn_back, 4, 2, alignment=Qt.AlignRight)

        layout.addWidget(container)
        
        return widget

    def on_main_menu_entered(self):
        self._stacked_widget.setCurrentIndex(0)

    def on_settings_entered(self):
        self._stacked_widget.setCurrentIndex(1)
    
    def on_gamerules_entered(self):
        self._stacked_widget.setCurrentIndex(2)

    def on_gameplay_entered(self):
        self.__init_game_variables()
        self.__generate_new_target_word()
        self.__update_game_ui()
        self._stacked_widget.setCurrentIndex(3)

    def __init_game_variables(self):
        self._score     = 0
        self._sequence  = []
        self._target    = ""
    
    def __generate_new_target_word(self):
        self._target = self._word_generator.get_random_word()
    
    def __update_game_ui(self):
        self._ql_score.setText(f"Score: {self._score}")
        sequence_text = ' '.join(self._sequence)
        self._ql_sequence_display.setPlainText(sequence_text)
        self._ql_target_word.setText(f"Parola segreta: {self._target}")

    def on_yes_clicked(self):
        self._score += 1
        self._sequence = []
        self._ql_score.setText(f"Score: {self._score}")
        self.__generate_new_target_word()
        self.__update_game_ui()

    def on_no_clicked(self):
        self._score = max(0, self._score - 1)
        self._sequence = []
        self._ql_score.setText(f"Score: {self._score}")
        self.__generate_new_target_word()
        self.__update_game_ui()

    def on_user_input(self):
        user_word = self._line_edit_input.text().strip()
        if not user_word:
            return
        
        self._sequence.append(user_word)
        self.__update_game_ui()
        self._line_edit_input.clear()
        self._line_edit_input.setStyleSheet("background-color: #d4edda;")
        QTimer.singleShot(200, lambda: self._line_edit_input.setStyleSheet(":/styles/main.qss"))

        self._line_edit_input.setEnabled(False)
        QTimer.singleShot(100, self.__process_ai_response)


    def __process_ai_response(self):
        try:
            ai_word = self._ai_client.generate_word(self._target, self._sequence)
            self._sequence.append(ai_word)
            self.__update_game_ui()
            
            self._tts.say(ai_word)
            
        except RateLimitError as e:
            dialog = RateLimitDialog(e.retry_after, self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Errore API",
                f"Errore durante la generazione della parola AI:\n{str(e)}"
            )
        finally:
            self._line_edit_input.setEnabled(True)
            self._line_edit_input.setFocus()
