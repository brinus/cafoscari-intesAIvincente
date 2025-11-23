"""
Dialog per mostrare il countdown quando si raggiunge il rate limit
"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont


class RateLimitDialog(QDialog):
    """Dialog modale che mostra un countdown per il rate limit"""
    
    def __init__(self, seconds: int, parent=None):
        super().__init__(parent)
        self.seconds_remaining = seconds
        self.setWindowTitle("Rate Limit Raggiunto")
        self.setModal(True)
        self.setFixedSize(500, 300)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(30)
        layout.setContentsMargins(40, 40, 40, 40)
        
        title_label = QLabel("Troppe richieste!")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        message_label = QLabel("Hai raggiunto il limite di richieste.\nAttendi prima di continuare.")
        message_font = QFont()
        message_font.setPointSize(14)
        message_label.setFont(message_font)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setWordWrap(True)
        layout.addWidget(message_label)
        
        self.countdown_label = QLabel(f"{seconds} secondi")
        countdown_font = QFont()
        countdown_font.setPointSize(32)
        countdown_font.setBold(True)
        self.countdown_label.setFont(countdown_font)
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet("color: #FF6B6B;")
        layout.addWidget(self.countdown_label)
        
        self.close_button = QPushButton("Chiudi")
        self.close_button.setMinimumHeight(50)
        self.close_button.setEnabled(False)
        self.close_button.clicked.connect(self.accept)
        layout.addWidget(self.close_button)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_countdown)
        self.timer.start(1000)
        
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #666666;
            }
            QPushButton:hover:enabled {
                background-color: #66BB6A;
            }
        """)
    
    def _update_countdown(self):
        """Aggiorna il countdown ogni secondo"""
        self.seconds_remaining -= 1
        
        if self.seconds_remaining > 0:
            self.countdown_label.setText(f"{self.seconds_remaining} secondi")
        else:
            self.countdown_label.setText("Pronto!")
            self.countdown_label.setStyleSheet("color: #4CAF50;")
            self.close_button.setEnabled(True)
            self.timer.stop()
            
            QTimer.singleShot(1000, self.accept)
