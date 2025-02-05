# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'classes.ui'
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
        self.setupUi(self)
        self.query()
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(494, 459)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnUpdateClass = QtWidgets.QPushButton(self.centralwidget)
        self.btnUpdateClass.setGeometry(QtCore.QRect(140, 310, 75, 31))
        self.btnUpdateClass.setObjectName("btnUpdateClass")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(270, 260, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 260, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.btnDeleteClass = QtWidgets.QPushButton(self.centralwidget)
        self.btnDeleteClass.setGeometry(QtCore.QRect(260, 310, 75, 31))
        self.btnDeleteClass.setObjectName("btnDeleteClass")
        self.editClassID = QtWidgets.QLineEdit(self.centralwidget)
        self.editClassID.setGeometry(QtCore.QRect(100, 260, 131, 31))
        self.editClassID.setObjectName("editClassID")
        self.editClassName = QtWidgets.QLineEdit(self.centralwidget)
        self.editClassName.setGeometry(QtCore.QRect(350, 260, 131, 31))
        self.editClassName.setObjectName("editClassName")
        self.btnAddClass = QtWidgets.QPushButton(self.centralwidget)
        self.btnAddClass.setGeometry(QtCore.QRect(20, 310, 75, 31))
        self.btnAddClass.setObjectName("btnAddClass")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 471, 192))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.btnQuitClass = QtWidgets.QPushButton(self.centralwidget)
        self.btnQuitClass.setGeometry(QtCore.QRect(370, 310, 75, 31))
        self.btnQuitClass.setObjectName("btnQuitClass")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 220, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.editClassSelect = QtWidgets.QLineEdit(self.centralwidget)
        self.editClassSelect.setGeometry(QtCore.QRect(100, 220, 131, 31))
        self.editClassSelect.setObjectName("editClassSelect")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 494, 33))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 为添加按钮关联槽函数
        self.btnAddClass.clicked.connect(self.add)
        # 表格项被单击时调用getItem
        self.tableWidget.itemClicked.connect(self.getItem)
        # 为修改按钮关联槽函数
        self.btnUpdateClass.clicked.connect(self.edit)
        # 为删除按钮关联槽函数
        self.btnDeleteClass.clicked.connect(self.delete)
        # 为退出按钮关联槽函数
        self.btnQuitClass.clicked.connect(self.close)

    def query(self):
        #清空表格的所有行
        self.tableWidget.setRowCount(0)
        #调用公共类中的公共方法，查询
        result=service.query('select b.classID,a.gradeName,b.className from tb_grade as a inner join tb_class as b on a.gradeID=b.gradeID')
        row=len(result)  # 获取数据的行数
        self.tableWidget.setRowCount(row)#设置行数
        self.tableWidget.setColumnCount(3)#设置列数
        #设置表格的标题
        self.tableWidget.setHorizontalHeaderLabels(['班级编号','年级名称','班级名称'])
        for i in range(row):#遍历行
            for j in range(self.tableWidget.columnCount()):#遍历列
                data=QTableWidgetItem(str(result[i][j]))
                #在i行j列放入数据data
                self.tableWidget.setItem(i,j,data)


    # 自定义一个方法
    # 到数据库中查询要添加的年级名称是否存在
    # 到数据库查找这个名字是否存在
    def getName(self, name):
        result = service.query('select * from tb_class where className=%s', (name,))
        return len(result)  # 返回查询的个数

    # 自定义槽函数,向年级表中添加数据
    def add(self):
        classid = self.editClassID.text()  # 获取年级的编号
        classname = self.editClassName.text()  # 获取年级的名称
        if classid != '' and classname != '':
            if self.getName(classname) > 0:
                # 要添加的年级名称在数据库中存在
                # 清空文本框
                self.editClassName.setText('')
                QMessageBox.information(None, '提示', '班级已经存在，请重新输入')
            else:
                # 执行添加操作
                result = service.exec('insert into tb_class values(%s,%s)', (classid, classname))
                if result > 0:
                    self.query()  # 添加成功后重新加载窗体
                    QMessageBox.information(None, '提示', '信息添加成功', QMessageBox.Ok)
        else:
            QMessageBox.warning(None, '警告', '请输入数据后在进行添加操作', QMessageBox.Ok)

    # 修改操作
    # 获取选中的表格内容
    def getItem(self, item):
        if item.column() == 0:  # 第一列
            self.select = item.text()
            self.editClassID.setText(self.select)

    # 年级的修改
    def edit(self):
        try:
            if self.select != '':
                # 年级编号是否有值
                classname = self.editClassName.text()
                if classname != '':
                    # 到数据库中查询一下，要修改的年级名称是否存在
                    if self.getName(classname) > 0:
                        # 存在
                        QMessageBox.information(None, '提示', '要修改的班级已经存在', QMessageBox.Ok)
                        pass
                    else:
                        result = service.exec('update tb_class set classname=%s where classid=%s',
                                              (classname, self.select))
                        if result > 0:
                            # 修改成功
                            self.query()
                            QMessageBox.information(None, '提示', '修改成功', QMessageBox.Ok)
        except Exception as e:
            print(e)
            QMessageBox.warning(None, '警告', '请选择要修改的数据', QMessageBox.Ok)

    # 在数据库中grade表有 主外键 关系
    # 班级表tb_class中含有gradeid，所以tb_class是外键表
    # 学生表tb_student中含有gradeid，所以tb_student是外键表
    # 现在再删除tb_grade中的gradeid，删除主表的主键，
    # 与之关联的外键表的数据要同时删除
    # 在数据库表中添加外键约束是加上 on delete cascade
    # 删除操作
    def delete(self):
        try:
            if self.select != '':
                # 删除年级表中的数据
                result = service.exec('delete from tb_class where classid=%s', (self.select,))
                if result > 0:
                    # 删除成功
                    self.query()
                    QMessageBox.information(None, '提示', '删除成功', QMessageBox.Ok)
        except Exception as e:
            print(e)
            QMessageBox.warning(None, '警告', '请选择要删除的数据', QMessageBox.Ok)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "班级设置"))
        self.btnUpdateClass.setText(_translate("MainWindow", "修改"))
        self.label_2.setText(_translate("MainWindow", "班级名称："))
        self.label.setText(_translate("MainWindow", "班级编号："))
        self.btnDeleteClass.setText(_translate("MainWindow", "删除"))
        self.btnAddClass.setText(_translate("MainWindow", "添加"))
        self.btnQuitClass.setText(_translate("MainWindow", "退出"))
        self.label_3.setText(_translate("MainWindow", "选择班级："))
