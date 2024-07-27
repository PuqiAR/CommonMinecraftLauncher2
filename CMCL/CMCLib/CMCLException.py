####################################
# Common Minecraft Launcher        #
# CMCLException module,part of CMCL#
# copyright PuqiAR@2024            #
####################################

class InternalException(Exception):
    def __init__(self, info:str) -> None:
        super().__init__(info)
        self.info = info
    def __str__(self):
        return "[Internal Exception]"+self.info