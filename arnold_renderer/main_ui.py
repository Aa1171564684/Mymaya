# coding:utf8
from PySide2 import QtWidgets, QtGui, QtCore
import maya.cmds as cmds
import mtoa.aovs as aovs

LGT_TYPE = [u'directionalLight', u'pointLight', u'ambientLight', u'spotLight', u'aiAreaLight', u'aiSkyDomeLight',
            u'aiMeshLight']
LAYER_TYPE = aovs.BUILTIN_AOVS
TEX_SIZE = [u'4096*4096', u'2048*2048', u'1920*1080', u'1280*720', u'960*540']
TEX_TYPE = [u'png', u'exr', u'jpeg']

btn_css = ["QPushButton{color:black}"
           "QPushButton:hover{color:red}"
           "QPushButton{background-color:gray}"
           "QPushButton{border:2px}"
           "QPushButton{border-radius:10px}"
           "QPushButton{padding:2px 4px}"]
com_css = ["QComboBox {font-family: Microsoft YaHei;}"
           "QComboBox {font-size: 20px;}"
           "QComboBox {font-weight: bold;}"
           "QComboBox {border-width: 5px;}"
           "QComboBox {border-style: solid;}"]


class MainUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)
        self.ui()

    def ui(self):
        self.setWindowTitle(u'毕业设计')
        self.setFixedSize(600, 700)
        self.setStyleSheet('font-size: 18PX')
        self.main_lay_v = QtWidgets.QVBoxLayout(self)

        self.qua_lay_v = QtWidgets.QVBoxLayout()
        self.qua_lay_h = QtWidgets.QHBoxLayout()
        self.quality_lab = QtWidgets.QLabel(u'设置渲染质量:')
        self.pe = QtGui.QPalette()
        self.pe.setColor(QtGui.QPalette.WindowText, QtCore.Qt.darkGray)
        self.quality_lab.setPalette(self.pe)
        self.quality_lab.setStyleSheet('QLabel{font-style: oblique;}'
                                       'QLabel{background:transparent;}'
                                       'QLabel{font-size: 15PX;}')
        self.quality_lab.setMaximumWidth(300)
        self.quality_lab.setMaximumHeight(30)
        self.quality_lab.setEnabled(True)
        self.quality_btn = QtWidgets.QPushButton(u'设置')
        self.quality_btn.setStyleSheet(btn_css[0])
        self.quality_btn_recovery = QtWidgets.QPushButton(u'恢复')
        self.quality_btn_recovery.setStyleSheet(btn_css[0])
        self.rad_high_quality = QtWidgets.QRadioButton(u'高')
        self.rad_medium_quality = QtWidgets.QRadioButton(u'中')
        self.rad_low_quality = QtWidgets.QRadioButton(u'低')
        self.qua_lay_h.addWidget(self.rad_low_quality)
        self.qua_lay_h.addWidget(self.rad_medium_quality)
        self.qua_lay_h.addWidget(self.rad_high_quality)
        self.qua_lay_h.addWidget(self.quality_btn_recovery)
        self.qua_lay_h.addWidget(self.quality_btn)
        self.qua_lay_v.addWidget(self.quality_lab)
        self.qua_lay_v.addLayout(self.qua_lay_h)

        self.attr_lay_h = QtWidgets.QHBoxLayout()
        self.cam_lab = QtWidgets.QLabel(u'摄像机')
        self.cam_lab.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        self.cam_btn_refresh = QtWidgets.QPushButton(u'刷新')
        self.cam_btn_refresh.setStyleSheet(btn_css[0])
        self.cam_type = QtWidgets.QComboBox()
        self.cam_type.setMinimumWidth(160)
        camera = cmds.ls(type='camera')
        for cam in camera:
            self.cam_type.addItem(cmds.listRelatives(cam, p=1)[0])
        self.cam_type.setStyleSheet(com_css[0])
        self.pixel_lab = QtWidgets.QLabel(u'图片尺寸')
        self.pixel_lab.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        self.pixel_type = QtWidgets.QComboBox()
        self.pixel_type.setMinimumWidth(150)
        for size in TEX_SIZE:
            self.pixel_type.addItem(size)
        self.pixel_type.setStyleSheet(com_css[0])
        self.attr_lay_h.addWidget(self.cam_btn_refresh)
        self.attr_lay_h.addWidget(self.cam_type)
        self.attr_lay_h.addWidget(self.cam_lab)
        self.attr_lay_h.addWidget(self.pixel_type)
        self.attr_lay_h.addWidget(self.pixel_lab)

        self.lgt_lay_v = QtWidgets.QVBoxLayout()
        self.lgt_lay_h = QtWidgets.QHBoxLayout()
        self.lgt_type = QtWidgets.QComboBox()
        self.lgt_list = QtWidgets.QListWidget()
        self.lgt_list.setStyleSheet("QListWidget{border-width: 5px;}"
                                    "QListWidget {border-style: solid;}")
        self.lgt_list.setStyleSheet("QListWidget::Item{padding-top:5px; padding-bottom:3px; }"
                                      "QListWidget::Item:hover{background:gray; }"
                                      "QListWidget::Item:selected{background:green; color:black; }")
        self.lgt_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lgt_type.setMinimumWidth(250)
        for lgt in LGT_TYPE:
            self.lgt_type.addItem(lgt)
        self.lgt_type.setStyleSheet(com_css[0])
        self.lgt_btn_refresh = QtWidgets.QPushButton(u'刷新')
        self.lgt_btn_creat = QtWidgets.QPushButton(u'创建灯光')
        self.lgt_btn_del = QtWidgets.QPushButton(u'删除所有灯光')
        self.lgt_btn_refresh.setStyleSheet(btn_css[0])
        self.lgt_btn_creat.setStyleSheet(btn_css[0])
        self.lgt_btn_del.setStyleSheet(btn_css[0])
        self.lgt_lay_h.addWidget(self.lgt_type)
        self.lgt_lay_h.addWidget(self.lgt_btn_refresh)
        self.lgt_lay_h.addWidget(self.lgt_btn_creat)
        self.lgt_lay_h.addWidget(self.lgt_btn_del)
        self.lgt_lay_v.addLayout(self.lgt_lay_h)
        self.lgt_lay_v.addWidget(self.lgt_list)

        self.layer_lay_v = QtWidgets.QVBoxLayout()
        self.layer_lay_h = QtWidgets.QHBoxLayout()
        self.layer_type = QtWidgets.QComboBox()
        self.layer_type.setMinimumWidth(250)
        for layer in LAYER_TYPE:
            self.layer_type.addItem(layer[0])
        self.layer_type.setStyleSheet(com_css[0])
        self.layer_btn_refresh = QtWidgets.QPushButton(u'刷新')
        self.layer_btn_creat = QtWidgets.QPushButton(u'添加分层')
        self.layer_btn_del = QtWidgets.QPushButton(u'删除所有分层')
        self.layer_btn_refresh.setStyleSheet(btn_css[0])
        self.layer_btn_creat.setStyleSheet(btn_css[0])
        self.layer_btn_del.setStyleSheet(btn_css[0])
        self.layer_list = QtWidgets.QListWidget()
        self.layer_list.setStyleSheet("QListWidget{border-width: 5px;}"
                                      "QListWidget {border-style: solid;}")
        self.layer_list.setStyleSheet("QListWidget::Item{padding-top:5px; padding-bottom:3px; }"
                                      "QListWidget::Item:hover{background:gray; }"
                                      "QListWidget::Item:selected{background:green; color:black; }")
        self.layer_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.layer_lay_h.addWidget(self.layer_type)
        self.layer_lay_h.addWidget(self.layer_btn_refresh)
        self.layer_lay_h.addWidget(self.layer_btn_creat)
        self.layer_lay_h.addWidget(self.layer_btn_del)
        self.layer_lay_v.addLayout(self.layer_lay_h)
        self.layer_lay_v.addWidget(self.layer_list)

        self.render_lay_v = QtWidgets.QVBoxLayout()
        self.render_lay_h = QtWidgets.QHBoxLayout()
        self.render_lay_h_h = QtWidgets.QHBoxLayout()
        self.render_tex_type = QtWidgets.QComboBox()
        for tex_format in TEX_TYPE:
            self.render_tex_type.addItem(tex_format)
        self.render_tex_type.setStyleSheet(com_css[0])
        self.render_prefix = QtWidgets.QLineEdit()
        self.render_prefix.setStyleSheet("QLineEdit{border-width: 5px;}"
                                         "QLineEdit {border-style: solid;}")
        self.render_prefix.setPlaceholderText(u'图片名')
        self.render_prefix.setMaximumWidth(150)
        self.render_line = QtWidgets.QLineEdit()
        self.render_line.setStyleSheet("QLineEdit{border-width: 5px;}"
                                       "QLineEdit {border-style: solid;}")
        self.render_line.setPlaceholderText(u'请选择渲染图片保存路径')
        self.render_line.setEnabled(False)
        self.render_browse_btn = QtWidgets.QPushButton(u'Browser')
        self.render_btn = QtWidgets.QPushButton(u'测试渲染')
        self.render_browse_btn.setStyleSheet(btn_css[0])
        self.render_btn.setStyleSheet(btn_css[0])
        self.render_btn.setEnabled(False)
        self.render_type = QtWidgets.QComboBox()
        self.render_type.setMinimumWidth(300)
        self.render_type.addItem(u'渲染静帧图片')
        self.render_type.addItem(u'渲染序列帧')
        self.render_type.setStyleSheet(com_css[0])
        self.render_batch_w = QtWidgets.QWidget()
        self.render_batch_h = QtWidgets.QHBoxLayout()
        self.render_batch_lab_st = QtWidgets.QLabel(u'开始帧:        ')
        self.render_batch_lab_end = QtWidgets.QLabel(u'结束帧:        ')
        self.render_batch_lab_st.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        self.render_batch_lab_end.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        self.render_batch_line_st = QtWidgets.QLineEdit()
        self.render_batch_line_end = QtWidgets.QLineEdit()
        self.render_batch_line_st.setStyleSheet("QLineEdit{border-width: 5px;}"
                                                "QLineEdit {border-style: solid;}")
        self.render_batch_line_end.setStyleSheet("QLineEdit{border-width: 5px;}"
                                                 "QLineEdit {border-style: solid;}")
        self.render_batch_h.addWidget(self.render_batch_lab_st)
        self.render_batch_h.addWidget(self.render_batch_line_st)
        self.render_batch_h.addWidget(self.render_batch_lab_end)
        self.render_batch_h.addWidget(self.render_batch_line_end)
        self.render_batch_w.setLayout(self.render_batch_h)
        self.render_batch_w.hide()
        self.render_lay_h.addWidget(self.render_tex_type)
        self.render_lay_h.addWidget(self.render_prefix)
        self.render_lay_h.addWidget(self.render_line)
        self.render_lay_h.addWidget(self.render_browse_btn)
        self.render_lay_h_h.addWidget(self.render_type)
        self.render_lay_h_h.addWidget(self.render_btn)
        self.render_lay_v.addWidget(self.render_batch_w)
        self.render_lay_v.addLayout(self.render_lay_h)
        self.render_lay_v.addLayout(self.render_lay_h_h)

        self.frame_one = QtWidgets.QFrame()
        self.frame_one.setFrameStyle(QtWidgets.QFrame.HLine | QtWidgets.QFrame.Raised)
        self.frame_two = QtWidgets.QFrame()
        self.frame_two.setFrameStyle(QtWidgets.QFrame.HLine | QtWidgets.QFrame.Raised)
        self.frame_thr = QtWidgets.QFrame()
        self.frame_thr.setFrameStyle(QtWidgets.QFrame.HLine | QtWidgets.QFrame.Raised)
        self.frame_four = QtWidgets.QFrame()
        self.frame_four.setFrameStyle(QtWidgets.QFrame.HLine | QtWidgets.QFrame.Raised)

        self.main_lay_v.addLayout(self.qua_lay_v)
        self.main_lay_v.addWidget(self.frame_one)
        self.main_lay_v.addLayout(self.attr_lay_h)
        self.main_lay_v.addWidget(self.frame_thr)
        self.main_lay_v.addLayout(self.lgt_lay_v)
        self.main_lay_v.addWidget(self.frame_two)
        self.main_lay_v.addLayout(self.layer_lay_v)
        self.main_lay_v.addWidget(self.frame_four)
        self.main_lay_v.addLayout(self.render_lay_v)

        self.render_type.currentIndexChanged.connect(self.render_batch_ui)

    def render_batch_ui(self):
        if self.render_type.currentText() == u'渲染序列帧':
            self.render_batch_w.show()
        elif self.render_type.currentText() == u'渲染静帧图片':
            self.render_batch_w.hide()


if __name__ == '__main__':
    ui = MainUI()
    ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    ui.show()
