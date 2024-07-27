##################################
# Common Minecraft Launcher      #
# Account Page,part of CMCL      #
# copyright PuqiAR@2024          #
# Licensed under the MIT License #
##################################

from PyQt5.QtWidgets import (
    QWidget,
    QListWidgetItem
)
from qfluentwidgets import (
    FluentIcon,
    ListWidget,
    BodyLabel
)

from QtUi.Ui_ManageAccount import Ui_Form as Ui_ManageAccount

from CMCL.CMCLib.Variables import *
from CMCL.CMCLib.SettingsController import Config


class AccountShowingPage(QWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self.listWidget = ListWidget(self)
    def add(self,widget,sizeHint=None):
        listItem = QListWidgetItem()
        if sizeHint:
            listItem.setSizeHint(sizeHint)
        self.listWidget.addItem(listItem)
        self.listWidget.setItemWidget(listItem,widget)

class EmptyAccountPage(QWidget):
    def __init__(self,parent,loginMethod):
        super().__init__(parent)
        self.label = BodyLabel(self)
        self.label.setText(f"额...你当前好像还没有{loginMethod}的账户")

class ManageAccountPage(Ui_ManageAccount,QWidget):
    def clear_stackedWidget(self):
        self.PopUpAniStackedWidget.removeWidget(self.PopUpAniStackedWidget.currentWidget())
    def init_pages(self):
        self.officialAccountPage = AccountShowingPage(self)
        self.offlineAccountPage = AccountShowingPage(self)
        self.thirdpartyAccountPage = AccountShowingPage(self)
        self.emptyAccountPage = EmptyAccountPage(self,constants.loginMethod.Official)

        self.PopUpAniStackedWidget.addWidget(self.emptyAccountPage)
        self.PopUpAniStackedWidget.addWidget(self.officialAccountPage)
        self.PopUpAniStackedWidget.addWidget(self.offlineAccountPage)
        self.PopUpAniStackedWidget.addWidget(self.thirdpartyAccountPage)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.clear_stackedWidget()
        self.init_pages()
        self.SegmentedWidget.addItem(
            constants.loginMethod.Official,
            "正版登录(MicrosoftLogin)",

        )