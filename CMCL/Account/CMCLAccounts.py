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
        self.Skin:bytes = None   # show
        self.Avatar:bytes = None # show
        self.Cape:bytes = None

class OfflineAccount(MCAccount):
    def __init__(self, Name):
        super().__init__(Name)
        self.type=constants.loginMethod.Offline

class MSAccount(MCAccount):
    def __init__(self, Name,AccessToken,Uuid,RefreshToken):
        super().__init__(Name)
        self.type=constants.loginMethod.Official
        self.AccessToken = AccessToken
        self.Uuid = Uuid
        self.RefreshToken = RefreshToken

class ThirdPartyAccount(MCAccount):
    def __init__(self, Name,Token):
        super().__init__(Name)
        self.type=constants.loginMethod.ThirdParty
        self.Token = Token

def AccountLoginMethod(account:MCAccount):
    if account.type == constants.loginMethod.Official:
        return "正版登录"
    elif account.type == constants.loginMethod.Offline:
        return "离线登录"
    elif account.type == constants.loginMethod.ThirdParty:
        return "第三方登录"
    else:
        return "error"