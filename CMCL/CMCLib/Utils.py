##################################
# Common Minecraft Launcher      #
# Utils module,part of CMCL      #
# copyright PuqiAR@2024          #
# Licensed under the MIT License #
##################################

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