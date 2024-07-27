##################################
# Common Minecraft Launcher      #
# Main Window ,   part of CMCL   #
# copyright PuqiAR@2024          #
# Licensed under the MIT License #
##################################
from time import sleep
from os import path as osp

from qfluentwidgets import (FluentIcon,
                            NavigationItemPosition,
                            SplashScreen,
                            )
from qframelesswindow import FramelessWindow


from PyQt5.QtCore import QSize,QTimer,QEventLoop
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget

from CMCL.CMCLib.SettingsController import Config
from CMCL.CMCLib.Logger import logger
from CMCL.CMCLib.CMCLException import InternalException
from CMCL.CMCLib.RealPath import Paths
from CMCL.DevConf import *
from CMCL.FluentUIExtend import CustomTitleBar

from Pages.HomePage import HomePage
from Pages.SettingsPage import SettingsPage
from QtUi.Ui_MainWindow import Ui_MainWindow
from Pages.AboutPage import AboutPage


class MainWindow(Ui_MainWindow,FramelessWindow):
    """
    CommonMinecraftLauncher 主窗口
    """
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.preprocess()
        self.show_splash_screen()
        self.show()
        self.reload_settings()
        self.pages = {}
        self.binding()
        self.init_pages()
        self.init_navigation_interface()
        self.last_process()

        # Show the splash screen for Config.SplashScreenTime (milliseconds)
        loop = QEventLoop(self)
        QTimer.singleShot(Config.SplashScreenTime.value,loop.quit)
        loop.exec()

        self.end_splash_screen()
    def end_splash_screen(self):
        self.splashScreen.finish()
    def show_splash_screen(self):
        self.splashScreen = SplashScreen(QIcon(CMCL_WINDOW_ICON),self)
        self.splashScreen.setIconSize(QSize(128,128))
    def last_process(self):
        """
        页面呈现给用户前最后的处理
        """
        self.on_navi_item_clicked("Home")  # show the home page
        self.stackedWidget.setCurrentWidget(self.homepage)
        self.NavigationInterface.setCurrentItem("Home")
        
    def reload_settings(self):
        """
        冷加载设置
        热加载仅在CMCL启动时调用
        """
        logger.debug(f"Reloading Settings")
        self.setWindowTitle(Config.LauncherWindowTitle.value)
        window = Config.WindowSize.value
        logger.debug(f"Got window size from Config,window")
        self.resize(window[0],window[1])
        logger.debug(f"Window resize to width {window[0]},height {window[1]}")
        
        if CMCL_USE_DARK_THEME:
            self.stackedWidget.setStyleSheet("background-color: rgb(20, 20, 20);")
    def preprocess(self):
        """
        初始化需设置的UI
        """
        self.setTitleBar(CustomTitleBar(self))
        self.titleBar.raise_()
        self.titleBar.setWindowIcon(QIcon(CMCL_WINDOW_ICON))
        self.TabBar.setAddButtonVisible(False)
        for n in range(self.stackedWidget.count()):
            self.stackedWidget.removeWidget(self.stackedWidget.widget(n))
    def binding(self):
        """
        绑定信号槽(PyQt)
        """
        #self.stackedWidget.currentChanged.connect(lambda: self.on_stackedWidget_changed())
        self.TabBar.tabCloseRequested.connect(lambda: self.on_tabbar_deleting())
        self.TabBar.tabBarClicked.connect(lambda: self.on_tabbar_click())
    def init_pages(self):
        """
        初始化各个子页面
        """
        logger.debug(f"Initing Pages,Current page:{self.stackedWidget.currentIndex()}")

        # 各个Page的QWidget
        self.emptyWidget = QWidget()
        self.homepage = HomePage(self)
        self.launch_page = None
        self.manage_account_page = None
        self.manage_game_page = None
        self.download_page = None
        self.settings_page = SettingsPage(self)
        self.about_application_page = AboutPage(self)

        self.stackedWidget.addWidget(self.emptyWidget)
        self.stackedWidget.addWidget(self.homepage)
        self.stackedWidget.addWidget(self.settings_page)
        self.stackedWidget.addWidget(self.about_application_page)

        # RouteKey 对应的页面QWidget
        self.pages = {
            "Home":self.homepage,
            "Launch":self.launch_page,
            #"Manage":self.manage_page,
            "Manage_Account":self.manage_account_page,
            "Manage_Game":self.manage_game_page,
            "Download":self.download_page,
            "Settings":self.settings_page,
            "About":self.about_application_page
        }
        # 页面的中文
        self.pages_to_zh = {
            "Home":"主页",
            "Launch":"启动",
            #"Manage":"管理",
            "Manage_Account":"账户",
            "Manage_Game":"游戏",
            "Download":"下载",
            "Settings":"设置",
            "About":"关于"
        }
        # 页面在导航栏显示的图标 (FluentIcon/FluentIconBase)
        self.pages_icon = {
            "Home":FluentIcon.HOME,
            "Launch":FluentIcon.PLAY,
            "Manage":FluentIcon.APPLICATION,
            "Manage_Account":FluentIcon.FINGERPRINT,
            "Manage_Game":FluentIcon.GAME,
            "Download":FluentIcon.DOWNLOAD,
            "Settings":FluentIcon.SETTING,
            "About":FluentIcon.INFO
        }
        
    def on_stackedWidget_changed(self):
        """
        调试使用：显示当前StackedWidget的索引
        """
        logger.debug(f"Current page:{self.stackedWidget.currentIndex()}")
    def change_NavigationInterface(self,routeKey:str):
        if routeKey in self.pages.keys():
            self.NavigationInterface.setCurrentItem(routeKey)
    def switchToPage(self,routeKey:str):
        """
        切换StackedWidget显示的页面并且更改TabBar的当前Tab和NavigationInterface的当前Item
        """
        if self.pages[routeKey]:
            self.stackedWidget.setCurrentWidget(self.pages[routeKey])
        else:
            logger.error(f"Page '{routeKey}' is empty page")
            self.stackedWidget.setCurrentWidget(self.emptyWidget)
        self.TabBar.setCurrentTab(routeKey)
        self.change_NavigationInterface(routeKey)
    def on_tabbar_deleting(self):
        """
        处理Tab的删除请求
        """
        routeKey = self.TabBar.currentTab().routeKey()
        self.TabBar.removeTabByKey(routeKey)

        if len(self.TabBar.items) == 0:
            
            return
        routeKey = self.TabBar.currentTab().routeKey()
        self.switchToPage(routeKey)
    def on_tabbar_click(self):
        """
        切换StackedWidget显示的页面
        """
        routeKey = self.TabBar.currentTab().routeKey()
        self.switchToPage(routeKey)
    def on_navi_item_clicked(self,routeKey:str):
        """
        添加NavigationInterface被点击的界面
        """
        for tab in self.TabBar.items:
            if routeKey == tab.routeKey():
                self.switchToPage(routeKey)
                return
        self.TabBar.addTab(
            routeKey,
            self.pages_to_zh[routeKey],
            self.pages_icon[routeKey],
            lambda: self.on_tabbar_click()
        )
        self.switchToPage(routeKey)
    def init_navigation_interface(self):
        """
        初始化导航栏
        """
        logger.debug(f"Initing Navigation Interface")

        for page in Config.Menu_Sequence.value:
            if page == "Home":      
                self.NavigationInterface.addItem(
                    "Home",
                    self.pages_icon[page],
                    "主页",
                    lambda: self.on_navi_item_clicked("Home")
                )
            elif page == "Launch":
                self.NavigationInterface.addItem(
                    "Launch",
                    self.pages_icon[page],
                    "启动",
                    lambda: self.on_navi_item_clicked("Launch")
                )
            elif page == "Manage":       
                self.NavigationInterface.addItem(
                    "Manage",
                    self.pages_icon[page],
                    "管理",
                )
                self.NavigationInterface.addItem(
                    "Manage_Account",
                    self.pages_icon["Manage_Account"],
                    "账户",
                    lambda: self.on_navi_item_clicked("Manage_Account"),
                    parentRouteKey="Manage"
                )
                self.NavigationInterface.addItem(
                    "Manage_Game",
                    self.pages_icon["Manage_Game"],
                    "游戏",
                    lambda: self.on_navi_item_clicked("Manage_Game"),
                    parentRouteKey="Manage"
                )
            elif page == "Download":
                self.NavigationInterface.addItem(
                    "Download",
                    self.pages_icon[page],
                    "下载",
                    lambda: self.on_navi_item_clicked("Download")
                )
            elif page == "Settings":
                self.NavigationInterface.addItem(
                    "Settings",
                    self.pages_icon[page],
                    "设置",
                    lambda: self.on_navi_item_clicked("Settings")
                )
            else:
                raise InternalException(f"Unknow page:{page}")
        self.NavigationInterface.addItem(
            "About",
            self.pages_icon["About"],
            "关于",
            position=NavigationItemPosition.BOTTOM,
            onClick=lambda: self.on_navi_item_clicked("About")
        )