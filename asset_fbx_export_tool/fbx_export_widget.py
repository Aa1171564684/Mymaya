# coding=utf8
# Copyright (c) 2020 GVF

from PySide2 import QtWidgets, QtCore
import logging
import public_functions
from gvf_globals import task_globals
import mtou_func
import re



log = logging.getLogger('fbx_tool')
log.setLevel(level=logging.INFO)


class FbxExportWidget(QtWidgets.QWidget):
    log_signal = QtCore.Signal(str)

    def __init__(self, parent=public_functions.get_main_window('maya')):
        super(FbxExportWidget, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setObjectName('Export')
        self.setWindowTitle('FBX_EXPORT')
        self.setMinimumSize(360, 540)
        self.setStyleSheet("""QWidget {font-size:14px}""")
        main_lay = QtWidgets.QVBoxLayout(self)
        child_lay = QtWidgets.QHBoxLayout()
        self.fbx_path = ""

        grp_box = QtWidgets.QGroupBox(u"导出工具")
        grp_box_lay = QtWidgets.QVBoxLayout(grp_box)
        self.tracking_edit = QtWidgets.QTextEdit()
        self.tracking_edit.setText(u'必须选择需要导出的模型和路径再执行export')
        self.tracking_edit.setReadOnly(True)
        browse_lay = QtWidgets.QHBoxLayout()
        self.line_edit = QtWidgets.QLineEdit()
        self.browse_btn = QtWidgets.QPushButton("Browse")
        browse_lay.addWidget(self.line_edit)
        browse_lay.addWidget(self.browse_btn)
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
        self.clear_btn = QtWidgets.QPushButton('Clear')
        self.clear_btn.setStyleSheet("QPushButton{color:red}"
                                     "QPushButton:hover{color:black}"
                                     "QPushButton{background-color:rgb(255,255,78)}"
                                     "QPushButton{border:2px}"
                                     "QPushButton{border-radius:10px}"
                                     "QPushButton{padding:2px 4px}")
        self.export_btn.setFixedHeight(30)
        self.clear_btn.setFixedHeight(30)

        grp_box_lay.addWidget(self.tracking_edit)
        main_lay.addWidget(grp_box)
        main_lay.addLayout(browse_lay)
        main_lay.addLayout(child_lay)
        child_lay.addWidget(self.export_btn)
        child_lay.addWidget(self.clear_btn)
        main_lay.addSpacing(10)
        self.export_btn.clicked.connect(self.main_func)
        self.browse_btn.clicked.connect(self.do_browse)
        self.clear_btn.clicked.connect(self.clear_text)
        self.log_signal.connect(self.set_text)

    def main_func(self):
        grp_list=[]
        # 获取选择的物体名称
        select_mesh = mtou_func.select_mesh()

        file_path = mtou_func.get_file_name()
        if not select_mesh:
            return False

        if not self.fbx_path:
            QtWidgets.QMessageBox.information(self, u'提示', u'请选择导出路径', QtWidgets.QMessageBox.Ok)
            return False
            # 检查大纲内是否有组
        status_gp = mtou_func.get_group()
        if status_gp == 'group':
            button_gp = QtWidgets.QMessageBox.information(self, u'警告', u'大纲内有Group，请先处理',
                                                          QtWidgets.QMessageBox.Ok)
            if button_gp == QtWidgets.QMessageBox.Ok:
                grp_list.append('two_uv')
        if len(grp_list)>0:
            self.log_signal.emit(u'大纲内有Group，请先处理')
            raise RuntimeError(u'大纲内有Group，请先处理')
        success_list = []
        failed_list = []
        if file_path:
            for log_mesh in select_mesh:
                infor_list = []
                self.log_signal.emit(u'开始导出:' + log_mesh)
                # 检查模型边数
                face_edge_dict = mtou_func.query_face_dege(log_mesh)
                for key, value in face_edge_dict.items():
                    if value > 4:
                        infor_list.append(log_mesh + u'模型存在超过四边的面')
                        failed_list.append(log_mesh + u'模型存在超过四边的面')
                # 查询UV坐标
                uv_posi=mtou_func.check_uv_point(log_mesh)
                if uv_posi:
                    uv_num=[]
                    for uv in uv_posi:
                        if not 0<=uv<=1:
                            uv_num.append(uv)
                    if len(uv_num)>0:
                        #QtWidgets.QMessageBox.information(self, u'警告', u'所选模型存在UV超出第一象限',QtWidgets.QMessageBox.OK )
                        infor_list.append(log_mesh + u':所选模型存在UV超出第一象限')
                        failed_list.append(log_mesh + u':所选模型存在UV超出第一象限')
                else:
                    uv_posi_one=mtou_func.check_one_uv(log_mesh)
                    uv_num_one = []
                    for uv_one in uv_posi_one:
                        if not 0 <= uv_one <= 1:
                            uv_num_one.append(uv_one)
                    if len(uv_num_one) > 0:
                        #QtWidgets.QMessageBox.information(self, u'警告', u'所选模型存在UV超出第一象限', QtWidgets.QMessageBox.OK)
                        infor_list.append(log_mesh + u':所选模型存在UV超出第一象限')
                        failed_list.append(log_mesh + u':所选模型存在UV超出第一象限')
                # 检查模型面数
                face_num = mtou_func.check_face_num(log_mesh)
                if re.search(r'Assets/Char', file_path) and isinstance(face_num, int):
                    if face_num >= 500000:
                        button_char = QtWidgets.QMessageBox.information(self, u'警告', u'所选资产模型面数大于等于50万,是否继续导出？',
                                                                        QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
                                                                        QtWidgets.QMessageBox.Cancel)
                        if button_char == QtWidgets.QMessageBox.Ok:
                            pass
                        else:
                            self.log_signal.emit(log_mesh + u'已取消导出')
                            infor_list.append(log_mesh + u':用户取消导出面数大于等于50万的资产')
                            failed_list.append(log_mesh + u':用户取消导出面数大于等于50万的资产')
                if re.search(r'Assets/Envir', file_path) and isinstance(face_num, int):
                    if face_num >= 10000:
                        button_envir = QtWidgets.QMessageBox.information(self, u'警告', u'所选场景模型面数大于等于1万，是否继续导出？',
                                                                         QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
                                                                         QtWidgets.QMessageBox.Cancel)
                        if button_envir == QtWidgets.QMessageBox.Ok:
                            pass
                        else:
                            self.log_signal.emit(log_mesh + u'已取消导出')
                            infor_list.append(log_mesh + u':用户取消导出面数大于等于1万的场景')
                            failed_list.append(log_mesh + u':用户取消导出面数大于等于1万的场景')
                # 世界坐标归零
                mtou_func.reset_object_position(log_mesh)
                # UVset
                status_uv=mtou_func.check_uv_count(log_mesh)
                if status_uv=='warning':
                    button_uv = QtWidgets.QMessageBox.information(self, u'警告', log_mesh+u'不是2UV的模型，是否继续导出？',
                                                                     QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
                                                                     QtWidgets.QMessageBox.Cancel)
                    if button_uv == QtWidgets.QMessageBox.Ok:
                        pass
                    else:
                        self.log_signal.emit(log_mesh + u'已取消导出')
                        infor_list.append(log_mesh + u':用户取消导出不是2UV的模型')
                        failed_list.append(log_mesh + u':用户取消导出不是2UV的模型')

                # 检查重复UV
                overlap_uv = mtou_func.check_uv_overlap(log_mesh)
                if overlap_uv:
                    infor_list.append(log_mesh + u'所选单个模型存在UV重叠的面')
                    failed_list.append(log_mesh + u'所选单个模型存在UV重叠的面')
                # 检查点重合
                point_position_list = mtou_func.chech_point_overlap(log_mesh)
                final_point = []
                for point in point_position_list:
                    if point not in final_point:
                        final_point.append(point)
                    else:
                        infor_list.append(log_mesh + u':单个模型中有重合的点')
                        failed_list.append(log_mesh + u':单个模型中有重合的点')
                if len(infor_list) == 0:
                    # 导出fbx到自定义的路径
                    if self.fbx_path and not self.fbx_path == "":
                        mtou_func.set_export_argument(log_mesh, self.fbx_path)
                        success_list.append(log_mesh)
                        self.log_signal.emit(log_mesh + u'无错误，模型导出成功\n')
                    else:
                        QtWidgets.QMessageBox.information(self, u'提示', u'请输入导出FBX文件的路径', QtWidgets.QMessageBox.Ok)
                        self.log_signal.emit(u'请输入导出FBX文件的路径')

        else:
            QtWidgets.QMessageBox.information(self, u'提示', u'当前文件未保存', QtWidgets.QMessageBox.Ok)
            return 

        self.log_signal.emit(
            u'共有' + str(len(success_list)) + u'个成功 , ' + str(len(select_mesh) - len(success_list)) + u'个失败')
        self.log_signal.emit(u'失败的模型和原因:\n' + str(failed_list).decode('unicode_escape'))
        QtWidgets.QMessageBox.information(self, u'提示', u'导出完成', QtWidgets.QMessageBox.Ok)

    # def open_path(self):
    #     QtWidgets.QFileDialog.getOpenFileName(self, u'文件选择框', self.fbx_path, 'FBX files(*.fbx)')

    def set_text(self, msg):
        self.tracking_edit.insertPlainText(msg + '\n')

    def clear_text(self):
        self.tracking_edit.clear()

    def do_browse(self):
        self.fbx_path = mtou_func.get_export_path()
        if self.fbx_path:
            self.line_edit.setText(self.fbx_path)
        else:
            self.line_edit.clear()


def main():
    public_functions.delete_existed_maya_window('Export')
    ui = FbxExportWidget(parent=public_functions.get_main_window('maya'))
    ui.show()
