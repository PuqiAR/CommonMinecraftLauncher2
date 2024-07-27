##################################
# Common Minecraft Launcher      #
# Account Module,part of CMCL    #
# copyright PuqiAR@2024          #
# Licensed under the MIT License #
##################################

from CMCL.CMCLib.Variables import constants

class MCAccount:
    def __init__(self,Name):
        self.Name = Name

class OfflineAccount(MCAccount):
    def __init__(self, Name):
        super().__init__(Name)

class MSAccount(MCAccount):
    def __init__(self, Name,Email,RefreshToken):
        super().__init__(Name)
        self.Email = Email
        self.RefreshToken = RefreshToken

class ThirdPartyAccount(MCAccount):
    def __init__(self, Name,Token):
        super().__init__(Name)
        self.Token = Token

