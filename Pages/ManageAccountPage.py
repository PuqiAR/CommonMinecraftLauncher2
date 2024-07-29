##################################
# Common Minecraft Launcher      #
# Account Page,part of CMCL      #
# copyright PuqiAR@2024          #
# Licensed under the MIT License #
##################################

from PyQt5.QtWidgets import (
    QWidget,
    QListWidgetItem,
    QListView,
    QApplication,
    QSizePolicy,
    QVBoxLayout
)
from PyQt5.QtCore import QSize


from qfluentwidgets import (
    FluentIcon,
    ListWidget,
    BodyLabel,
    InfoBar
)

from QtUi.Ui_ManageAccount import Ui_Form as Ui_ManageAccount

from CMCL.CMCLib.Variables import *
from CMCL.CMCLib.SettingsController import Config
from CMCL.FluentUIExtend import *
from Asset.FluentIcons import FluentIconsEx
from CMCL.Account.MSLogin import *

from CMCL.CMCLib.Utils import *
from Pages.AccountCard import AccountCard

class AccountShowingPage(QWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self.listWidget = ListWidget()
        self.listWidget.setResizeMode(QListView.Adjust)
        self.listWidget.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.listWidget)
        self.layout().setContentsMargins(0,0,0,0)
    def add(self,widget,sizeHint=None):
        listItem = QListWidgetItem()
        if sizeHint:
            listItem.setSizeHint(QSize(928,sizeHint))
        self.listWidget.addItem(listItem)
        self.listWidget.setItemWidget(listItem,widget)

class EmptyAccountPage(QWidget):
    def __init__(self,parent,loginMethod):
        super().__init__(parent)
        self.label = BodyLabel(self)
        self.label.setText(f"额...你当前好像还没有{loginMethod}的账户")

class ManageAccountPage(Ui_ManageAccount,QWidget):
    def clear_stackedWidget(self):
        while self.PopUpAniStackedWidget.count()>0:
            self.PopUpAniStackedWidget.removeWidget(self.PopUpAniStackedWidget.currentWidget())
    def switchToPage(self,routeKey):
        self.SegmentedWidget.setCurrentItem(routeKey)
        self.PopUpAniStackedWidget.setCurrentWidget(self.pages[routeKey])
    def init_pages(self):
        self.officialAccountPage = AccountShowingPage(self)
        self.offlineAccountPage = AccountShowingPage(self)
        self.thirdpartyAccountPage = AccountShowingPage(self)
        self.emptyAccountPage = EmptyAccountPage(self,constants.loginMethod.Official)

        self.pages = {
            constants.loginMethod.Official:self.officialAccountPage,
            constants.loginMethod.Offline:self.offlineAccountPage,
            constants.loginMethod.ThirdParty:self.thirdpartyAccountPage,
            "empty":self.emptyAccountPage
        }

        self.PopUpAniStackedWidget.addWidget(self.emptyAccountPage)
        self.PopUpAniStackedWidget.addWidget(self.officialAccountPage)
        self.PopUpAniStackedWidget.addWidget(self.offlineAccountPage)
        self.PopUpAniStackedWidget.addWidget(self.thirdpartyAccountPage)

        if len(accounts.accounts_data[constants.loginMethod.Official])>0:
            self.switchToPage(constants.loginMethod.Official)
        elif len(accounts.accounts_data[constants.loginMethod.Offline])>0:
            self.switchToPage(constants.loginMethod.Offline)
        elif len(accounts.accounts_data[constants.loginMethod.ThirdParty])>0:
            self.switchToPage(constants.loginMethod.ThirdParty)
        else:
            self.emptyAccountPage = EmptyAccountPage(self,"任意")
            self.switchToPage("empty")
    def load_accounts_list(self):
        self.officialAccountPage.listWidget.clear()
        for account in accounts.accounts_data[constants.loginMethod.Official]:
            card = AccountCard(None,account)
            self.officialAccountPage.add(card,80)

    def add_account_msgBox(self):
        messageBox = ComboMessageBox(self,"账户类型")
        messageBox.comboBox.addItem(
            "正版登录",
            FluentIconsEx.MICROSOFT,
            constants.loginMethod.Official
        )
        messageBox.comboBox.addItem(
            "离线登录",
            FluentIconsEx.OFFLINE_FILL,
            constants.loginMethod.Offline
        )
        messageBox.comboBox.addItem(
            "第三方登录",
            FluentIconsEx.THIRDPARTY,
            constants.loginMethod.ThirdParty
        )

        if messageBox.exec():
            # add account
            method = messageBox.comboBox.currentData()
            if method == constants.loginMethod.Official:
                self.add_ms_account()
            elif method == constants.loginMethod.Offline:
                self.add_offline_account()
            elif method == constants.loginMethod.ThirdParty:
                self.add_thirdparty_account()
    def update_mslogin_progress(self,progress):
        QApplication.processEvents()
        if self.use_info_bar_show_message:
            if self.MicrosoftOAuthProgressMessageBox.isVisible():
                self.MicrosoftOAuthProgressMessageBox.close()
            InfoBar.success(
                "登录到正版账户",
                self.MicrosoftOAuthThread.steps[progress],
                parent=self,
                duration=5000
            )
            QApplication.processEvents()
        else:
            self.MicrosoftOAuthProgressMessageBox.Update(
                self.MicrosoftOAuthThread.steps[progress],
                int(progress/self.MicrosoftOAuthThread.steps_len*100)
            )
        QApplication.processEvents()
    def show_add_ms_account_message(self):
        """
        用户关闭弹窗时,消息改为Infobar显示
        """
        self.use_info_bar_show_message = True
    def ms_login_success(self,account:MSAccount):
        AccountController._add_account(account)
        self.MicrosoftOAuthProgressMessageBox.close()
        if account in accounts.accounts_data[constants.loginMethod.Official]:
            InfoBar.warning(
                "登录到正版账户",
                f"正版账户{account.Name}已存在!",
                parent=self,
                duration=5000
            )
        else:
            InfoBar.success(
                "登录到正版账户",
                f"登录正版账户{account.Name}成功!",
                parent=self,
                duration=5000
            )
            self.push_ms_account(account)
    def add_ms_account(self):
        self.MicrosoftOAuthProgressMessageBox = ProgressBarMessageBox(self,"",userClosedCallBack=lambda:self.show_add_ms_account_message())
        self.MicrosoftOAuthThread = MSAuthThread(self)
        self.MicrosoftOAuthThread.errorLogin.connect(self.ms_login_faild)
        self.MicrosoftOAuthThread.gotAuthCode.connect(self.update_mslogin_progress)
        self.MicrosoftOAuthThread.gotAuthToken.connect(self.update_mslogin_progress)
        self.MicrosoftOAuthThread.gotRefreshToken.connect(self.update_mslogin_progress)
        self.MicrosoftOAuthThread.XboxLiveAuthFinished.connect(self.update_mslogin_progress)
        self.MicrosoftOAuthThread.XSTSAuthFinished.connect(self.update_mslogin_progress)
        self.MicrosoftOAuthThread.gotMinecraftToken.connect(self.update_mslogin_progress)
        self.MicrosoftOAuthThread.checkedMinecraft.connect(self.update_mslogin_progress)
        self.MicrosoftOAuthThread.gotUuid.connect(self.ms_login_success)

        self.MicrosoftOAuthProgressMessageBox.show()
        self.MicrosoftOAuthThread.OAuthMicrosoft()
    def add_offline_account(self):
        name = ""
        box = LineEditMessageBox(self,"输入名称")
        if box.exec():
            name = box.lineEdit.text()
        else:
            return
        account = OfflineAccount(name)
        AccountController._add_account(account)
        self.push_offline_account(account)
    def add_thirdparty_account(self):
        pass
    def ms_login_faild(self,msg):
        if self.MicrosoftOAuthProgressMessageBox.isVisible():
            self.MicrosoftOAuthProgressMessageBox.close()
        InfoBar.error(
            "登录到正版账户",
            "呃..看起来发生了一点错误:"+msg,
            parent=self,
            duration=5000,
        )
        QApplication.processEvents()
    def push_ms_account(self,account:MSAccount):
        self.officialAccountPage.add(AccountCard(None,account),80)
    def push_offline_account(self,account:OfflineAccount):
        self.offlineAccountPage.add(AccountCard(None,account),80)
    def push_third_party_account(self,account:ThirdPartyAccount):
        self.thirdpartyAccountPage.add(AccountCard(None,account),80)
    def push_account(self,account:MCAccount):
        if account.type == constants.loginMethod.Official:
            self.push_ms_account(account)
        elif account.type == constants.loginMethod.Offline:
            self.push_offline_account(account)
        elif account.type == constants.loginMethod.ThirdParty:
            self.push_third_party_account(account)
        else:
            raise Exception(f"未知的账户类型{account.type}")
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.clear_stackedWidget()
        AccountController.load_accounts()
        self.SegmentedWidget.addItem(
            constants.loginMethod.Official,
            "正版登录(MicrosoftLogin)",
            lambda: self.PopUpAniStackedWidget.setCurrentWidget(self.officialAccountPage),
            FluentIconsEx.MICROSOFT
        )
        self.SegmentedWidget.addItem(
            constants.loginMethod.Offline,
            "离线登录",
            lambda: self.PopUpAniStackedWidget.setCurrentWidget(self.offlineAccountPage),
            FluentIconsEx.OFFLINE_FILL
        )
        self.SegmentedWidget.addItem(
            constants.loginMethod.ThirdParty,
            "第三方登录",
            lambda: self.PopUpAniStackedWidget.setCurrentWidget(self.thirdpartyAccountPage),
            FluentIconsEx.THIRDPARTY
        )
        self.init_pages()
        self.load_accounts_list()
        self.use_info_bar_show_message = False

        self.TransparentToolButton.setIcon(FluentIcon.ADD_TO)
        self.TransparentToolButton.clicked.connect(lambda:self.add_account_msgBox())
        