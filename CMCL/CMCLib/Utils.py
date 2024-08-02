##################################
# Common Minecraft Launcher      #
# Utils module,part of CMCL      #
# copyright PuqiAR@2024          #
# Licensed under the MIT License #
##################################

from requests import get as http_get
from json import loads as json_loads

from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtCore import QObject, QThread
from CMCL.CMCLib.Logger import logger

from CMCL.CMCLib.CMCLException import *
def os_is_dark_theme(): 
    try:
        import winreg
    except ImportError:
        return False
    registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    reg_keypath = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
    try:
        reg_key = winreg.OpenKey(registry, reg_keypath)
    except FileNotFoundError:
        return False

    for i in range(1024):
        try:
            value_name, value, _ = winreg.EnumValue(reg_key, i)
            if value_name == 'AppsUseLightTheme':
                return value == 0
        except OSError:
            break
    return False

def readFile(path) -> str:
    f = open(path,'r',encoding='utf-8')
    x = f.read()
    f.close()
    return x

def ms_get_uuid(name:str)->str:
    content = http_get(f"https://api.mojang.com/users/profiles/minecraft/{name}").text
    return json_loads(content)['id']
def ms_get_user_all_profile(accessToken:str)->dict:
    content = http_get(f"https://api.minecraftservices.com/minecraft/profile",headers={'Authorization':f'Bearer {accessToken}'}).text
    return json_loads(content)

class Skin:
    @staticmethod
    def getHead(name:str) -> bytes:
        response = http_get(f"https://crafatar.com/renders/head/{ms_get_uuid(name)}")
        return response.content
    @staticmethod
    def getProfile(name:str) -> bytes:
        response = http_get(f"https://crafatar.com/avatars/{ms_get_uuid(name)}")
        return response.content
    @staticmethod
    def getBodyRenders(name:str) -> bytes:
        response = http_get(f"https://crafatar.com/renders/body/{ms_get_uuid(name)}")
        return response.content
    @staticmethod
    def getCape(name:str) -> bytes:
        response = http_get(f"https://crafatar.com/capes/{ms_get_uuid(name)}")
        return response.content
    @staticmethod
    def getSkin(name:str) -> bytes:
        response = http_get(f"https://crafatar.com/skins/{ms_get_uuid(name)}")
        return response.content

def bytesToImage(data:bytes):
    return QImage.fromData(data)
def bytesToPixmap(data:bytes):
    return QPixmap.fromImage(bytesToImage(data))

def Retry(func,times=3):
    def wrapper(*args,**kwargs):
        for i in range(times):
            try:
                return func(*args,**kwargs)
            except Exception as e:
                logger.error("execute faild,error "+e.__str__())
                continue
        return -1
    return wrapper

def Check(value,correct_value,method=lambda x,y:x==y,error=InternalException("Check faild")):
    if method(value,correct_value):
        return True
    else:
        raise error

class Thread(QThread):
    def __init__(self, parent,worker) -> None:
        super().__init__(parent)
        self.worker = worker
    def run(self) -> None:
        self.worker()
        self.finished.emit()