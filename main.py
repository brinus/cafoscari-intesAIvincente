from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QTextStream

from cafoscari_intesAIvincente.gui import MainWindow

import rc_styles

def main():
    app = QApplication([])

    style_file = QFile(":/styles/main.qss")
    if style_file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(style_file)
        app.setStyleSheet(stream.readAll())
        style_file.close()

    window = MainWindow()
    window.show()

    app.exec()

if __name__ == "__main__":
    main()
