##################################
# Common Minecraft Launcher      #
# CMCL Main,part of CMCL         #
# copyright PuqiAR@2024          #
# Licensed under the MIT License #
##################################

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

from sys import argv as application_args
from sys import exit as application_exit
import gc
#from os import path as osp
from ctypes import windll

from CMCL.CMCLib.RealPath import realpath
realpath.init(__file__)
from CMCL.CMCLib.RealPath import update_Paths
update_Paths()

from CMCL.CMCLib.Logger import logger
from CMCL.DevConf import *
from CMCL.CMCLib.Utils import os_is_dark_theme
from CMCL.Account.AccountController import *
from qfluentwidgets import Dialog,setThemeColor,setTheme,Theme

from qdarkstyle import load_stylesheet_pyqt5

if CMCL_DEV_MODE:
    logger.warning("CMCL2 is running in development mode,some functions are not working properly!")
else:
    logger.info("Welcome use CMCL2!")

from CMCL.CMCLib.SettingsController import Config
from CMCL.CMCLib.Variables import *


QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
QApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

windll.shell32.SetCurrentProcessExplicitAppUserModelID("CMCL2")

has_exception = False

app = QApplication(application_args)
from Asset.FluentIcons.FluentIconsEx import * 
"""
必须在引入MainWindow前,QApplication后引入 FluentIconEx
否则报错 'QPixmap: Must construct a QGuiApplication before a QPixmap'
因为在 FluentIconEx使用了QIcon
"""

#logger.info(f"dark theme:{os_is_dark_theme()}")

gc.enable()

with open(osp.join(realpath.get(),"Asset/DarkStyle.qss"),"r",encoding="utf-8") as f:
    DarkStyle = f.read()

if Config.themeMode == Theme.AUTO and os_is_dark_theme():
    logger.info("use dark theme(auto)")
    app.setStyleSheet(DarkStyle)
    setTheme(Theme.DARK)
    CMCL_USE_DARK_THEME = True
elif Config.theme == Theme.DARK:
    logger.info("use dark theme(manual)")
    app.setStyleSheet(DarkStyle)
    setTheme(Theme.DARK)
    CMCL_USE_DARK_THEME = True
else:
    setTheme(Theme.LIGHT)

setThemeColor(Config.themeColor.value)

from Pages.MainWindow import MainWindow

if CMCL_DEV_MODE:
    mainwindow = MainWindow()
    ret = app.exec()
    Config.save()
    AccountController.save_accounts()
    application_exit(ret)
else:
    try:
        mainwindow = MainWindow()
        application_exit(app.exec_())
    except Exception as e:
        logger.critical("Uncaught Exception,"+e.__str__())
        has_exception = True
        messageDialog = Dialog(
            "致命错误",
            "CMCL发生了致命错误:" + e.__str__() + "\n请将报错提交给CMCL开发者,谢谢",
            mainwindow
        )
        messageDialog.cancelButton.hide()
        messageDialog.buttonLayout.insertStretch(1)
        messageDialog.exec()
    finally:
        Config.save()
        AccountController.save_accounts()
        application_exit(0 if has_exception else -1)
