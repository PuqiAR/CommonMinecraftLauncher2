################################
# Common Minecraft Launcher    #
# HomePage module,part of CMCL #
# copyright PuqiAR@2024        #
################################
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from QtUi.Ui_HomePage import Ui_Form as _HomePage

class HomePage(_HomePage,QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUi(self)