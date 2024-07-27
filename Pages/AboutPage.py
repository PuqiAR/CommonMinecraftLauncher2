##################################
# Common Minecraft Launcher      #
# About Page,part of CMCL        #
# copyright PuqiAR@2024          #
# Licensed under the MIT License #
##################################

from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget

from qfluentwidgets import (FluentIcon)

from QtUi.Ui_AboutPage import Ui_Form as Ui_AboutPage

from CMCL.CMCLib.SettingsController import Config

ABOUT = """
Common Minecraft Launcher 是一个十分普通的Minecraft启动器
所有代码均由PuqiAR编写
由 PyQt5 和 PyQt5-Fluent-Widgets 驱动
该项目基于MIT协议发布，对源代码的分发、使用请遵循MIT License(https://github.com/PuqiAR/CommonMinecraftLauncher2/blob/main/LICENSE)

Bug反馈、建议等请加入官方QQ群
Copyright (c) 2024 PuqiAR
mailto: PuqiAR@qq.com
"""


class AboutPage(Ui_AboutPage,QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.label.setText(ABOUT)
        self.HyperlinkButton_OpenSite.url = "http://cmcl.top"
        self.HyperlinkButton_JoinGroup.url = "https://qm.qq.com/cgi-bin/qm/qr?k=9kinQ49GjncBngV2ORk8w53R0RNVTmEX&jump_from=webapi&authKey=iBPQ9ly/PdiPS9lLOQCNUQ1facfudivFzwovkHuU+/tFI+KG5PhWycDO9ssS6Uyf"
        self.TransparentPushButton_Github.setIcon(FluentIcon.GITHUB)
        self.TransparentPushButton_Github.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/PuqiAR/CommonMinecraftLauncher2")))