###################################
# Common Minecraft Launcher       #
# SettingsPage module,part of CMCL#
# copyright PuqiAR@2024           #
# Licensed under the MIT License  #
###################################

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget,QListWidgetItem,QHBoxLayout

from qfluentwidgets import (ExpandGroupSettingCard,
                            SettingCard,
                            LineEdit,
                            TeachingTipView,
                            PrimaryPushButton,
                            TeachingTip,
                            ComboBoxSettingCard,
                            RangeSettingCard,
                            InfoBar,
                            qconfig
                        )
from qfluentwidgets.common.icon import FluentIcon
from qfluentwidgets.components.widgets.teaching_tip import TeachingTipTailPosition

from QtUi.Ui_SettingsPage import Ui_Form as Ui_SettingsPage

from CMCL.CMCLib.Logger import logger
from CMCL.CMCLib.SettingsController import Config
from CMCL.CMCLib.RealPath import realpath,Paths
from CMCL.DevConf import *
from Asset.FluentIcons import FluentIconsEx

from sys import executable as application_executable
from sys import argv as application_argv
from os import execl
from os import path as osp


class LineEditSettingCard(SettingCard):
    def __init__(self, icon,title, content=None,ConfigValue = None):
        super().__init__(icon, title, content)
        self.lineEdit = LineEdit()
        self.hBoxLayout.addWidget(self.lineEdit)
        self.hBoxLayout.setContentsMargins(48, 12, 48, 12)
        self.lineEdit.setText(ConfigValue if Config else "")
    def bind_callback(self,callback):
        self.lineEdit.textChanged.connect(callback)
    def get_value(self):
        return self.lineEdit.text()

class LauncherSettings(ExpandGroupSettingCard):
    def __init__(self, parent=None,settingsChangedCallBack=None):
        super().__init__(FluentIcon.PLAY,"启动器设置","设置启动器配置",parent)
        self.windowTitleSettingCard = LineEditSettingCard(
            FluentIcon.TAG,
            "标题设置",
            "启动器窗口标题设置",
            ConfigValue=Config.LauncherWindowTitle.value
        )
        self.windowTitleSettingCard.lineEdit.setFixedWidth(200)
        self.addGroupWidget(self.windowTitleSettingCard)
        self.windowTitleSettingCard.bind_callback(lambda: self.callback())
        self.settingsChangedCallBack = settingsChangedCallBack
        
        self.windowSizeSettingsCard = LineEditSettingCard(
            FluentIconsEx.RESIZE,
            "窗口大小设置",
            "启动器窗口大小设置(长x宽)",
            ConfigValue=str(Config.WindowSize.value).replace('[','').replace(']','').replace(',','x').replace(' ','')
        )
        self.windowSizeSettingsCard.lineEdit.setFixedWidth(200)
        self.addGroupWidget(self.windowSizeSettingsCard)
        self.windowSizeSettingsCard.bind_callback(lambda: self.callback())

        self.themeSettingsCard = ComboBoxSettingCard(
            qconfig.themeMode,
            FluentIcon.PALETTE,
            "主题设置",
            "启动器主题设置(深色主题正在制作中)",
            texts=["浅色", "深色", "跟随系统设置"],
            parent=self
        )
        self.themeSettingsCard.setEnabled(False)
        self.addGroupWidget(self.themeSettingsCard)
        self.themeSettingsCard.comboBox.currentIndexChanged.connect(lambda:self.callback())

        self.splashScreenTimeSettingsCard = RangeSettingCard(
            Config.SplashScreenTime,
            FluentIcon.DATE_TIME,
            "启动屏幕时间设置",
            "设置启动器初始闪屏等待时长(ms)",
            parent=self
        )
        self.addGroupWidget(self.splashScreenTimeSettingsCard)
        self.splashScreenTimeSettingsCard.valueChanged.connect(lambda:self.callback())
    def callback(self):
        if self.settingsChangedCallBack:
            self.settingsChangedCallBack()
        self.save_settings()
    def save_settings(self):
       Config.LauncherWindowTitle.value=self.windowTitleSettingCard.get_value()
       temp = self.windowSizeSettingsCard.get_value().split('x')
       Config.WindowSize.value=[int(temp[0]),int(temp[1])]
    def add_widget(self,widget):
        w = QWidget()
        hbox = QHBoxLayout(w)
        hbox.addWidget(widget)
        self.addGroupWidget(w)


class SettingsPage(Ui_SettingsPage,QWidget):
    def __init__(self,parent) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.init_settings_options()
        self.PrimaryPushButton_Save.setHidden(True)
        self.PrimaryPushButton_Save.clicked.connect(lambda:self.save_config())
    def save_button_show(self):
        """
        显示保存按钮 (回调函数)
        """
        self.PrimaryPushButton_Save.setHidden(False)
    def save_config(self):
        self.PrimaryPushButton_Save.setHidden(True)
        logger.debug("Saving Config")
        Config.save()
        
        view = TeachingTipView(
            icon=FluentIcon.SYNC,
            title='重新启动CMCL2',
            content="重启CMCL以应用设置",
            isClosable=True,
            tailPosition=TeachingTipTailPosition.TOP_RIGHT,
        )
        button = PrimaryPushButton("重启")
        button.setFixedWidth(100)
        view.addWidget(button)
        self.restart_tt = TeachingTip.make(target=self,view=view,duration=-1,parent=self,tailPosition=TeachingTipTailPosition.TOP_RIGHT)
        button.clicked.connect(lambda:self.restart())
    def restart(self):
        self.restart_tt.close()
        if CMCL_DEV_MODE:
            InfoBar.error(
                "无法自动重启",
                "CMCL处于开发模式,无法自动重启,程序将在1.5秒后退出,请手动重启CMCL2",
                duration=1500,
                parent=self                             
            )
            QTimer.singleShot(1500,exit)
        else:
            execl([osp.join(Paths.LIBPATH,"Restarter.exe"),CMCL_DEV_PROCESS_NAME,CMCL_EXECUTABELE])
    def init_settings_options(self):
        self.cards = []
        self.cards_list_item = []
        self.launcher_settings_page = LauncherSettings(settingsChangedCallBack=lambda:self.save_button_show())
        self.cards.append(self.launcher_settings_page)
        for card in self.cards:
            item = QListWidgetItem(self.ListWidget)
            self.ListWidget.addItem(item)
            self.ListWidget.setItemWidget(item,card)