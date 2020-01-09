from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        #主窗口设置
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 700)
        MainWindow.setStyleSheet("background-color: rgb(250, 250, 250);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.caidan(MainWindow)

        # 加入作业lable
        self.lable = QtWidgets.QLabel(MainWindow)
        self.lable.setText("Process")
        self.lable.setGeometry(QtCore.QRect(70, 50, 200, 40))
        font = QtGui.QFont("KaiTi_GB2312", 16, 53)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.lable.setFont(font)
        self.lable.setStyleSheet("color: rgb(51,105,30);")
        self.lable.setTextFormat(QtCore.Qt.AutoText)
        self.lable.setWordWrap(True)

        self.mode = QtWidgets.QLabel(MainWindow)
        self.mode.setGeometry(QtCore.QRect(15, 20, 300, 40))
        font = QtGui.QFont("KaiTi_GB2312", 18, 53)
        # font.setFamily("KaiTi_GB2312")
        # font.setPointSize(18)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.mode.setFont(font)
        self.mode.setStyleSheet("color: rgb(51,105,30);")
        self.mode.setTextFormat(QtCore.Qt.AutoText)
        self.mode.setWordWrap(True)

        #创建快捷加入按钮
        self.btnGroup = {}
        for i in range(0, 64):
            self.btnGroup[i] = QtWidgets.QPushButton(MainWindow)  # 创建一个按钮，并将按钮加入到窗口MainWindow中
            self.btnGroup[i].setFont(QtGui.QFont('SimHei', 8, 50))
            self.btnGroup[i].setText(str(i+1)+'0k')
            self.btnGroup[i].setGeometry(QtCore.QRect(((i//16)+1)*36, 90 + (i % 16) * 32, 30, 29))
            self.btnGroup[i].setStyleSheet("QPushButton{color:rgb(255,255,230)}"
                                           "QPushButton{background-color:rgb(124,179,66)}"
                                           "QPushButton{border: 2px solid rgb(100,100,100)}"
                                           "QPushButton:hover{background-color:rgb(104,159,56)}"
                                           "QPushButton:pressed{background-color:rgb(51,105,30)}")

        # 创建一个文本框输入大小，并将按钮加入到窗口MainWindow中
        self.textbox = QtWidgets.QLineEdit(MainWindow)
        self.textbox.setPlaceholderText("小于640的整数")
        self.textbox.setFont(QtGui.QFont('Microsoft YaHei', 10))
        self.textbox.setGeometry(35, 620, 135, 25)
        self.textbox.setStyleSheet(
            "QLineEdit:hover{background-color:rgb(255,255,255)}"  # 光标移动到上面后的前景色
            '''QLineEdit{
                    color:rgb(0,0,0)
                    background-color:rgb(242,242,242)
                    width:200px;
                    border-radius:10px;
                    padding:2px 4px;
            }'''
        )
        validator = QDoubleValidator(0, 640, 3)
        self.textbox.setValidator(validator)

        # 创建一个文本框输入大小，并将按钮加入到窗口MainWindow中
        self.vtextbox = QtWidgets.QLineEdit(MainWindow)
        self.vtextbox.setPlaceholderText("使用回车来保存输入")
        self.vtextbox.setFont(QtGui.QFont('Microsoft YaHei', 10))
        self.vtextbox.setGeometry(185, 420, 150, 25)
        self.vtextbox.setStyleSheet(
            "QLineEdit:hover{background-color:rgb(255,255,255)}"  # 光标移动到上面后的前景色
            '''QLineEdit{
                    color:rgb(255,0,0)
                    background-color:rgb(242,242,242)
                    width:200px;
                    border-radius:10px;
                    padding:2px 4px;
            }'''
        )
        validator = QDoubleValidator(0, 640, 3)
        self.vtextbox.setValidator(validator)

        # 创建文本框输入确认按钮，并将按钮加入到窗口MainWindow中
        self.text_btn = QtWidgets.QPushButton('OK', MainWindow)
        self.text_btn.setFont(QtGui.QFont('Microsoft YaHei', 10))
        self.text_btn.setGeometry(200, 620, 50, 25)
        self.text_btn.setStyleSheet(
            "QPushButton{color:rgb(255,255,255)}"
            "QPushButton{background-color:rgb(124,179,66)}"
            "QPushButton{border: 2px solid rgb(100,100,100)}"
            "QPushButton:hover{background-color:rgb(104,159,56)}"
            "QPushButton:pressed{background-color:rgb(51,105,30)}")

        # 创建重置按钮
        self.clear_btn = QtWidgets.QPushButton('Reset', MainWindow)
        self.clear_btn.setFont(QtGui.QFont('Microsoft YaHei', 9))
        self.clear_btn.setGeometry(500, 640, 60, 25)
        self.clear_btn.setStyleSheet(
            "QPushButton{color:rgb(80,80,80)}"
            "QPushButton{background-color:rgb(190,190,190)}"
            "QPushButton{border: 2px solid rgb(130,130,130)}"
            "QPushButton:hover{background-color:rgb(150,150,150)}"
            "QPushButton:pressed{background-color:rgb(130,130,130)}")

        self.stop_btn = QtWidgets.QPushButton('stop', MainWindow)
        self.stop_btn.setFont(QtGui.QFont('Microsoft YaHei', 10))
        self.stop_btn.setGeometry(500, 600, 60, 25)
        self.stop_btn.setStyleSheet(
            "QPushButton{color:rgb(255,255,255)}"
            "QPushButton{background-color:rgb(124,179,66)}"
            "QPushButton{border: 2px solid rgb(100,100,100)}"
            "QPushButton:hover{background-color:rgb(104,159,56)}"
            "QPushButton:pressed{background-color:rgb(51,105,30)}")

        self.start_btn = QtWidgets.QPushButton('start', MainWindow)
        self.start_btn.setFont(QtGui.QFont('Microsoft YaHei', 10))
        self.start_btn.setGeometry(500, 560, 60, 25)
        self.start_btn.setStyleSheet(
            "QPushButton{color:rgb(255,255,255)}"
            "QPushButton{background-color:rgb(124,179,66)}"
            "QPushButton{border: 2px solid rgb(100,100,100)}"
            "QPushButton:hover{background-color:rgb(104,159,56)}"
            "QPushButton:pressed{background-color:rgb(51,105,30)}")



    def caidan(self, MainWindow):
        # 添加菜单——模式按钮：可选首次适应算法或最佳适应算法
        self.menu_bar = QMainWindow.menuBar(MainWindow)
        self.menu_info = {"进程调度": {}, "程序装入": {}, "内存分配": {}}
        self.SchedulingBar = self.menu_bar.addMenu("进程调度")
        self.LoadingBar = self.menu_bar.addMenu("程序装入")
        self.AllocationBar = self.menu_bar.addMenu("内存分配")
        self.menu_bar.setFont(QtGui.QFont('KaiTi_GB2312', 12, 53))
        self.menu_bar.setStyleSheet(
            "QMenuBar::item { \
                color: rgb(255,255,255);  /*字体颜色*/ \
                border: 2px solid rgb(245,255,250); \
                background-color:rgb(124,179,66);\
            } \
            QMenuBar::item:selected { \
                border: 2px solid rgb(66,66,66); \
                background-color:rgb(51,105,30);/*选中的样式*/ \
            } \
            QMenuBar::item:pressed {/*菜单项按下效果*/ \
                border: 2px solid rgb(66,66,66); \
                background-color: rgb(51,105,30); \
            }")
        ##########################################################################
        self.FcfsBar = QtWidgets.QWidgetAction(MainWindow, checkable=True)
        self.FcfsAction = QtWidgets.QLabel("FCFS")
        self.add_menu(self.SchedulingBar, self.FcfsBar, self.FcfsAction)
        self.SjfBar = QtWidgets.QWidgetAction(MainWindow, checkable=True)
        self.SjfAction = QtWidgets.QLabel("SJF")
        self.add_menu(self.SchedulingBar, self.SjfBar, self.SjfAction)
        self.RotaryBar = QtWidgets.QWidgetAction(MainWindow, checkable=True)
        self.RotaryAction = QtWidgets.QLabel("轮转调度")
        self.add_menu(self.SchedulingBar, self.RotaryBar, self.RotaryAction)
        self.PriorityBar = QtWidgets.QWidgetAction(MainWindow, checkable=True)
        self.PriorityAction = QtWidgets.QLabel("优先级调度")
        self.add_menu(self.SchedulingBar, self.PriorityBar, self.PriorityAction)

        ##########################################################################
        self.AbsoluteLoadBar = QtWidgets.QWidgetAction(MainWindow, checkable=True)
        self.AbsoluteLoadAction = QtWidgets.QLabel("绝对装入")
        self.add_menu(self.LoadingBar, self.AbsoluteLoadBar, self.AbsoluteLoadAction)
        self.RelocatableLoadBar = QtWidgets.QWidgetAction(MainWindow, checkable=True)
        self.RelocatableLoadAction = QtWidgets.QLabel("可重定位装入 ")
        self.add_menu(self.LoadingBar, self.RelocatableLoadBar, self.RelocatableLoadAction)
        self.Dynamic_LoadingBar = QtWidgets.QWidgetAction(MainWindow, checkable=True)
        self.Dynamic_LoadingAction = QtWidgets.QLabel("动态装入")
        self.add_menu(self.LoadingBar, self.Dynamic_LoadingBar, self.Dynamic_LoadingAction)

        ##########################################################################
        self.FixedBar = QtWidgets.QWidgetAction(MainWindow, checkable=True)
        self.FixedAction = QtWidgets.QLabel("固定分区")
        self.add_menu(self.AllocationBar, self.FixedBar, self.FixedAction)
        self.FirstFitBar = QtWidgets.QWidgetAction(MainWindow, checkable=True)
        self.FirstFitAction = QtWidgets.QLabel("首次适应")
        self.add_menu(self.AllocationBar, self.FirstFitBar, self.FirstFitAction)
        self.BestFitBar = QtWidgets.QWidgetAction(MainWindow, checkable=True)
        self.BestFitAction = QtWidgets.QLabel("最佳适应")
        self.add_menu(self.AllocationBar, self.BestFitBar, self.BestFitAction)



    def add_menu(self, father, Menu, Action):
        Menu.setChecked(True)
        font = QtGui.QFont()
        font.setFamily('KaiTi_GB2312')
        font.setPointSize(50)
        Action.setFont(font)
        Action.setStyleSheet(
            "QLabel { color: rgb(255,255,255);  /*字体颜色*/ \
                background-color:rgb(51,105,30);\
                }"
            "QLabel:hover{  background-color:rgb(51,105,30);/*选中的样式*/ \
                }"
        )
        Menu.setDefaultWidget(Action)
        father.addAction(Menu)
        self.menu_info[father.title()][Action.text()] = {}
        self.menu_info[father.title()][Action.text()]['bar'] = Menu
        self.menu_info[father.title()][Action.text()]['action'] = Action


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Voice Assistant"))