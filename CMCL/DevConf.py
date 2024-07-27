################################
# Common Minecraft Launcher    #
# DevConfig module,part of CMCL#
# copyright PuqiAR@2024        #
################################
from sys import executable
from os import path as osp

from CMCL.CMCLib.RealPath import Paths

CMCL_DEV_MODE = True

CMCL_DEV_MAIN_VERSION = "2.0.0"

CMCL_DEV_PROCESS_NAME = "CMCL.py" if CMCL_DEV_MODE else "CMCL.exe"

CMCL_CAN_AUTO_RESTART = False if CMCL_DEV_MODE else True

CMCL_EXECUTABELE = executable if CMCL_DEV_MODE else ""

CMCL_WINDOW_ICON = osp.join(Paths.ASSETPATH,"IconDev512.png" if CMCL_DEV_MODE else "Icon512.png")

CMCL_USE_DARK_THEME = False