##################################
# Common Minecraft Launcher      #
# Account Ctrl,part of CMCL      #
# copyright PuqiAR@2024          #
# Licensed under the MIT License #
##################################

from pickle import dumps as pickle_dumps
from pickle import loads as pickle_loads

from CMCL.CMCLib.SettingsController import Config
from CMCL.CMCLib.Variables import *
from CMCL.CMCLib.Utils import *
from CMCL.Account.CMCLAccounts import *
from CMCL.CMCLib.RealPath import *
from CMCL.CMCLib.Logger import logger


from os import (listdir,remove,rename)

ACCOUNT_PATH = osp.join(Paths.INTERNALPATH,"Account","Data")
logger.debug("ACCOUNT_PATH: %s"%ACCOUNT_PATH)

class AccountController:
    @staticmethod
    def load_accounts():
        
        for file_path in listdir(Config.AccountsPath.value):
            logger.debug("file_path: %s"%file_path)
            if not file_path.endswith(".acc"):
                logger.debug("file_path: %s is not a account file"%file_path)
                continue
            with open(osp.join(Config.AccountsPath.value,file_path),"rb") as f:
                data = f.read() 
            if data == "":
                remove(osp.join(Config.AccountsPath.value,file_path))
            data = pickle_loads(data,encoding="utf-8")
            if not isinstance(data,MCAccount):
                logger.warning("Account file data error!auto deleted it")
                remove(osp.join(Config.AccountsPath.value,file_path))
                continue
            if data.Name != file_path.split(".")[0]:
                logger.warning("Account file name error!auto renamed it")
                rename(
                    osp.join(Config.AccountsPath.value,file_path),
                    osp.join(Config.AccountsPath.value,data.Name+constants.AccountDataFileFormat)
                )
            AccountController._add_account(data)
        logger.info("######## loaded accounts "+str(Accounts.accounts_data))
    @staticmethod
    def _add_account(account:MCAccount):
        logger.debug(f"account type is {type(account)}")

        if account.type == constants.loginMethod.Official:
            accounts.accounts_data[constants.loginMethod.Official].append(account)
        elif account.type == constants.loginMethod.Offline:
            accounts.accounts_data[constants.loginMethod.Offline].append(account)
        elif account.type == constants.loginMethod.ThirdParty:
            accounts.accounts_data[constants.loginMethod.ThirdParty].append(account)
        else:
            raise Exception("Invalid account type")
        if not account.type == constants.loginMethod.Official:
            return
        if not account.Avatar:
            account.Avatar = Skin.getProfile(account.Name)
        if not account.Skin:
            account.Skin = Skin.getSkin(account.Name)
        if not account.Cape:
            account.Cape = Skin.getCape(account.Name)

    @staticmethod
    def save_account(account:MCAccount):
        name = account.Name
        with open(osp.join(Config.AccountsPath.value,constants.AccountDataFileFormat%name),"wb") as f:
            f.write(pickle_dumps(account))
    @staticmethod
    def update_account(account:MCAccount,new_account:MCAccount):
        """
        用于更新mc账户的名称,ms账户的token
        更换type不支持，使用remove_account

        Parameters:
        -----------
        account: MCAccount
            the account to be updated
        new_account: MCAccount
            the new account to update to account
        """
        Check(
            account.type,
            new_account.type,
            error=InternalException(f"trying refresh mc account: account {account.Name}:{account.type} doesn't match the refresh account {new_account.Name}:{account.type}")
        )
        Check(
            account.Name in accounts.accounts_data[account.type],
            True,
            error=InternalException(f"trying refresh {account.Name} account: account {account.Name} doesn't exist in accounts")
        )
        accounts.accounts_data[account.Name] = new_account

    @staticmethod
    def save_accounts():
        for account in accounts.accounts_data[constants.loginMethod.Official]:
            AccountController.save_account(account)
        for account in accounts.accounts_data[constants.loginMethod.Offline]:
            AccountController.save_account(account)
        for account in accounts.accounts_data[constants.loginMethod.ThirdParty]:
            AccountController.save_account(account)
    @staticmethod
    def remove_account(Account:MCAccount):
        remove(osp.join(Config.AccountsPath.value,constants.AccountDataFileFormat%Account.Name))
        if Account.type == constants.loginMethod.Official:
            accounts.accounts_data[constants.loginMethod.Official].remove(Account)
        elif Account.type == constants.loginMethod.Offline:
            accounts.accounts_data[constants.loginMethod.Offline].remove(Account)
        elif Account.type == constants.loginMethod.ThirdParty:
            accounts.accounts_data[constants.loginMethod.ThirdParty].remove(Account)