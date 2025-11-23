from PySide6.QtStateMachine import QStateMachine, QState
from PySide6.QtCore import Signal

class StateMachine(QStateMachine):
    
    go_to_settings  = Signal()
    go_to_gamerules = Signal()
    go_to_gameplay  = Signal()
    go_to_main_menu = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__init_states()
        self.__init_transitions()

    def __init_states(self):
        self._state_main_menu   = QState(self)
        self._state_settings    = QState(self)
        self._state_gamerules   = QState(self)
        self._state_gameplay    = QState(self)

        self._state_main_menu.setObjectName("MainMenuState")
        self._state_settings.setObjectName("SettingsState")
        self._state_gamerules.setObjectName("GamerulesState")
        self._state_gameplay.setObjectName("GameplayState")

        self.setInitialState(self._state_main_menu)
    
    def __init_transitions(self):
        self._state_main_menu.addTransition(self.go_to_settings, self._state_settings)
        self._state_main_menu.addTransition(self.go_to_gamerules, self._state_gamerules)

        self._state_settings.addTransition(self.go_to_main_menu, self._state_main_menu)

        self._state_gamerules.addTransition(self.go_to_gameplay, self._state_gameplay)
        self._state_gamerules.addTransition(self.go_to_main_menu, self._state_main_menu)

        self._state_gameplay.addTransition(self.go_to_main_menu, self._state_main_menu)
        self._state_gameplay.addTransition(self.go_to_main_menu, self._state_main_menu)
        
    def start(self):
        super().start()

    @property
    def state_main_menu(self):
        return self._state_main_menu

    @property
    def state_settings(self):
        return self._state_settings
    
    @property
    def state_gamerules(self):
        return self._state_gamerules

    @property
    def state_gameplay(self):
        return self._state_gameplay