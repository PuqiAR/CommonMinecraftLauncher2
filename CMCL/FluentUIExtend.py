###################################
# Common Minecraft Launcher       #
# UI Extend module,part of CMCL   #
# copyright PuqiAR@2024           #
###################################
from qframelesswindow import StandardTitleBar
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QWidget

from CMCL.CMCLib.SettingsController import Config

from qfluentwidgets import (
    MessageBoxBase,
    ComboBox,
    SubtitleLabel,
    ProgressBar,
    LineEdit
)
class CustomTitleBar(StandardTitleBar):
    """ Custom title bar """

    def __init__(self, parent):
        super().__init__(parent)

        # customize the style of title bar button
        self.minBtn.setHoverColor(Qt.white)
        self.minBtn.setHoverBackgroundColor(QColor(0, 100, 182))
        self.minBtn.setPressedColor(Qt.white)
        self.minBtn.setPressedBackgroundColor(QColor(54, 57, 65))

        # use qss to customize title bar button
        self.maxBtn.setStyleSheet("""
            TitleBarButton {
                qproperty-hoverColor: white;
                qproperty-hoverBackgroundColor: rgb(0, 100, 182);
                qproperty-pressedColor: white;
                qproperty-pressedBackgroundColor: rgb(54, 57, 65);
            }
        """)

class ComboMessageBox(MessageBoxBase):
    def __init__(self, parent=None,title="",minWidth=300):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(title)
        self.comboBox = ComboBox()
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.comboBox)
        self.widget.setMinimumWidth(minWidth)
class LineEditMessageBox(MessageBoxBase):
    def __init__(self, parent=None,title="",minWidth=300):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(title)
        self.lineEdit = LineEdit()
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.lineEdit)
        self.widget.setMinimumWidth(minWidth)

class ProgressBarMessageBox(MessageBoxBase):
    def __init__(self, parent=None,title="",minWidth=300,userClosedCallBack=None):
        super().__init__(parent)
        self.cancelButton.hide()
        self.buttonLayout.insertStretch(1)

        self.titleLabel = SubtitleLabel(title)
        self.progressBar = ProgressBar()
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.progressBar)
        self.widget.setMinimumWidth(minWidth)
        self.yesButton.clicked.connect(self.__onYesButtonClicked)

        self.userClosedCallBack = userClosedCallBack
    def __onYesButtonClicked(self):
        self.user_closed()
    def user_closed(self):
        if self.userClosedCallBack:
            self.userClosedCallBack()
    def update_title(self,title:str):
        self.titleLabel.setText(title)
    def update_progress(self,value:int):
        self.progressBar.setValue(value)
    def Update(self,title,value):
        self.update_title(title)
        self.update_progress(value)

