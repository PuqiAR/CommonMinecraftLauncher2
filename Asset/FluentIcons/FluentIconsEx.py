###################################
# Common Minecraft Launcher       #
# FluentIconEx module,part of CMCL#
# copyright PuqiAR@2024           #
# Licensed under the MIT License  #
###################################

from os import path as osp
from PyQt5.QtGui import QIcon

from CMCL.CMCLib.RealPath import Paths
from CMCL.CMCLib.SettingsController import Config


ICONS:list[QIcon] = []

RESIZE = QIcon(osp.join(Paths.ASSETICONSPATH,"FluentResize24Regular.png"))
MICROSOFT = QIcon(osp.join(Paths.ASSETICONSPATH,"MdiMicrosoft.png"))
OFFLINE_FILL = QIcon(osp.join(Paths.ASSETICONSPATH,"Offline_fill.png"))
THIRDPARTY = QIcon(osp.join(Paths.ASSETICONSPATH,"3rdparty.png"))

ICONS.append(RESIZE)