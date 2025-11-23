import random
from PySide6.QtCore import QFile, QTextStream


class WordGenerator:
    
    def __init__(self, words_file: str = ":/data/words.txt"):
        self.words_file = words_file
        self._words = []
        self._load_words()
    
    def _load_words(self):
        file = QFile(self.words_file)
        
        if not file.open(QFile.ReadOnly | QFile.Text):
            raise FileNotFoundError(f"File parole non trovato: {self.words_file}")
        
        stream = QTextStream(file)
        content = stream.readAll()
        file.close()
        
        self._words = [word.strip() for word in content.split(',')]
        self._words = [word for word in self._words if word]
        
        if not self._words:
            raise ValueError("Il file parole è vuoto")
    
    def get_random_word(self) -> str:
        return random.choice(self._words)
    
    def get_total_words(self) -> int:
        return len(self._words)
    
    def word_exists(self, word: str) -> bool:
        return word.lower() in [w.lower() for w in self._words]
