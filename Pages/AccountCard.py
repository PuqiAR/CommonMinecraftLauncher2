##################################
# Common Minecraft Launcher      #
# Account Card,part of CMCL      #
# copyright PuqiAR@2024          #
# Licensed under the MIT License #
##################################

from QtUi.Ui_AccountCard import Ui_Form as Ui_AccountCard

from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore

from CMCL.CMCLib.Variables import *
from CMCL.Account.CMCLAccounts import *


from CMCL.CMCLib.Utils import *

class AccountCard(Ui_AccountCard,QWidget):
    def __init__(self,parent,Account:MCAccount):
        super().__init__(parent)
        self.setupUi(self)
        self.Account = Account
        self.BodyLabel_Name.setText(Account.Name)
        self.CaptionLabel.setText(AccountLoginMethod(Account))
        self.refreshPixmap()
    def getProfile(self):
        self.profile = Skin.getProfile(self.Account.Name)
    def setProfile(self):
        img = bytesToPixmap(self.profile)
        self.ImageLabel.setScaledContents(True)
        img = img.scaled(self.ImageLabel.width(), self.ImageLabel.height(), aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        self.ImageLabel.setImage(img)
    def refreshPixmap(self):
        self.th=Thread(self,lambda:self.getProfile())
        self.th.finished.connect(lambda:self.setProfile())
        self.th.start()

        
