# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\Files\Maker\Code\CommonMinecraftLauncher-PyQT\CMCLv2\QtUi\ManageAccount.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(948, 519)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.BodyLabel = BodyLabel(Form)
        font = QtGui.QFont()
        font.setFamily("MiSans")
        font.setPointSize(14)
        font.setBold(False)
        self.BodyLabel.setFont(font)
        self.BodyLabel.setObjectName("BodyLabel")
        self.verticalLayout.addWidget(self.BodyLabel)
        self.CaptionLabel = CaptionLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(11)
        font.setBold(False)
        self.CaptionLabel.setFont(font)
        self.CaptionLabel.setObjectName("CaptionLabel")
        self.verticalLayout.addWidget(self.CaptionLabel)
        self.SegmentedWidget = SegmentedWidget(Form)
        self.SegmentedWidget.setObjectName("SegmentedWidget")
        self.verticalLayout.addWidget(self.SegmentedWidget)
        self.PopUpAniStackedWidget = PopUpAniStackedWidget(Form)
        self.PopUpAniStackedWidget.setObjectName("PopUpAniStackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.PopUpAniStackedWidget.addWidget(self.page)
        self.verticalLayout.addWidget(self.PopUpAniStackedWidget)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 30)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.BodyLabel.setText(_translate("Form", "管理账户"))
        self.CaptionLabel.setText(_translate("Form", "在这里管理你的所有账户"))
from qfluentwidgets import BodyLabel, CaptionLabel, PopUpAniStackedWidget, SegmentedWidget