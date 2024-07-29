##################################
# Common Minecraft Launcher      #
# Variables   ,part of CMCL      #
# copyright PuqiAR@2024          #
# Licensed under the MIT License #
##################################


class Constants:
    class LoginMethod:
        Official = "Official"
        Offline = "Offline"
        ThirdParty = "ThirdParty"
    class LoginFormat:
        Accounts = "Accounts"
        AccessToken = "AccessToken"
        Token = "Token"
        RefreshToken = "RefreshToken"
        SkinPath = "SkinPath"

    loginMethod = LoginMethod()
    loginFormat = LoginFormat()

    AccountDataFileFormat = "%s.acc"
constants = Constants()


class Accounts:
    accounts_data = {
            constants.loginMethod.Official:[
            ],
            constants.loginMethod.Offline:[
            ],
            constants.loginMethod.ThirdParty:[
            ],
    }