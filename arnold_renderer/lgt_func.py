# coding:utf8
from PySide2 import QtWidgets, QtGui, QtCore
import maya.cmds as cmds
import shiboken2
import maya.OpenMayaUI as mul


def get_maya_widow():
    maya_ptr = mul.MQtUtil.mainWindow()
    maya_window = shiboken2.wrapInstance(long(maya_ptr), QtWidgets.QWidget)
    return maya_window


class LgtUI(QtWidgets.QWidget):
    def __init__(self, parent=get_maya_widow()):
        super(LgtUI, self).__init__(parent)

        # self.r_color_list = []
        # self.g_color_list = []
        # self.b_color_list = []
        self.slider_list = []

        self.setWindowFlags(QtCore.Qt.Window)
        self.setFixedSize(400, 400)
        self.setStyleSheet('font-size:15PX')
        self.setWindowTitle(u'灯光参数设置')

        self.lgt_color = QtWidgets.QLabel(u'灯光颜色')
        self.lgt_color.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken)
        self.lgt_intensity = QtWidgets.QLabel(u'灯光强度')
        self.lgt_intensity.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken)
        self.lgt_shadow_color = QtWidgets.QLabel(u'阴影颜色')
        self.lgt_shadow_color.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken)
        self.lgt_expouse = QtWidgets.QLabel(u'曝光度    ')
        self.lgt_expouse.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken)
        self.lgt_cast_shadow_btn = QtWidgets.QLabel(u'造成阴影')
        self.lgt_normalize = QtWidgets.QLabel(u'正常化')
        self.lgt_normalize.setAlignment(QtCore.Qt.AlignRight)
        self.lgt_intensity_sp = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.lgt_intensity_sp.setMaximum(1000)
        self.lgt_intensity_sp.setSingleStep(1)
        self.lgt_color_sp = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.lgt_color_sp.setMaximum(100)
        self.lgt_color_sp.setSingleStep(1)
        self.lgt_shadow_color_sp = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.lgt_shadow_color_sp.setMaximum(100)
        self.lgt_shadow_color_sp.setSingleStep(1)
        self.lgt_expouse_sp = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.lgt_expouse_sp.setMaximum(500)
        self.lgt_expouse_sp.setSingleStep(1)
        self.lgt_color_btn = QtWidgets.QPushButton()
        self.lgt_color_btn.setMaximumWidth(40)
        self.lgt_intensity_line = QtWidgets.QLineEdit()
        self.lgt_intensity_line.setMaximumWidth(40)
        self.lgt_shadow_color_btn = QtWidgets.QPushButton()
        self.lgt_shadow_color_btn.setMaximumWidth(40)
        self.lgt_expouse_line = QtWidgets.QLineEdit()
        self.lgt_expouse_line.setMaximumWidth(40)
        self.lgt_cast_shadow_btn_ch = QtWidgets.QCheckBox()
        self.lgt_cast_shadow_btn_ch.setChecked(True)
        self.lgt_normalize_ch = QtWidgets.QCheckBox()
        self.lgt_normalize_ch.setChecked(True)

        self.lgt_lay_child_g = QtWidgets.QGridLayout(self)
        self.lgt_lay_child_g.addWidget(self.lgt_color, 0, 0)
        self.lgt_lay_child_g.addWidget(self.lgt_color_btn, 0, 2)
        self.lgt_lay_child_g.addWidget(self.lgt_color_sp, 0, 3)
        self.lgt_lay_child_g.addWidget(self.lgt_intensity, 1, 0)
        self.lgt_lay_child_g.addWidget(self.lgt_intensity_line, 1, 2)
        self.lgt_lay_child_g.addWidget(self.lgt_intensity_sp, 1, 3)
        self.lgt_lay_child_g.addWidget(self.lgt_shadow_color, 2, 0)
        self.lgt_lay_child_g.addWidget(self.lgt_shadow_color_btn, 2, 2)
        self.lgt_lay_child_g.addWidget(self.lgt_shadow_color_sp, 2, 3)
        self.lgt_lay_child_g.addWidget(self.lgt_expouse, 3, 0)
        self.lgt_lay_child_g.addWidget(self.lgt_expouse_line, 3, 2)
        self.lgt_lay_child_g.addWidget(self.lgt_expouse_sp, 3, 3)
        self.lgt_lay_child_g.addWidget(self.lgt_cast_shadow_btn, 4, 0)
        self.lgt_lay_child_g.addWidget(self.lgt_cast_shadow_btn_ch, 4, 1)
        self.lgt_lay_child_g.addWidget(self.lgt_normalize, 4, 3)
        self.lgt_lay_child_g.addWidget(self.lgt_normalize_ch, 4, 4)

        self.lgt_color_sp.valueChanged.connect(self.color_sptobtn)
        self.lgt_color_btn.clicked.connect(self.color_btntosp)
        self.lgt_intensity_sp.valueChanged.connect(self.intensity_sptoline)
        self.lgt_intensity_line.textChanged.connect(self.intensity_linetosp)
        self.lgt_shadow_color_sp.valueChanged.connect(self.shadow_color_sptobtn)
        self.lgt_shadow_color_btn.clicked.connect(self.shadow_color_btntosp)
        self.lgt_expouse_sp.valueChanged.connect(self.expouse_sptoline)
        self.lgt_expouse_line.textChanged.connect(self.expouse_linetosp)
        self.lgt_normalize_ch.stateChanged.connect(self.normalize_set)
        self.lgt_cast_shadow_btn_ch.stateChanged.connect(self.cast_set)

    def color_sptobtn(self):
        slider = float(self.lgt_color_sp.value()) / 100
        r_color = None
        g_color = None
        b_color = None
        self.slider_list.append(slider)
        if self.slider_list[-1] > self.slider_list[-2]:
            r_color = (slider - self.slider_list[-2]) + self.slider_list[-2]
            g_color = (slider - self.slider_list[-2]) + self.slider_list[-2]
            b_color = (slider - self.slider_list[-2]) + self.slider_list[-2]
        elif self.slider_list[-1] < [-2]:
            r_color = self.slider_list[-2] - abs((slider - self.slider_list[-2]))
            g_color = self.slider_list[-2] - abs((slider - self.slider_list[-2]))
            b_color = self.slider_list[-2] - abs((slider - self.slider_list[-2]))

        if r_color == g_color == b_color == 0.0:
            for k in self.color_select:
                cmds.setAttr("%s.color" % k, 0, 0, 0, type='double3')
                self.lgt_color_btn.setStyleSheet('QPushButton{background-color:%s}' % (self.double3))

        else:
            for h in self.color_select:
                cmds.setAttr("%s.colorR" % h, r_color)
                cmds.setAttr("%s.colorG" % h, g_color)
                cmds.setAttr("%s.colorB" % h, 0.0)
                self.lgt_color_btn.setStyleSheet('QPushButton{background-color:%s}' % (self.double3))
                # cmds.setAttr("%s.color" % h, slider, slider, slider, type='double3')

    def color_btntosp(self):
        color = QtWidgets.QColorDialog.getColor()
        self.double3 = color.getRgbF()[:-1]
        if color.isValid():
            self.lgt_color_btn.setStyleSheet('QPushButton{background-color:%s}' % color.name())
            self.color_select = cmds.ls(sl=True)
            for i in self.color_select:
                cmds.setAttr("%s.color" % i, self.double3[0], self.double3[1], self.double3[2],
                             type='double3')
                self.slider_list.append(self.double3[2])
                self.lgt_color_sp.setValue(int(sorted(self.double3)[-1] * 100))
        else:
            pass

    def intensity_sptoline(self):
        self.intensity_select = cmds.ls(sl=1)
        for intensity in self.intensity_select:
            self.lgt_intensity_line.setText(str(float(self.lgt_intensity_sp.value()) / 10))
            cmds.setAttr("%s.intensity" % intensity, float(self.lgt_intensity_sp.value()) / 10)

    def intensity_linetosp(self):
        try:
            self.intensity_select = cmds.ls(sl=1)
            for intensity in self.intensity_select:
                self.lgt_intensity_sp.setValue(int(float(self.lgt_intensity_line.text()) * 10))
                cmds.setAttr("$s.intensity" % intensity, float(self.lgt_intensity_line.text()))
        except:
            pass

    def shadow_color_sptobtn(self):
        pass

    def shadow_color_btntosp(self):
        pass

    def expouse_sptoline(self):
        self.expouse_select = cmds.ls(sl=1)
        for expouse in self.expouse_select:
            self.lgt_expouse_line.setText(str(float(self.lgt_expouse_sp.value()) / 10))
            cmds.setAttr("%s.aiExposure" % expouse, float(self.lgt_expouse_sp.value()) / 10)

    def expouse_linetosp(self):
        try:
            self.expouse_select = cmds.ls(sl=1)
            for expouse in self.expouse_select:
                self.lgt_expouse_sp.setValue(int(float(self.lgt_expouse_line.text()) * 10))
                cmds.setAttr("%s.aiExposure" % expouse, float(self.lgt_expouse_line.text()))
        except:
            pass

    def normalize_set(self):
        self.normalize_select = cmds.ls(sl=1)
        for normalize in self.normalize_select:
            if self.lgt_normalize_ch.isChecked():
                cmds.setAttr("%s.aiNormalize" % normalize, 1)
            else:
                cmds.setAttr("%s.aiNormalize" % normalize, 0)

    def cast_set(self):
        self.cast_select = cmds.ls(sl=1)
        for cast in self.cast_select:
            if self.lgt_cast_shadow_btn_ch.isChecked():
                cmds.setAttr("%s.aiCastShadows" % cast, 1)
            else:
                cmds.setAttr("%s.aiCastShadows" % cast, 0)
# if __name__ == '__main__':
#     lgt = LgtUI()
#     lgt.show()
