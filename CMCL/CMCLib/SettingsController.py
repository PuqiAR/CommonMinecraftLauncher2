#############################################
# Common Minecraft Launcher                 #
# SettingsController module,part of CMCL    #
# copyright PuqiAR@2024                     #
# Licensed under the MIT License            #
#############################################
from json import loads,dumps
from dataclasses import dataclass
from os import path as osp

from CMCL.CMCLib.RealPath import realpath,Paths
from CMCL.CMCLib.Logger import logger


from qfluentwidgets import QConfig,ConfigItem,qconfig,RangeConfigItem,RangeValidator
SETTINGS_FILE_PATH = "Settings.json"
Settings = {}
SettingsLoaded = False


class SettingsController(QConfig):
    LauncherWindowTitle = ConfigItem("Launcher","WindowTitle","CMCL2",restart=True)
    WindowSize = ConfigItem("Launcher","WindowSize",[1000,600],restart=True)
    Menu_Sequence = ConfigItem("Launcher","Menu",["Home","Launch","Manage","Download","Settings"],restart=True)
    SplashScreenTime= RangeConfigItem("Launcher","SplashScreenTime",1.5,RangeValidator(0,3000),restart=True)

    AccountsPath = ConfigItem("Account","AccountsPath",osp.join(Paths.INTERNALPATH,"Account"),restart=True)

Config = SettingsController()

logger.debug(f"Settings file path:{osp.join(realpath.get(),'CMCL',SETTINGS_FILE_PATH)}")
qconfig.load(osp.join(realpath.get(),'CMCL',SETTINGS_FILE_PATH),Config)