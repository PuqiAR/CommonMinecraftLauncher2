###############################
# Common Minecraft Launcher   #
# RealPath module,part of CMCL#
# copyright PuqiAR@2024       #
###############################
from os import path as osp

from CMCL.CMCLib.CMCLException import InternalException
from dataclasses import dataclass

class RealPath:
    def __init__(self,main_file="") -> None:
        if (main_file!=""):
            self.realpath = osp.realpath(osp.dirname(main_file))
            self.inited = True
        else:
            self.inited = False
    def get(self) -> str:
        if not self.inited:
            raise InternalException("RealPath not inited")
        else:
            return self.realpath
    def init(self,main_file):
        if (self.inited):
            return
        self.realpath = osp.realpath(osp.dirname(main_file))
        self.inited = True

if __name__ != '__main__':
    realpath = RealPath()
else:
    raise InternalException("This module is not intended to be run directly")

@dataclass
class CMCLPaths:
    INTERNALPATH = osp.join("","CMCL")                 # CMCL
    LIBPATH = osp.join(INTERNALPATH,"CMCLib")          # CMCL/CMCLib
    LOGPATH = osp.join(INTERNALPATH,"Logs")            # CMCL/Logs
    ASSETPATH = osp.join("","Asset")
    ASSETICONSPATH = osp.join(ASSETPATH,"FluentIcons")

Paths = CMCLPaths()

def update_Paths():
    Paths.INTERNALPATH = osp.join(realpath.get(),"CMCL")
    Paths.LIBPATH = osp.join(Paths.INTERNALPATH,"CMCLib")
    Paths.LOGPATH = osp.join(Paths.INTERNALPATH,"Logs")
    Paths.ASSETPATH = osp.join(realpath.get(),"Asset")
    Paths.ASSETICONSPATH = osp.join(Paths.ASSETPATH,"FluentIcons")