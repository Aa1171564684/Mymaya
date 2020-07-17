# coding=utf8
# Copyright (c) 2019 GVF

import ctypes
import hashlib
import os
import re
import sys
import time
import json
import subprocess
from ctypes.wintypes import MAX_PATH
from PySide import QtGui, QtCore
import monitor_func

PY_NAME = "node_thread.py"
ENV_NAME = "env_thread.py"
MAYA_PY_PATH = '"C:\\Program Files\\Autodesk\\Maya2017\\bin\\mayapy.exe"'
DEV_RUN_PY_PATH = os.path.join("D:/gvfpipe/dcc_ops/maya/scripts/maya_Monitor/", PY_NAME)
ENV_RUN_PY_PATH = os.path.join("D:/gvfpipe/dcc_ops/maya/scripts/maya_Monitor/", ENV_NAME)
CMD_COMMAND = "{} {}".format(MAYA_PY_PATH, DEV_RUN_PY_PATH)
ENV_COMMAND = "{} {}".format(MAYA_PY_PATH, ENV_RUN_PY_PATH)


# sys，env子线程
class EnvThread(QtCore.QThread):
    env_sign = QtCore.Signal(str)
    env_sign_two = QtCore.Signal(int)
    env_sign_thr = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(EnvThread, self).__init__(parent)

        self.env_path = None
        self.the_on = True

    # 获取路径
    def get_env(self, path):
        if path:
            self.env_path = path

    def run(self):
        self.sleep(10)
        while self.the_on:
            if re.search('.ma', str(self.env_path)) or re.search('.mb', str(self.env_path)):
                # 配置环境执行操作
                run_command = ENV_COMMAND + ' ' + self.env_path
                p = subprocess.Popen(run_command, shell=True, stdout=subprocess.PIPE)
                stdout = p.stdout.readlines()[1:]
                if re.search(r'env is normal', str(stdout)):
                    if re.search(r'sys is normal', str(stdout)):
                        self.env_sign_two.emit(1)
                        self.env_sign_thr.emit(self.env_path + '\n' + 'No problem')
                    else:
                        self.env_sign.emit(self.env_path + '\n' + str(stdout))
                else:
                    self.env_sign.emit(self.env_path + '\n' + str(stdout))
            else:
                # 配置环境执行操作
                for ma_path in list(monitor_func.search_files(self.env_path)):
                    run_command = ENV_COMMAND + ' ' + ma_path
                    p = subprocess.Popen(run_command, shell=True, stdout=subprocess.PIPE)
                    stdout = p.stdout.readlines()[1:]
                    if re.search(r'env is normal', str(stdout)):
                        if re.search(r'sys is normal', str(stdout)):
                            self.env_sign_two.emit(1)
                            self.env_sign_thr.emit(ma_path + '\n' + 'No problem')
                        else:
                            self.env_sign.emit(ma_path + '\n' + str(stdout))
                    else:
                        self.env_sign.emit(ma_path + '\n' + str(stdout))
            self.sleep(20)


# 文件子线程
class FodThread(QtCore.QThread):
    fod_sign = QtCore.Signal(str)
    fod_sign_two = QtCore.Signal(str)
    fod_sign_thr = QtCore.Signal(int)
    list_spt = []
    list_my_spt = []
    list_install = []
    list_modu = []

    def __init__(self, parent=None):
        super(FodThread, self).__init__(parent)
        self.thd_on = True

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
                pttq_path4 = buf.value + r'\maya\2017\modules'
                for root, dirs, files in os.walk(pttq_path1):
                    if re.search(r'userSetup',str(files)):
                        self.fod_sign.emit(str(pttq_path1)+'    Find userSetup!!!')
                for root, dirs, files in os.walk(pttq_path2):
                    if re.search(r'userSetup',str(files)):
                        self.fod_sign.emit(str(pttq_path2)+'    Find userSetup!!!')
                md5_inst = monitor_func.judge_time_fod(pttq_path3)
                if not self.list_install:
                    self.list_install.append(md5_inst)
                md5_spt = monitor_func.judge_time_fod(pttq_path1)
                if not self.list_spt:
                    self.list_spt.append(md5_spt)
                md5_my_spt = monitor_func.judge_time_fod(pttq_path2)
                if not self.list_my_spt:
                    self.list_my_spt.append(md5_my_spt)
                md5_modu = monitor_func.judge_time_fod(pttq_path4)
                if not self.list_modu:
                    self.list_modu.append(md5_modu)
                if md5_inst in self.list_install:
                    # self.fod_sign_two.emit('maya installation path is normal')
                    if md5_spt in self.list_spt:
                        # self.fod_sign_two.emit('The file ‘script’ in the maya document is normal')
                        if md5_my_spt in self.list_my_spt:
                            if md5_modu in self.list_modu:
                                self.fod_sign_two.emit('The file about maya is normal.')
                                self.fod_sign_thr.emit(1)
                            else:
                                self.fod_sign.emit("The file 'maya/2017/modules' in the maya document has changed")
                        else:
                            self.fod_sign.emit("The file 'maya/2017/script' in the maya document has changed")
                    else:
                        self.fod_sign.emit("The file 'maya/script' in the maya document has changed")
                else:
                    self.fod_sign.emit(" File changes under maya installation path")
            self.sleep(5)


# scriptNode子线程
class NodeThread(QtCore.QThread):
    node_sign = QtCore.Signal(str)
    node_sign_two = QtCore.Signal(int)
    node_sign_thr = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(NodeThread, self).__init__(parent)
        self.node_path = None
        self.thf_on = True

    def get_path(self, path):
        if path:
            self.node_path = path

    def run(self):
        self.sleep(10)
        while self.thf_on:
            if re.search('.ma', str(self.node_path)) or re.search('.mb', str(self.node_path)):
                run_command = CMD_COMMAND + ' ' + self.node_path
                proc = subprocess.Popen(run_command, shell=True, stdout=subprocess.PIPE)
                stdout_value = proc.stdout.readlines()[-1]
                if re.search(r'No problem', str(stdout_value)):
                    self.node_sign_two.emit(1)
                    self.node_sign_thr.emit(self.node_path + '\n' + 'No problem')
                else:
                    self.node_sign.emit(self.node_path + '\n' + str(stdout_value))
            else:
                for ma_path in list(monitor_func.search_files(self.node_path)):
                    run_command = CMD_COMMAND + ' ' + ma_path
                    proc = subprocess.Popen(run_command, shell=True, stdout=subprocess.PIPE)
                    stdout_value = proc.stdout.readlines()[-1]
                    if re.search(r'No problem', str(stdout_value)):
                        self.node_sign_two.emit(1)
                        self.node_sign_thr.emit(ma_path + '\n' + 'No problem')
                    else:
                        self.node_sign.emit(ma_path + '\n' + str(stdout_value))
            self.sleep(20)


# 自定义QLineEdit
class MLineEdit(QtGui.QLineEdit):

    def __init__(self, parent=None):
        super(MLineEdit, self).__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):

        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):

        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            if re.search(r'///', url.toString()):
                self.setText(url.toString().split('///')[-1].replace('\\', '/'))
            else:
                self.setText(url.toString().replace('\\', '/'))


# 主界面
class Main(QtGui.QWidget):
    error_json = []

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.node_thread = NodeThread()
        self.env_thread = EnvThread()
        self.fod_thread = FodThread()
        self.path = None

        self.setWindowTitle('MAYA_MONITOR')
        self.setMinimumHeight(500)
        self.setMinimumWidth(1000)
        self.setStyleSheet('Font-Size:15px')
        self.setWindowIcon(QtGui.QIcon("D:/speed.ico"))

        self.start_btn = QtGui.QPushButton('Start')
        self.start_btn.setEnabled(False)
        self.start_btn.setMaximumWidth(120)
        self.start_btn.setMinimumHeight(40)
        self.time_lab_s = QtGui.QLabel()
        self.time_lab_s.setFrameShape(QtGui.QFrame.Box)
        self.time_lab_s.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Sunken)
        self.time_lab_s.setLineWidth(2)
        self.time_lab_e = QtGui.QLabel()
        self.time_lab_e.setFrameShape(QtGui.QFrame.Box)
        self.time_lab_e.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Sunken)
        self.time_lab_e.setLineWidth(2)
        self.end_btn = QtGui.QPushButton('End')
        self.end_btn.setEnabled(False)
        self.end_btn.setMaximumWidth(120)
        self.end_btn.setMinimumHeight(40)

        frame_one = QtGui.QFrame()
        frame_one.setFrameShape(QtGui.QFrame.HLine)
        frame_one.setFrameStyle(QtGui.QFrame.HLine | QtGui.QFrame.Raised)
        frame_one.setFrameShadow(QtGui.QFrame.Raised)
        frame_one.setLineWidth(2)

        frame_two = QtGui.QFrame()
        frame_two.setFrameShape(QtGui.QFrame.HLine)
        frame_two.setFrameStyle(QtGui.QFrame.HLine | QtGui.QFrame.Raised)
        frame_two.setFrameShadow(QtGui.QFrame.Raised)
        frame_two.setLineWidth(2)

        self.path_line = MLineEdit()
        self.path_line.setPlaceholderText('Please enter the path to check')
        self.path_line.setMinimumHeight(40)
        self.brow_btn = QtGui.QPushButton('Browse')
        self.brow_btn.setMinimumWidth(120)
        self.brow_btn.setMinimumHeight(40)

        self.env_lab = QtGui.QLabel('Environ_Status:      ')
        self.env_lab.setStyleSheet('Font-Size:20px')
        self.env_lab.setMinimumHeight(50)
        self.env_lab.setFrameShape(QtGui.QFrame.Box)
        self.env_lab.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Sunken)
        self.env_lab.setLineWidth(2)
        self.env_text = QtGui.QTextEdit('Environ_Monitor:')
        self.env_text.setReadOnly(True)

        self.fod_lab = QtGui.QLabel('Folder_Status:')
        self.fod_lab.setStyleSheet('Font-Size:20px')
        self.fod_lab.setFrameShape(QtGui.QFrame.Box)
        self.fod_lab.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Sunken)
        self.fod_lab.setMinimumHeight(50)
        self.fod_lab.setLineWidth(2)
        self.fod_text = QtGui.QTextEdit('Folder_Monitor:')
        self.fod_text.setReadOnly(True)

        self.node_lab = QtGui.QLabel('Node_Status:')
        self.node_lab.setStyleSheet('Font-Size:20px')
        self.node_lab.setFrameShape(QtGui.QFrame.Box)
        self.node_lab.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Sunken)
        self.node_lab.setMinimumHeight(50)
        self.node_lab.setLineWidth(2)
        self.node_text = QtGui.QTextEdit('Node_Monitor:')
        self.node_text.setReadOnly(True)

        self.h_layout = QtGui.QHBoxLayout()
        self.h_layout_path = QtGui.QHBoxLayout()
        self.v_layout_env = QtGui.QVBoxLayout()
        self.v_layout_fod = QtGui.QVBoxLayout()
        self.v_layout_node = QtGui.QVBoxLayout()

        self.v_layout_env.addWidget(self.env_lab)
        self.v_layout_env.addWidget(self.env_text)
        self.v_layout_fod.addWidget(self.fod_lab)
        self.v_layout_fod.addWidget(self.fod_text)
        self.v_layout_node.addWidget(self.node_lab)
        self.v_layout_node.addWidget(self.node_text)
        self.h_layout_path.addWidget(self.path_line)
        self.h_layout_path.addWidget(self.brow_btn)

        self.h_layout.addWidget(self.end_btn)
        self.h_layout.addWidget(self.time_lab_s)
        self.h_layout.addWidget(self.time_lab_e)
        self.h_layout.addWidget(self.start_btn)

        main_layout = QtGui.QGridLayout(self)
        main_layout.setSpacing(10)
        main_layout.addLayout(self.h_layout, 0, 0, 1, 0)
        main_layout.addWidget(frame_one, 1, 0, 1, 0)
        main_layout.addLayout(self.h_layout_path, 2, 0, 1, 0)
        main_layout.addLayout(self.v_layout_env, 3, 1)
        main_layout.addLayout(self.v_layout_fod, 3, 0)
        main_layout.addLayout(self.v_layout_node, 3, 2)
        main_layout.addWidget(frame_two, 4, 0, 4, 0)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.show_time)

        self.start_btn.clicked.connect(self.show_lab)
        self.start_btn.clicked.connect(self.env_on)
        self.start_btn.clicked.connect(self.node_on)
        self.start_btn.clicked.connect(self.fod_on)
        self.start_btn.clicked.connect(self.reset_text)
        self.brow_btn.clicked.connect(self.get_path)
        self.end_btn.clicked.connect(self.hide_lab)
        self.end_btn.clicked.connect(self.over_thread)

        self.path_line.textChanged.connect(self.enter_path_one)

    def reset_text(self):
        self.start_btn.setEnabled(False)
        self.brow_btn.setEnabled(False)
        self.fod_text.setText('Folder_Monitor:')
        self.env_text.setText('Environ_Monitor:')
        self.node_text.setText('Node_Monitor:')
        self.fod_lab.setText('Folder_Status:')
        self.env_lab.setText('Environ_Status:')
        self.node_lab.setText('Node_Status:')

    def get_path(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, "请选择文件夹", "/")
        if directory:
            self.path_line.setText(directory)
        else:
            pass

    def enter_path_one(self):
        self.path = self.path_line.text()
        if self.path:
            self.start_btn.setEnabled(True)

    def show_time(self):
        datetime = QtCore.QDateTime.currentDateTime()
        text = datetime.toString()
        self.time_lab_e.setText('current_time:' + text)
        self.end_btn.setEnabled(True)
        self.path_line.setReadOnly(True)

    def show_lab(self):
        datetime = QtCore.QDateTime.currentDateTime()
        text = datetime.toString()
        self.time_lab_s.setText("start_time:" + text)
        self.timer.start()

    def hide_lab(self):
        self.timer.stop()

    def fod_on(self):
        self.fod_thread.start()
        self.fod_lab.setText('Folder_Status:' + 'Correct')
        if self.fod_thread.fod_sign.connect(self.fod_test_show):
            self.fod_thread.fod_sign_two.connect(self.no_fod_test_show)
        if self.fod_thread.fod_sign_thr:
            self.fod_thread.fod_sign_thr.connect(self.fod_true)

    def fod_test_show(self, msg):
        self.fod_lab.setText('Folder_Status:' + 'Wrong')
        self.fod_text.append(msg + '\n')
        self.error_json.append(msg)
        self.fod_text.setStyleSheet("color:red")

    def no_fod_test_show(self, msg):
        self.fod_text.append(msg + '\n')
        self.fod_text.setStyleSheet("color:black")

    def fod_true(self, msg):
        if msg == 1:
            self.fod_lab.setText('Folder_Status:' + 'Correct')

    def env_on(self):
        if self.path:
            self.env_thread.get_env(self.path)
        self.env_thread.start()
        if self.env_thread.env_sign:
            self.env_thread.env_sign.connect(self.env_test)
        if self.env_thread.env_sign_two:
            self.env_thread.env_sign_two.connect(self.env_test_status)
            self.env_thread.env_sign_thr.connect(self.env_test_true)

    def env_test_status(self, msg):
        if msg == 1:
            self.env_lab.setText('Environ_Status:' + 'Correct')
            self.env_text.setStyleSheet("color:black")

    def env_test_true(self, msg):
        self.env_text.append(msg)

    def env_test(self, msg):
        self.env_text.append(msg)
        self.error_json.append(msg)
        self.env_lab.setText('Environ_Status:' + 'Wrong')
        self.env_text.setStyleSheet("color:red")

    def node_on(self):
        if self.path:
            self.node_thread.get_path(self.path)
        self.node_thread.start()
        if self.node_thread.node_sign:
            self.node_thread.node_sign.connect(self.node_test)
        if self.node_thread.node_sign_two:
            self.node_thread.node_sign_two.connect(self.node_test_status)
            self.node_thread.node_sign_thr.connect(self.node_test_true)

    def node_test_status(self, msg):
        if msg == 1:
            self.node_lab.setText('Node_Status:' + 'Correct')
            self.node_text.setStyleSheet("color:black")

    def node_test_true(self, msg):
        self.node_text.append(msg)

    def node_test(self, msg):
        self.node_text.append(msg)
        self.error_json.append(msg)
        self.node_lab.setText('Node_Status:' + 'Wrong')
        self.node_text.setStyleSheet("color:red")

    def over_thread(self):
        self.env_text.setStyleSheet("color:black")
        self.node_text.setStyleSheet("color:black")
        self.path_line.setReadOnly(False)
        self.brow_btn.setEnabled(True)
        self.start_btn.setEnabled(True)
        self.fod_thread.thd_on = False
        self.fod_thread.exit()
        self.env_thread.the_on = False
        self.env_thread.exit()
        self.node_thread.thf_on = False
        self.node_thread.exit()

    def closeEvent(self, event):
        event.accept()
        if self.path:
            if self.error_json:
                monitor_func.creat_json(self.path,self.error_json)
        os._exit(0)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ui = Main()
    ui.show()
    app.exec_()
