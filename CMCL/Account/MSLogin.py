##################################
# Common Minecraft Launcher      #
# Microsoft Login,part of CMCL   #
# copyright PuqiAR@2024          #
# Licensed under the MIT License #
##################################

import requests
# use requests (post,get)
from selenium import webdriver # open browser


from CMCL.CMCLib.Logger import logger
from CMCL.FluentUIExtend import *
from CMCL.Account.CMCLAccounts import *
from CMCL.CMCLib.CMCLException import *
from CMCL.Account.AccountController import *
from CMCL.CMCLib.Utils import *

from PyQt5.QtCore import QThread,pyqtSignal

CMCL_MS_OAuth_URL = "https://login.live.com/oauth20_authorize.srf?client_id=00000000402b5328&response_type=code&scope=service::user.auth.xboxlive.com::MBI_SSL&redirect_uri=https://login.live.com/oauth20_desktop.srf"
CMCL_MS_OAuth_URL = """
https://login.live.com/oauth20_authorize.srf
?client_id=00000000402b5328
&scope=service::user.auth.xboxlive.com::MBI_SSL
&redirect_uri=https://login.live.com/oauth20_desktop.srf
&response_type=code
&prompt=login
&msproxy=1
&issuer=mso
&tenant=consumers
&ui_locales=zh-CN
"""

class MSAuthThread(QThread):
    gotAuthCode = pyqtSignal(int)
    gotAuthToken = pyqtSignal(int)
    gotRefreshToken = pyqtSignal(int)
    XboxLiveAuthFinished = pyqtSignal(int)
    XSTSAuthFinished = pyqtSignal(int)
    gotMinecraftToken = pyqtSignal(int)
    checkedMinecraft = pyqtSignal(int)
    gotUuid = pyqtSignal(MSAccount)

    errorLogin = pyqtSignal(str)

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.steps = ["","获取授权码","获取授权令牌","获取刷新令牌","Xbox Live身份验证","XSTS 身份验证","获取Minecraft访问令牌","检查账户信息","最后一步:获取UUID"]
        self.step_c = 1
        self.steps_len = len(self.steps)-1
        self.AccountAdding = MSAccount("","","","")
    def last_step(self,accessToken):
        """
        添加账户
        """
        logger.info("MSLogin:last_step")
        self.step_c = self.steps_len
        self.AccountAdding.AccessToken = accessToken
        self.AccountAdding.Name = ms_get_user_all_profile(accessToken)["name"]
        self.AccountAdding.Uuid = ms_get_uuid(self.AccountAdding.Name)
        logger.info("successfully login account %s" % self.AccountAdding.Name)
        self.gotUuid.emit(self.AccountAdding)

    def checkMinecraft(self,accessToken):
        """
        检查账户Minecraft
        Seventh Step
        """
        self.step_c+=1
        logger.info("Checking Minecraft...")
        header = {"Authorization": f"Bearer {accessToken}"}
        response = requests.get("https://api.minecraftservices.com/entitlements/mcstore",headers=header)
        if response.text=="" or response.status_code!=200:
            self.errorLogin.emit("Not a official account or verify failed")
            return
        self.checkedMinecraft.emit(self.step_c)
        self.last_step(accessToken)
    def getMinecraftToken(self,token,UserHash):
        """
        获取Minecraft访问令牌
        token: xsts令牌
        Sixth Step
        """
        logger.info("Get Minecraft Token")
        self.step_c+=1
        data = {
            "identityToken": f"XBL3.0 x={UserHash};{token}"
        }
        header = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response = requests.post("https://api.minecraftservices.com/authentication/login_with_xbox", json=data,headers=header)
        if response.status_code == 200:
            jsdata = response.json()
            self.gotMinecraftToken.emit(self.step_c)
            accessToken = jsdata["access_token"]
            logger.info("MS Login Success,the access token is %s" % accessToken)
            self.AccountAdding.AccessToken = accessToken
            self.checkMinecraft(accessToken)
        else:
            self.errorLogin.emit("Get Minecraft Token Failed")
    
    def XSTS_Auth(self,Token,UserHash):
        """
        XSTS 验证
        Fifth Step
        """
        self.step_c+=1
        logger.debug("XSTS Auth")
        data = {
            "Properties": {
                "SandboxId": "RETAIL",
                "UserTokens": [
                    Token
                ]
            },
            "RelyingParty": "rp://api.minecraftservices.com/",
            "TokenType": "JWT"
        }
        header = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response = requests.post("https://xsts.auth.xboxlive.com/xsts/authorize", json=data,headers=header)
        if response.status_code == 200:
            token = response.json()["Token"] # token:xsts令牌
            self.getMinecraftToken(token,UserHash)
            self.XSTSAuthFinished.emit(self.step_c)
        else:
            self.errorLogin.emit("XSTS Auth Failed")
            return

    def XboxLive_Auth(self,AccessToken):
        """
        Xbox Live 身份验证
        fourth Step
        """
        self.step_c+=1
        logger.debug("Xbox Live Auth")
        data = {
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": AccessToken # 第二步中获取的访问令牌，如遇"Bad Request"可去掉"d="
            },
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT"
        }
        header = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response = requests.post("https://user.auth.xboxlive.com/user/authenticate", json=data,headers=header)
        if response.status_code == 200:
            token = response.json()["Token"]
            UserHash  = response.json()["DisplayClaims"]["xui"][0]["uhs"]
            self.XboxLiveAuthFinished.emit(self.step_c)
            self.XSTS_Auth(token,UserHash)
        else:
            self.errorLogin.emit("Xbox Live Auth Failed")
            return
    def Get_Auth_Token(self,code):
        """
        Second Step && third step
        """
        self.step_c+=1
        logger.debug("Getting Auth Token")
        data = {
            "client_id": "00000000402b5328",
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
            "scope": "service::user.auth.xboxlive.com::MBI_SSL",
        }
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "login.live.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        response = requests.post("https://login.live.com/oauth20_token.srf", data=data, headers=header)

        struct_data = response.json()
        AccessToken = struct_data["access_token"] ### tt
        self.gotAuthToken.emit(self.step_c)
        self.step_c+=1
        RefreshToken = struct_data["refresh_token"] ### tt
        self.gotRefreshToken.emit(self.step_c)
        self.AccountAdding.RefreshToken = RefreshToken
        self.XboxLive_Auth(AccessToken)

    def Get_Auth_Code(self):
        """
        First Step
        """
        self.step_c=1
        logger.debug("Getting Auth Code")
        browser = webdriver.ChromiumEdge()
        browser.get(CMCL_MS_OAuth_URL)
    
        redirect_url = browser.current_url
        while not redirect_url.find("?code=")>0:
            redirect_url = browser.current_url
            logger.debug(f"current url:{redirect_url},wating login...")
        browser.close()

        code = redirect_url.split("?code=")[1].split("&")[0]
        logger.debug("login success,got code!"+code)
        self.gotAuthCode.emit(self.step_c)
        self.Get_Auth_Token(code)
        

    def OAuthMicrosoft(self):
        """
        Microsoft Login Entry
        """
        logger.debug("starting OAuthMicrosoft")
        self.started.emit()
        self.Get_Auth_Code()


class MSRefreshThread(QThread):
    def __init__(self,Account:MSAccount):
        """
        Parameters
        ----------
        Account:MSAccount
            the account that need to refresh
        """
        super().__init__(self)
        self.Account = Account
    def run(self) -> None:
        logger.debug("starting MSRefreshThread")
        self.started.emit()

