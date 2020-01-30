from PyQt5 import QtWidgets, QtGui, QtCore, uic
from UI import Ui_MainWindow
import sys
from functools import partial
from time import sleep
import threading
from PyQt5.QtWidgets import QVBoxLayout
import sip
from math import fabs
# import base64
# from memory_pic import *

sys.dont_write_bytecode = True

# def get_pic(pic_code, pic_name):
#     image = open(pic_name, 'wb')
#     image.write(base64.b64decode(pic_code))
#     image.close()
# get_pic(two_ico, "two.ico")
a = 1

def IsThisUse(action, bar, Flag=False):
    bar.setChecked(Flag)
    font = QtGui.QFont()
    font.setFamily("Calibri")
    font.setPointSize(10)
    action.setFont(font)
    if Flag:
        action.setStyleSheet(
            "QLabel { color: rgb(255,255,255);  /*字体颜色*/ \
                background-color:rgb(51,105,30);}"
            "QLabel:hover{  background-color:rgb(51,105,30);/*选中的样式*/ \
                }"
        )
    else:
        action.setStyleSheet(
            "QLabel { color: rgb(225,225,225);  /*字体颜色*/ \
                background-color:rgb(124,179,66);}"
            "QLabel:hover{ background-color:rgb(51,105,30);/*选中的样式*/ \
                            }"
)


class myWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(myWindow, self).__init__()
        # self.layout = QVBoxLayout()
        # self.setLayout(self.layout)
        self.setWindowTitle('毛智谦-操作系统原理')
        self.category = '内存分配'
        self.mode = '首次适应'
        self.myCommand = " "
        self.setWindowIcon(QtGui.QIcon('two.ico'))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # 输入框
        self.ui.text_btn.clicked.connect(self.text_changed)
        self.ui.textbox.returnPressed.connect(self.text_changed)
        self.ui.vtextbox.returnPressed.connect(self.v_changed)
        #
        for category in self.ui.menu_info:
            for mode in self.ui.menu_info[category]:
                self.ui.menu_info[category][mode]['bar'].triggered.connect(partial(self.recoginize, category, mode))

        self.ui.clear_btn.clicked.connect(self.clear)  # Reset按钮连接重置内存空间函数
        # 仅在进程调度使用
        self.ui.start_btn.clicked.connect(self.start)
        self.ui.stop_btn.clicked.connect(self.stop)

        for i in range(0, 64):
            self.ui.btnGroup[i].clicked.connect(partial(self.addNode, 10*(i+1)))

        self.Infor = {'进程调度': ['FCFS', 'SJF', '轮转调度', '优先级调度'],
                      '程序装入': ['绝对装入', '可重定位装入', '动态装入'],
                      '内存分配': ['固定分区', '首次适应', '最佳适应']}

        # 1表示可以处理作业但不能增删作业
        self.v = 1
        self.unit = 'k'
        self.flag = -1
        self.isbestFit = False  # 默认为首次匹配
        self.recoginize(self.category, self.mode)

    def mode_selection(self):
        self.isbestFit = True if self.mode == '最佳适应' else False
        self.unit = 's' if self.category == '进程调度' else 'k'
        for i in range(0, 64):
            self.ui.btnGroup[i].setText(str(10*i+10)+self.unit)
        self.ui.lable.setText('Process' if self.category == '内存分配' else 'Time')
        self.clear()
        self.ui.mode.setText("{}: {}".format(self.category, self.mode))
        # 根据self.category来决定UI界面
        if self.category == '进程调度':
            self.ui.vtextbox.show()
            self.ui.start_btn.show()
            self.ui.stop_btn.show()
        elif self.category == '内存分配':
            self.ui.vtextbox.hide()
            self.ui.start_btn.hide()
            self.ui.stop_btn.hide()
        # 调整按钮颜色，全设置为非选中
        for category in self.ui.menu_info.values():
            for mode in category.values():
                IsThisUse(mode['action'], mode['bar'])
        IsThisUse(self.ui.menu_info[self.category][self.mode]['action'],
                  self.ui.menu_info[self.category][self.mode]['bar'], True)

    def recoginize(self, category, mode):
        self.category, self.mode = category, mode
        self.mode_selection()

    '''将作业清除'''
    def clear(self):
        self.workNumber = 0
        self.nodeList = []
        self.nodeList.insert(0, {'number': -1,
                                 'start': 0,
                                 'length': 640,
                                 'isnull': True})
        self.nodeList[0]['btn'] = self.addButton(self.nodeList[0])

    # 寻找首次适应算法添加结点的位置
    def findFirstNode(self, length):
        self.targetNumber = -1
        for i in range(0, len(self.nodeList)):
            # 如果结点i为空闲 且 本节点长度大于作业需要长度
            if self.nodeList[i]['isnull'] and self.nodeList[i]['length'] >= length:
                self.targetNumber = i
                return self.targetNumber
        return -1

    def FCFSNode(self):
        for i in range(0, len(self.nodeList)):
            if not self.nodeList[i]['isnull']:
                return i
        return -1

    def SJFNode(self):
        Mini, mini = 0, 641
        for i in range(0, len(self.nodeList)):
            if self.nodeList[i]['length']<mini and not self.nodeList[i]['isnull']:
                Mini, mini = i, self.nodeList[i]['length']
        return Mini

    # 寻找最佳适应算法添加结点的位置
    def findBestNode(self, length):
        self.targetNumber, self.min = -1, 641
        for i in range(0, len(self.nodeList)):
            # 如果结点i为空闲且大于所需长度的情况下求最小值
            if self.nodeList[i]['isnull'] and (self.min > self.nodeList[i]['length'] >= length):
                self.min = self.nodeList[i]['length']
                self.targetNumber = i
        return self.targetNumber

    def findBestStartNode(self):
        pass

    # ##########################################################以上为基础函数
    # 添加结点
    def addNode(self, length):
        if self.flag != -1:
            return
        # 根据不同算法寻找合适的空闲结点
        # print(self.isbestFit)
        i = self.findBestNode(length) if self.isbestFit else self.findFirstNode(length)
        if i >= 0:
            # 该工作结点的number，在list中的位置最后将变为i
            self.workNumber += 1
            self.nodeList.insert(i+1, {'number': self.workNumber,
                                       'start': self.nodeList[i]['start'],
                                       'length': length,
                                       'isnull': False})
            self.nodeList[i+1]['btn'] = self.addButton(self.nodeList[i+1])
            # 若该空闲结点仍有残留空间，则后续剩余部分成为空闲结点
            if self.nodeList[i]['length'] > length:
                self.nodeList.insert(i+2, {'number': -1,
                                           'start': self.nodeList[i+1]['start']+length,
                                           'length': self.nodeList[i]['length']-length,
                                           'isnull': True})
                self.nodeList[i+2]['btn'] = self.addButton(self.nodeList[i+2])
            sip.delete(self.nodeList[i]['btn'])
            del self.nodeList[i]

    # 删除作业结点
    def deleteNode(self, workNumber):
        if self.flag !=-1:
            return
        self.current = -1
        for i in range(0, len(self.nodeList)):
            if self.nodeList[i]['number'] == workNumber:
                # 为了寻找self.list[current]['number'] = self.current
                self.current = i
                break
        if self.current != -1:
            # 前后都无空闲结点，则直接将自己转化为空闲结点
            if (self.current == 0 or not self.nodeList[self.current - 1]['isnull']) \
                    and (self.current == len(self.nodeList) - 1 or not self.nodeList[self.current + 1]['isnull']):
                self.nodeList.insert(self.current + 1, {'number': -1,  # 非作业结点
                                                        'start': self.nodeList[self.current]['start'],
                                                        'length': self.nodeList[self.current]['length'],
                                                        'isnull': True})  # 空闲
                self.nodeList[self.current + 1]['btn'] = self.addButton(self.nodeList[self.current+1])
                sip.delete(self.nodeList[self.current]['btn'])
                del self.nodeList[self.current]
            else:
                # 若节点前有空结点则合并
                if self.current >= 1 and self.nodeList[self.current-1]['isnull']:
                    self.nodeList.insert(self.current + 1, {'number': -1,
                                                            'start': self.nodeList[self.current - 1]['start'],
                                                            'length': self.nodeList[self.current-1]['length']
                                                                    + self.nodeList[self.current]['length'],
                                                            'isnull': True})
                    self.nodeList[self.current + 1]['btn'] = self.addButton(self.nodeList[self.current+1])
                    del self.nodeList[self.current - 1]['btn']
                    del self.nodeList[self.current - 1]
                    del self.nodeList[self.current - 1]['btn']
                    del self.nodeList[self.current - 1]
                    # 在原current位置插后插入后删除两个节点，新节点位置为current-1
                    self.current -= 1
                # 若结点后有空节点则合并
                if self.current < len(self.nodeList)-1 and self.nodeList[self.current+1]['isnull']:
                    self.nodeList.insert(self.current + 2, {'number': -1,  # 非作业结点
                                                            'start': self.nodeList[self.current]['start'],
                                                            'length': self.nodeList[self.current]['length']
                                                                    + self.nodeList[self.current + 1]['length'],
                                                            'isnull': True})  # 空闲
                    self.nodeList[self.current + 2]['btn'] = self.addButton(self.nodeList[self.current+2])
                    sip.delete(self.nodeList[self.current]['btn'])
                    del self.nodeList[self.current]
                    sip.delete(self.nodeList[self.current]['btn'])
                    del self.nodeList[self.current]

    # 将作业加入列表
    def addButton(self, node):
        if node['isnull']:  # 空闲结点按钮
            if self.category == '内存分配':
                show_info = str(node['length'])+self.unit
            elif self.category == '进程调度':
                show_info = str(node['length'])+'s'
            btn = QtWidgets.QPushButton(str(node['length'])+self.unit, self)
            btn.setFont(QtGui.QFont('Microsoft YaHei', int(node['length'] / 42) + 5))
            btn.setGeometry(380, 30+node['start'], 100, node['length'])
            btn.setStyleSheet(
                "QPushButton{color:rgb(150,150,150)}"
                "QPushButton{background-color:rgb(240,240,240)}"
                "QPushButton{border: 1.5px solid rgb(66,66,66);}")
        else:       # 作业结点按钮
            btn = QtWidgets.QPushButton('P'+str(node['number'])+':\n'+str(node['length'])+self.unit, self)
            btn.setFont(QtGui.QFont('Microsoft YaHei', int(node['length'] / 42) + 5))
            btn.setGeometry(380, 30 + node['start'], 100, node['length'])
            btn.setStyleSheet(
                "QPushButton{color:rgb(1,0,0)}"
                "QPushButton{background-color:rgb(124,179,66)}"
                "QPushButton:hover{background-color:rgb(210,210,210)}"
                "QPushButton:pressed{background-color:rgb(200,200,200)}"
                "QPushButton{border: 1.5px solid rgb(66,66,66);}")
            btn.clicked.connect(partial(self.deleteNode, node['number']))
        btn.show()
        # self.layout.addWidget(btn)
        return btn

    # 文本处理函数
    def text_changed(self):
        if self.ui.textbox.text() == '':
            self.content = 0
        else:
            self.content = 0
            self.content = int(self.ui.textbox.text())

        self.ui.textbox.setText('')
        if self.content <= 640:
            self.addNode(self.content)

    def v_changed(self):
        if self.ui.vtextbox.text() == '':
            self.v = 1
        else:
            self.v = 1
            self.v = int(self.ui.vtextbox.text()) + 1
        self.ui.textbox.setText('')

    def SwitchThread(self):
        while True:
            # 取消进程的标志，当点击stop时成立
            if self.flag == -1:
                break
            self.current = self.FCFSNode()
            if self.current == -1:
                break
            m = self.nodeList[self.current]['length']
            # k越大，速度越慢 k [1-9] 速度 [9-1]
            for i in range(0, m, 1):
                if self.current == 0:
                    self.nodeList.insert(0, {'number': -1,
                                             'start': 0,
                                             'length': 1,
                                             'isnull': True})
                    self.nodeList[0]['btn'] = self.addButton(self.nodeList[0])
                    self.current = 1
                else:
                    self.nodeList.insert(self.current, {'number': -1,
                                                        'start': self.nodeList[self.current - 1]['start'],
                                                        'length': self.nodeList[self.current - 1]['length'] + 1,
                                                        'isnull': True})
                    self.nodeList[self.current]['btn'] = self.addButton(self.nodeList[self.current])
                    sip.delete(self.nodeList[self.current - 1]['btn'])
                    del self.nodeList[self.current - 1]
                QtWidgets.QApplication.processEvents()
                if self.nodeList[self.current]['length'] > 1:
                    self.nodeList.insert(self.current + 1, {'number': -1,  # 非作业结点
                                                            'start': self.nodeList[self.current]['start'] + 1,
                                                            'length': self.nodeList[self.current]['length'] - 1,
                                                            'isnull': False})  # 空闲
                    self.nodeList[self.current + 1]['btn'] = self.addButton(self.nodeList[self.current + 1])
                sip.delete(self.nodeList[self.current]['btn'])
                del self.nodeList[self.current]
                sleep(0.025 / self.v)
                # print(self.v)
                QtWidgets.QApplication.processEvents()
                # print(self.nodeList)
            # and的短路机制
            if len(self.nodeList) > 1 and self.nodeList[self.current]['isnull']:
                self.current -= 1
                self.nodeList.insert(self.current + 2, {'number': -1,  # 非作业结点
                                                        'start': self.nodeList[self.current]['start'],
                                                        'length': self.nodeList[self.current]['length']
                                                                  + self.nodeList[self.current + 1]['length'],
                                                        'isnull': True})  # 空闲
                self.nodeList[self.current + 2]['btn'] = self.addButton(self.nodeList[self.current + 2])
                sip.delete(self.nodeList[self.current]['btn'])
                del self.nodeList[self.current]
                sip.delete(self.nodeList[self.current]['btn'])
                del self.nodeList[self.current]
        self.flag = -1
        QtWidgets.QApplication.processEvents()

    def start(self):
        self.flag = 1
        self.mao = threading.Thread(target=self.SwitchThread(), name='mao')

    def stop(self):
        self.flag = -1
        QtWidgets.QApplication.processEvents()

    def WorkUse(self,workNumber):
        self.current = -1
        for i in range(0, len(self.nodeList)):
            if self.nodeList[i]['number'] == workNumber:
                # 为了寻找self.list[current]['number'] = self.current
                self.current = i
                break

if __name__ == "__main__":
    app = 0
    app = QtWidgets.QApplication([])
    application = myWindow()
    application.show()
    sys.exit(app.exec_())
