# coding=utf8
# Copyright (c) 2019 GVF

import ctypes
import hashlib
import os
import re
import sys
import time
import win32con
from ctypes.wintypes import MAX_PATH
from PySide2 import QtWidgets, QtCore

qmut_env = QtCore.QMutex()  # 创建线程锁
qmut_nod = QtCore.QMutex()
qmut_fod = QtCore.QMutex()


class Env_Thread(QtCore.QThread):
    def __init__(self, parent=None):
        super(Env_Thread, self).__init__(parent)

        self.the_on = True

    def run(self):
        self.sleep(10)
        while self.the_on:
            pass
        self.sleep(5)


class Fod_Thread(QtCore.QThread):
    fod_sign = QtCore.Signal(str)
    fod_sign_two = QtCore.Signal(str)
    fod_sign_thr = QtCore.Signal(int)
    list_spt = []
    list_my_spt = []
    list_install = []

    def __init__(self, parent=None):
        super(Fod_Thread, self).__init__(parent)
        self.thd_on = True

    # def get_maya_location(self):
    #     '''
    #     获取maya安装目录
    #     :return: C:\Program Files\Autodesk\Maya2017
    #     '''
    #     list_install = []
    #     for i in (os.environ):
    #         if i == 'MAYA_LOCATION':
    #             list_install.append(i)
    #     if not list_install:
    #         # print u'系统未识别到MAYA_LOCATION'
    #         return False
    #     else:
    #         # print os.environ.get(list[0]) #maya安装目录
    #         return os.environ.get(list_install[0])

    def DFS_file_search(self, dict_name):
        '''
        获取该路径下所有文件的路径
        '''
        # list.pop() list.append()这两个方法就可以实现栈维护功能
        stack = []
        result_txt = []
        stack.append(dict_name)
        while len(stack) != 0:  # 栈空代表所有目录均已完成访问
            temp_name = stack.pop()
            try:
                temp_name2 = os.listdir(temp_name)  # list ["","",...]
                for eve in temp_name2:
                    stack.append(temp_name + "\\" + eve)  # 维持绝对路径的表达
            except:
                result_txt.append(temp_name)
        return result_txt
        # list.pop() list.append()这两个方法就可以实现栈维护功能
        stack = []
        result_txt = []
        stack.append(dict_name)
        while len(stack) != 0:  # 栈空代表所有目录均已完成访问
            temp_name = stack.pop()
            try:
                temp_name2 = os.listdir(temp_name)  # list ["","",...]
                for eve in temp_name2:
                    stack.append(temp_name + "\\" + eve)  # 维持绝对路径的表达
            except:
                result_txt.append(temp_name)
        return result_txt

    def judge_time(self, pttq_path):
        """

        Args:
            pttq_path:

        Returns:
                获取此文件的md5
        """
        pttq_path_list = []
        time_list = []  # pttq_path1下所有文件修改日期的列表
        for i in self.DFS_file_search(pttq_path):
            # print i
            file_time = time.ctime(os.stat(i).st_mtime)  # 文件的修改时间
            if file_time in time_list:
                pass
            else:
                time_list.append(file_time)
        for root_dir, sub_dir, sub_files in os.walk(pttq_path):
            if sub_dir:
                pttq_path_list.append(sub_dir)
            if sub_files:
                pttq_path_list.append(sub_files)
        m1 = hashlib.md5()
        m1.update(str(pttq_path_list) + str(time_list))
        md5 = m1.hexdigest()  # md5值
        return md5

    def run(self):
        '''

        Returns:
                判断文件是否变动
        '''
        while self.thd_on:
            dll = ctypes.windll.shell32
            buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
            if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
                # maya_version = re.findall('\d{4}', 'C:\Program Files\Autodesk\Maya2017')[0]
                pttq_path1 = buf.value + r'\maya\scripts'
                pttq_path2 = buf.value + r'\maya\2017\scripts'
                pttq_path3 = r'C:\Program Files\Autodesk\Maya2017'
                md5_inst = self.judge_time(pttq_path3)
                if not self.list_install:
                    self.list_install.append(md5_inst)
                md5_spt = self.judge_time(pttq_path1)
                if not self.list_spt:
                    self.list_spt.append(md5_spt)
                md5_my_spt = self.judge_time(pttq_path2)
                if not self.list_my_spt:
                    self.list_my_spt.append(md5_my_spt)
                if md5_inst in self.list_install:
                    # self.fod_sign_two.emit('maya installation path is normal')
                    if md5_spt in self.list_spt:
                        # self.fod_sign_two.emit('The file ‘script’ in the maya document is normal')
                        if md5_my_spt in self.list_my_spt:
                            self.fod_sign_two.emit('The file about maya is normal.')
                            self.fod_sign_thr.emit(1)
                        else:
                            self.fod_sign.emit("The file ‘maya2017/script’ in the maya document has changed")
                    else:
                        self.fod_sign.emit("The file ‘script’ in the maya document has changed")
                else:
                    self.fod_sign.emit(" File changes under maya installation path")
            self.sleep(10)

class Node_Thread(QtCore.QThread):
    node_sign=QtCore.Signal(str)

    def __init__(self, parent=None):
        super(Node_Thread, self).__init__(parent)

        self.thf_on = True

    def run(self):
        self.sleep(15)
        while self.thf_on:
            import maya.standalone as standalone
            standalone.initialize()
            import maya.cmds as cmds
            cmds.file('D:/Ball.ma', o=True, f=True,executeScriptNodes=False)  # 打开一个测试文件
            script_node = cmds.ls(typ='script')
            maya_env_list = []
            for key in os.environ.keys():
                if 'MAYA' in key:
                    maya_env_list.append(key)  # 获取maya相关的环境变量
            for script in script_node:  # 若环境变量存在于script node中，则打印出script node的名字
                for word in maya_env_list:
                    if word in cmds.getAttr(script + '.before'):
                        self.node_sign.emit(u'脚本节点: {0} 发现了环境变量名词 {1}.'.format(script,word))
            standalone.uninitialize()



class Env_widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Env_widget, self).__init__(parent)

        self.setWindowTitle('MAYA_MONITOR')
        self.setMinimumHeight(500)
        self.setMinimumWidth(1000)
        self.setStyleSheet('Font-Size:15px')

        # palette1 = QtGui.QPalette()
        # palette1.setColor(self.backgroundRole(),QtGui.QColor(2, 183, 53))
        # self.setPalette(palette1)

        self.start_btn = QtWidgets.QPushButton('Start')
        self.start_btn.setMaximumWidth(120)
        self.start_btn.setMinimumHeight(40)
        self.time_lab_s = QtWidgets.QLabel()
        self.time_lab_s.setFrameShape(QtWidgets.QFrame.Box)
        self.time_lab_s.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken)
        self.time_lab_s.setLineWidth(2)
        self.time_lab_e = QtWidgets.QLabel()
        self.time_lab_e.setFrameShape(QtWidgets.QFrame.Box)
        self.time_lab_e.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken)
        self.time_lab_e.setLineWidth(2)
        self.end_btn = QtWidgets.QPushButton('End')
        self.end_btn.setEnabled(False)
        self.end_btn.setMaximumWidth(120)
        self.end_btn.setMinimumHeight(40)

        frame_one = QtWidgets.QFrame()
        frame_one.setFrameShape(QtWidgets.QFrame.HLine)
        frame_one.setFrameStyle(QtWidgets.QFrame.HLine | QtWidgets.QFrame.Raised)
        frame_one.setFrameShadow(QtWidgets.QFrame.Raised)
        frame_one.setLineWidth(2)

        frame_two = QtWidgets.QFrame()
        frame_two.setFrameShape(QtWidgets.QFrame.HLine)
        frame_two.setFrameStyle(QtWidgets.QFrame.HLine | QtWidgets.QFrame.Raised)
        frame_two.setFrameShadow(QtWidgets.QFrame.Raised)
        frame_two.setLineWidth(2)

        self.env_lab = QtWidgets.QLabel('Environ_Status:      ')
        self.env_lab.setStyleSheet('Font-Size:20px')
        self.env_lab.setMinimumHeight(50)
        self.env_lab.setFrameShape(QtWidgets.QFrame.Box)
        self.env_lab.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken)
        self.env_lab.setLineWidth(2)
        self.env_text = QtWidgets.QTextEdit('Environ_Monitor:')
        self.env_text.setReadOnly(True)

        self.fod_lab = QtWidgets.QLabel('Folder_Status:')
        self.fod_lab.setStyleSheet('Font-Size:20px')
        self.fod_lab.setFrameShape(QtWidgets.QFrame.Box)
        self.fod_lab.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken)
        self.fod_lab.setMinimumHeight(50)
        self.fod_lab.setLineWidth(2)
        self.fod_text = QtWidgets.QTextEdit('Folder_Monitor:')
        self.fod_text.setReadOnly(True)

        self.node_lab = QtWidgets.QLabel('Node_Status:')
        self.node_lab.setStyleSheet('Font-Size:20px')
        self.node_lab.setFrameShape(QtWidgets.QFrame.Box)
        self.node_lab.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken)
        self.node_lab.setMinimumHeight(50)
        self.node_lab.setLineWidth(2)
        self.node_text = QtWidgets.QTextEdit('Node_Monitor:')
        self.node_text.setReadOnly(True)

        self.h_layout = QtWidgets.QHBoxLayout()
        self.v_layout_one = QtWidgets.QVBoxLayout()
        self.v_layout_two = QtWidgets.QVBoxLayout()
        self.v_layout_three = QtWidgets.QVBoxLayout()

        self.v_layout_one.addWidget(self.env_lab)
        self.v_layout_one.addWidget(self.env_text)
        self.v_layout_two.addWidget(self.fod_lab)
        self.v_layout_two.addWidget(self.fod_text)
        self.v_layout_three.addWidget(self.node_lab)
        self.v_layout_three.addWidget(self.node_text)

        self.h_layout.addWidget(self.end_btn)
        self.h_layout.addWidget(self.time_lab_s)
        self.h_layout.addWidget(self.time_lab_e)
        self.h_layout.addWidget(self.start_btn)

        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setSpacing(10)
        main_layout.addLayout(self.h_layout, 0, 0, 1, 0)
        main_layout.addWidget(frame_one, 1, 0, 1, 0)
        main_layout.addLayout(self.v_layout_one, 2, 1)
        main_layout.addLayout(self.v_layout_two, 2, 0)
        main_layout.addLayout(self.v_layout_three, 2, 2)
        main_layout.addWidget(frame_two, 3, 0, 3, 0)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.show_time)

        self.start_btn.clicked.connect(self.show_lab)
        self.start_btn.clicked.connect(self.env_mo)
        self.start_btn.clicked.connect(self.node_mo)
        self.start_btn.clicked.connect(self.fod_mo)
        self.end_btn.clicked.connect(self.hide_lab)
        self.end_btn.clicked.connect(self.over_thread)

    def check_sue(self):
        pass

    def show_time(self):
        datetime = QtCore.QDateTime.currentDateTime()
        text = datetime.toString()
        self.time_lab_e.setText('current_time:' + text)
        self.end_btn.setEnabled(True)

    def show_lab(self):
        datetime = QtCore.QDateTime.currentDateTime()
        text = datetime.toString()
        self.time_lab_s.setText("start_time:" + text)
        self.timer.start()

    def hide_lab(self):
        self.timer.stop()
        self.fod_text.setText('Folder_Monitor:')
        self.fod_lab.setText('Folder_Status:')
        self.env_text.setText('Environ_Monitor:')
        self.env_lab.setText('Environ_Status:')
        self.node_text.setText('Node_Monitor:')
        self.node_lab.setText('Node_Status:')



    def fod_mo(self):
        self.fod_thread = Fod_Thread()
        self.fod_thread.start()
        self.fod_lab.setText('Folder_Status:' + 'Correct')
        if self.fod_thread.fod_sign.connect(self.fod_test_show):
            self.fod_thread.fod_sign_two.connect(self.no_fod_test_show)
        if self.fod_thread.fod_sign_thr:
            self.fod_thread.fod_sign_thr.connect(self.fod_true)

    def fod_test_show(self, msg):
        self.fod_lab.setText('Folder_Status:' + 'Wrong')
        self.fod_text.append(msg + '\n')

    def no_fod_test_show(self, msg):
        self.fod_text.append(msg + '\n')

    def fod_true(self, msg):
        if msg == 1:
            self.fod_lab.setText('Folder_Status:' + 'Correct')

    def env_mo(self):
        self.start_btn.setEnabled(False)
        self.env_thread = Env_Thread()
        self.env_thread.start()

    def node_mo(self):
        self.node_thread = Node_Thread()
        self.node_thread.start()
        self.node_thread.node_sign.connect(self.node_test)

    def node_test(self, msg):
        self.node_text.append(msg)

    def over_thread(self):
        self.start_btn.setEnabled(True)
        self.fod_thread.thd_on = False
        self.fod_thread.exit()
        self.env_thread.the_on = False
        self.env_thread.exit()
        self.node_thread.thf_on = False
        self.node_thread.exit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Env_widget()
    ui.show()
    app.exec_()
