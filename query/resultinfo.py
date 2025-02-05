# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resultinfo.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import *

import sys
sys.path.append('../')#为什么，因为grade.py与需要先从当前路径出来，再进入service中
from service import service

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow,self).__init__()
        #调用本类中的实例方法
        self.setupUi(self)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 457)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnQuit = QtWidgets.QPushButton(self.centralwidget)
        self.btnQuit.setGeometry(QtCore.QRect(710, 20, 81, 31))
        self.btnQuit.setObjectName("btnQuit")
        self.btnQuery = QtWidgets.QPushButton(self.centralwidget)
        self.btnQuery.setGeometry(QtCore.QRect(620, 20, 81, 31))
        self.btnQuery.setObjectName("btnQuery")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 70, 761, 311))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 111, 41))
        self.label.setObjectName("label")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(200, 20, 111, 41))
        self.label_1.setObjectName("label_1")
        self.editname = QtWidgets.QLineEdit(self.centralwidget)
        self.editname.setGeometry(QtCore.QRect(90, 20, 113, 41))
        self.editname.setObjectName("editname")
        self.cboExamKind = QtWidgets.QComboBox(self.centralwidget)
        self.cboExamKind.setGeometry(QtCore.QRect(280, 20, 121, 41))
        self.cboExamKind.setObjectName("cboExamKind")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(410, 20, 111, 41))
        self.label_2.setObjectName("label_2")
        self.cboSubject = QtWidgets.QComboBox(self.centralwidget)
        self.cboSubject.setGeometry(QtCore.QRect(490, 20, 121, 41))
        self.cboSubject.setObjectName("cboSubject")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 33))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #槽函数
        self.bindCbo()
        self.query()
        self.btnQuery.clicked.connect(self.query)

    # 自定义绑定下拉组合框的方法
    def bindCbo(self):
        self.cboExamKind.addItem('所有')
        result=service.query('select kindname from tb_examkinds')
        for i in result:
            self.cboExamKind.addItem(i[0])
        self.cboSubject.addItem('所有')
        result=service.query('select subname from tb_subject')
        for i in result:
            self.cboSubject.addItem(i[0])
    #
    def query(self):
        self.tableWidget.setRowCount(0)#清空所有行
        stuname=self.editname.text()#获取姓名的单行文本框
        kindname=self.cboExamKind.currentText()#获取考试的类别
        subname=self.cboSubject.currentText()#获取考试的科目
        if stuname=='':
            if kindname=='所有':
                if subname=='所有':
                    #查询全部
                    result=service.query(
                        'select stuid,stuname,concat(gradename,classname),kindname,subname,result from v_resultinfo')
                else:#根据考试科目查
                    result = service.query(
                        'select stuid,stuname,concat(gradename,classname),kindname,subname,result from v_resultinfo where subname=%s',subname)
            else:#根据考试类别查
                if subname=='所有':#只需根据考试类别查
                    result = service.query(
                        'select stuid,stuname,concat(gradename,classname),kindname,subname,result from v_resultinfo where kindname=%s',kindname)
                else:#根据考试科目和考试类别查
                    result = service.query(
                        'select stuid,stuname,concat(gradename,classname),kindname,subname,result from v_resultinfo where subname=%s and kindname=%s',subname,kindname)
        else:#姓名不为空的情况
            if kindname=='所有':
                if subname=='所有':
                    #根据姓名查询
                    result=service.query(
                        'select stuid,stuname,concat(gradename,classname),kindname,subname,result from v_resultinfo where stuname like %s','%'+stuname+'%')
                else:#根据考试科目查
                    result = service.query(
                        'select stuid,stuname,concat(gradename,classname),kindname,subname,result from v_resultinfo where subname=%s and stuname like %s',subname,'%'+stuname+'%')
            else:#根据考试类别查
                if subname=='所有':#只需根据考试类别查
                    result = service.query(
                        'select stuid,stuname,concat(gradename,classname),kindname,subname,result from v_resultinfo where kindname=%s and stuname like %s',kindname,'%'+stuname+'%')
                else:#根据考试科目和考试类别查
                    result = service.query(
                        'select stuid,stuname,concat(gradename,classname),kindname,subname,result from v_resultinfo where subname=%s and kindname=%s and stuname like %s',subname,kindname,'%'+stuname+'%')
        #显示在表格上
        row=len(result)
        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(
            ['学生编号','学生姓名','班级','考试类别','科目','成绩']
        )
        for i in range(row):
            for j in range(6):
                data=QTableWidgetItem(str(result[i][j]))
                self.tableWidget.setItem(i, j, data)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "成绩信息查询"))
        self.btnQuit.setText(_translate("MainWindow", "退出"))
        self.btnQuery.setText(_translate("MainWindow", "查询"))
        self.label.setText(_translate("MainWindow", "学生姓名："))
        self.label_1.setText(_translate("MainWindow", "考试类别："))
        self.label_2.setText(_translate("MainWindow", "考试科目："))
