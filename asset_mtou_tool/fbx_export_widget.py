# coding=utf8
# Copyright (c) 2020 GVF

import sys
import re
import os
import json
import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore,QtGui
import logging
import public_functions
from gvf_globals import task_globals
import mtou_func

if not task_globals.task_id:
    msg = u"请先在任务系统选择对应镜头任务"
    raise RuntimeError(msg)

log = logging.getLogger('fbx_tool')
log.setLevel(level=logging.INFO)

QtWidgets.QMessageBox.information(None, u'提示', u'必须选择需要导出FBX的模型再执行export')

public_functions.delete_existed_maya_window('Export')


class FbxExportWidget(QtWidgets.QWidget):
    log_signal = QtCore.Signal(str)

    def __init__(self, parent=public_functions.get_main_window('maya')):
        super(FbxExportWidget, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setObjectName('Export')
        self.setWindowTitle('FBX_EXPORT')
        self.setMinimumSize(360,540)
        self.setStyleSheet("""QWidget {font-size:14px}""")
        main_lay = QtWidgets.QVBoxLayout(self)
        child_lay = QtWidgets.QHBoxLayout()

        grp_box = QtWidgets.QGroupBox(u"导出工具")
        grp_box_lay = QtWidgets.QVBoxLayout(grp_box)
        self.tracking_edit = QtWidgets.QTextEdit()
        self.tracking_edit.setText(u'必须选择需要导出的模型再执行export')
        self.tracking_edit.setReadOnly(True)
        self.line_edit = QtWidgets.QLineEdit(u'请输入导出路径和模型的FBX文件名称,eg:D:\\test.fbx')
        self.line_edit.setStyleSheet(("QLineEdit{color:green}"
                                    "QLineEdit:hover{color:red}"
                                    "QLineEdit{background-color:rgb(128,185,195)}"
                                    "QLineEdit{border:10px}"
                                    "QLineEdit{border-radius:3px}"
                                    "QLineEdit{padding:2px 1px}"))
        self.export_btn = QtWidgets.QPushButton("Export")
        self.export_btn.setStyleSheet("QPushButton{color:black}"
                                  "QPushButton:hover{color:red}"
                                  "QPushButton{background-color:rgb(78,255,255)}"
                                  "QPushButton{border:2px}"
                                  "QPushButton{border-radius:10px}"
                                  "QPushButton{padding:2px 4px}"
                                  "QPushButton{font-size:18px}")
        self.find_path = QtWidgets.QPushButton('Open')
        self.find_path.setStyleSheet("QPushButton{color:green}"
                                      "QPushButton:hover{color:red}"
                                      "QPushButton{background-color:rgb(255,78,255)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:10px}"
                                      "QPushButton{padding:2px 4px}"
                                      "QPushButton{font-size:18px}")
        self.clear_btn = QtWidgets.QPushButton('Clear')
        self.clear_btn.setStyleSheet("QPushButton{color:red}"
                                     "QPushButton:hover{color:black}"
                                     "QPushButton{background-color:rgb(255,255,78)}"
                                     "QPushButton{border:2px}"
                                     "QPushButton{border-radius:10px}"
                                     "QPushButton{padding:2px 4px}")
        self.export_btn.setFixedHeight(30)
        self.find_path.setFixedHeight(30)
        self.clear_btn.setFixedHeight(30)

        grp_box_lay.addWidget(self.tracking_edit)
        main_lay.addWidget(grp_box)
        main_lay.addWidget(self.line_edit)
        main_lay.addLayout(child_lay)
        child_lay.addWidget(self.export_btn)
        child_lay.addWidget(self.find_path)
        child_lay.addWidget(self.clear_btn)
        main_lay.addSpacing(10)
        self.export_btn.clicked.connect(self.main_func)
        self.line_edit.textChanged.connect(self.set_path)
        self.find_path.clicked.connect(self.open_path)
        self.clear_btn.clicked.connect(self.clear_text)
        self.log_signal.connect(self.set_text)

    def main_func(self):
        infor_list = []
        # 获取选择的物体名称
        select_mesh = mtou_func.select_mesh()
        # 检查模型面数
        status = mtou_func.check_face_num(select_mesh)
        if status == 'char':
            log.warning(u'所选模型面数大于等于50万')
            self.log_signal.emit(u'所选模型面数大于等于50万')
            button_char = QtWidgets.QMessageBox.information(self, u'警告', u'所选资产模型面数大于等于50万,是否继续导出？',
                                                            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
                                                            QtWidgets.QMessageBox.Cancel)
            if button_char == QtWidgets.QMessageBox.Ok:
                pass
            else:
                log.warning(u'已取消导出资产')
                self.log_signal.emit(u'已取消导出资产')
                infor_list.append('50')
        elif status == 'envir':
            log.warning(u'所选场景面数大于等于1万')
            self.log_signal.emit(u'所选场景面数大于等于1万')
            button_envir = QtWidgets.QMessageBox.information(self, u'警告', u'所选场景模型面数大于等于1万，是否继续导出？',
                                                             QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
                                                             QtWidgets.QMessageBox.Cancel)
            if button_envir == QtWidgets.QMessageBox.Ok:
                pass
            else:
                log.warning(u'已取消导出场景')
                self.log_signal.emit(u'已取消导出场景')
                infor_list.append('1')
        elif status == 'error':
            log.error(u'请检查是否选择模型或者场景是否成功进入任务系统')
            self.log_signal.emit(u'请检查是否选择模型或者场景是否成功进入任务系统')
            infor_list.append('no')
            raise RuntimeError(u'请检查是否选择模型或者场景是否成功进入任务系统')
        else:
            log.info(u'模型面数正常')
            self.log_signal.emit(u'模型面数正常')
        # 检查世界坐标及uvset
        if mtou_func.reset_object_position(select_mesh) == True:
            log.info(u'世界坐标已归零，模型没有超过UV')
            self.log_signal.emit(u'世界坐标已归零，模型没有超过UV')
        # 检查重复UV
        overlap_uv = mtou_func.check_uv_overlap(select_mesh)
        if overlap_uv == None:
            log.info(u"没有UV重复的面")
            self.log_signal.emit(u"没有UV重复的面")
        else:
            QtWidgets.QMessageBox.information(self, u'警告', u'模型存在UV重复的面', QtWidgets.QMessageBox.Ok)
            log.error(u'模型存在UV重复的面')
            self.log_signal.emit(u'模型存在UV重复的面')
            infor_list.append('UV')
            raise RuntimeError(u'模型存在UV重复的面')
        # 检查模型边数
        face_edge_dict = mtou_func.query_face_dege(select_mesh)
        normal_list = []
        for key, value in face_edge_dict.items():
            if value > 4:
                QtWidgets.QMessageBox.information(self, u'警告', u'模型存在超过四边的面', QtWidgets.QMessageBox.Ok)
                log.error(u'模型存在超过四边的面')
                self.log_signal.emit(u'模型存在超过四边的面')
                infor_list.append('four')
                raise RuntimeError(u'模型存在超过四边的面')

            else:
                normal_list.append(key)
        if len(normal_list) > 0:
            log.info(u'模型面边数正常')
            self.log_signal.emit(u'模型面边数正常')
        # 检查点重合
        point_position_list = mtou_func.chech_point_overlap(select_mesh)
        final_point = []
        for point in point_position_list:
            if point not in final_point:
                final_point.append(point)
            else:
                QtWidgets.QMessageBox.information(self, u'警告', u'模型有重合的点', QtWidgets.QMessageBox.Ok)
                log.error(u'模型有重合的点')
                self.log_signal.emit(u'模型有重合的点')
                infor_list.append('point')
                raise RuntimeError(u'模型有重合的点')
        if len(final_point) == len(point_position_list):
            log.info(u'模型没有重合点')
            self.log_signal.emit(u'模型没有重合点')
        if len(infor_list) == 0:
            # 导出fbx到自定义的路径
            try:
                mtou_func.set_export_argument(select_mesh, self.fbx_path)
                QtWidgets.QMessageBox.information(self, u'恭喜', u'导出成功', QtWidgets.QMessageBox.Ok)
                log.info(u'模型导出成功')
                self.log_signal.emit(u'模型导出成功')
            except:
                QtWidgets.QMessageBox.information(self, u'提示', u'请输入导出FBX文件的路径', QtWidgets.QMessageBox.Ok)
                log.warning(u'请输入导出FBX文件的路径')
                self.log_signal.emit(u'请输入导出FBX文件的路径')

    def open_path(self):
        QtWidgets.QFileDialog.getOpenFileName(self, u'文件选择框', self.fbx_path, 'FBX files(*.fbx)')

    def set_text(self, msg):
        # process_msg = "<font color=#13CE66><b>[Clean]</b></font>" + " <b>{0}</b> is clean!<br />".format(msg)
        # self.tracking_edit.insertHtml(process_msg)
        self.tracking_edit.insertPlainText(msg + '\n')

    def set_path(self):
        self.fbx_path = self.line_edit.text()

    def clear_text(self):
        self.tracking_edit.clear()



# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     ui = FbxExportWidget()
#     ui.show()
#     app.exec_()
