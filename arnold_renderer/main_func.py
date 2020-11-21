# coding:utf-8
import sys
import re
from fuzzywuzzy import fuzz
from PySide2 import QtWidgets, QtGui, QtCore
from random import randint
import shiboken2
import maya.OpenMayaUI as mul
import maya.cmds as cmds
import pymel.core as pm
import mtoa.aovs as aovs
import mtoa.utils as mutils
import lgt_func

reload(lgt_func)
sys.path.append(r'D:\ruan_designer')
import main_ui

reload(main_ui)

LGT_TYPE = [u'directionalLight', u'pointLight', u'ambientLight', u'spotLight', u'aiAreaLight', u'aiSkyDomeLight',
            u'aiMeshLight']
LAYER_TYPE = aovs.BUILTIN_AOVS


def get_maya_widow():
    maya_ptr = mul.MQtUtil.mainWindow()
    maya_window = shiboken2.wrapInstance(long(maya_ptr), QtWidgets.QWidget)
    return maya_window


class MainFunc(main_ui.MainUI):
    def __init__(self, parent=get_maya_widow()):
        super(MainFunc, self).__init__(parent)
        self.qua = None

        self.setWindowFlags(QtCore.Qt.Window)
        self.setObjectName('design')
        self.rad_high_quality.clicked.connect(self.qua_high)
        self.rad_medium_quality.clicked.connect(self.qua_medium)
        self.rad_low_quality.clicked.connect(self.qua_low)
        self.quality_btn.clicked.connect(self.qua_creat)
        self.cam_btn_refresh.clicked.connect(self.cam_refresh)
        self.quality_btn_recovery.clicked.connect(self.quality_recovery)

        # lgt 右键菜单
        self.popMenu = QtWidgets.QMenu()
        self.lgt_modify = QtWidgets.QAction(u'修改灯光属性', self.popMenu)
        self.lgt_rename = QtWidgets.QAction(u'修改灯光名称', self.popMenu)
        self.lgt_del = QtWidgets.QAction(u'删除此灯光', self.popMenu)
        self.popMenu.addAction(self.lgt_modify)
        self.popMenu.addAction(self.lgt_rename)
        self.popMenu.addAction(self.lgt_del)
        self.lgt_modify.triggered.connect(self.lgt_modify_attribute)
        self.lgt_rename.triggered.connect(self.lgt_rename_item)
        self.lgt_del.triggered.connect(self.lgt_del_item)
        self.lgt_type.currentIndexChanged.connect(self.lgt_add_list)
        self.lgt_btn_creat.clicked.connect(self.lgt_creat)
        self.lgt_btn_del.clicked.connect(self.lgt_list_clear)
        self.lgt_list.itemClicked.connect(self.lgt_select)
        self.lgt_btn_refresh.clicked.connect(self.lgt_refresh)
        self.lgt_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # 设置listwidget的菜单上下文为自定义，即允许右键
        self.lgt_list.customContextMenuRequested[QtCore.QPoint].connect(self.lgt_list_menu)  # 右键触发函数，弹出菜单(menu）

        # layer 右键菜单
        self.popMenu_layer = QtWidgets.QMenu()
        self.layer_modify = QtWidgets.QAction(u'禁用层', self.popMenu_layer)
        self.layer_enable = QtWidgets.QAction(u'启用层', self.popMenu_layer)
        self.layer_del = QtWidgets.QAction(u'删除层', self.popMenu_layer)
        self.popMenu_layer.addAction(self.layer_enable)
        self.popMenu_layer.addAction(self.layer_modify)
        self.popMenu_layer.addAction(self.layer_del)
        self.layer_modify.triggered.connect(self.layer_modify_attribute)
        self.layer_enable.triggered.connect(self.layer_enable_attribute)
        self.layer_del.triggered.connect(self.layer_del_item)
        self.layer_list.itemClicked.connect(self.layer_select)
        self.layer_btn_refresh.clicked.connect(self.layer_refresh)

        self.layer_type.currentIndexChanged.connect(self.layer_add_list)
        self.layer_btn_creat.clicked.connect(self.layer_creat)
        self.layer_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # 设置listwidget的菜单上下文为自定义，即允许右键
        self.layer_list.customContextMenuRequested[QtCore.QPoint].connect(self.layer_list_menu)  # 右键触发函数，弹出菜单(menu）
        self.layer_btn_del.clicked.connect(self.layer_list_clear)

        # browser
        self.render_browse_btn.clicked.connect(self.render_folder)

        # test_render
        self.render_btn.clicked.connect(self.render)
        self.cam_type.currentIndexChanged.connect(self.render_camera)
        self.pixel_type.currentIndexChanged.connect(self.render_pixel)
        self.render_tex_type.currentIndexChanged.connect(self.render_format)
        self.render_prefix.textChanged.connect(self.render_file_name)
        self.render_batch_line_st.textChanged.connect(self.render_frame_st)
        self.render_batch_line_end.textChanged.connect(self.render_frame_end)
        self.tex_format = self.render_tex_type.itemText(0)
        if re.search(r'png', self.tex_format):
            cmds.setAttr("defaultArnoldDriver.ai_translator", 'png', type="string")
            cmds.setAttr("defaultArnoldDriver.pngFormat", 1)
        elif re.search(r'exr', self.tex_format):
            cmds.setAttr("defaultArnoldDriver.ai_translator", 'exr', type="string")
            # cmds.setAttr("defaultArnoldDriver.exrTiled",1)
        elif re.search(r'jpeg', self.tex_format):
            cmds.setAttr("defaultArnoldDriver.ai_translator", 'jpeg', type="string")
            # cmds.setAttr("defaultArnoldDriver.quality",100)

    def cam_refresh(self):
        cam_total = cmds.ls(type='camera')
        cam_type_total = []
        try:
            for i in range(self.cam_type.count()):
                cam_type_total.append(self.cam_type.itemText(i))
        except:
            pass
        for cam in cam_total:
            if cmds.listRelatives(cam, p=1)[0] in cam_type_total:
                pass
            else:
                self.cam_type.addItem(cmds.listRelatives(cam, p=1)[0])
                self.cam_type.setCurrentText(cmds.listRelatives(cam, p=1)[0])

        for ty in cam_type_total:
            if cmds.objExists(ty):
                pass
            else:
                for i in range(self.cam_type.count()):
                    if self.cam_type.itemText(i) == ty:
                        self.cam_type.removeItem(i)

    def quality_recovery(self):
        """
            恢复最初的参数设置
        Returns:

        """
        self.quality_lab.setText(u'设置渲染质量: ')
        # 设置camera,diffuse,specular,tranmission,sss,volume参数
        cmds.setAttr("defaultArnoldRenderOptions.AASamples", 3)
        cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples", 2)
        cmds.setAttr("defaultArnoldRenderOptions.GISpecularSamples", 2)
        cmds.setAttr("defaultArnoldRenderOptions.GITransmissionSamples", 2)
        cmds.setAttr("defaultArnoldRenderOptions.GISssSamples", 2)
        cmds.setAttr("defaultArnoldRenderOptions.GIVolumeSamples", 2)
        self.re_black = QtGui.QPalette()
        self.re_black.setColor(QtGui.QPalette.WindowText, QtCore.Qt.lightGray)
        self.rad_high_quality.setPalette(self.re_black)
        self.rad_medium_quality.setPalette(self.re_black)
        self.rad_low_quality.setPalette(self.re_black)

    def qua_high(self):
        if self.rad_high_quality.isChecked():
            self.qua = self.rad_high_quality.text()

    def qua_medium(self):
        if self.rad_medium_quality.isChecked():
            self.qua = self.rad_medium_quality.text()

    def qua_low(self):
        if self.rad_low_quality.isChecked():
            self.qua = self.rad_low_quality.text()

    def qua_creat(self):
        """
            设置渲染参数
        :return:
        """
        try:
            if self.qua == u'高':
                self.quality_lab.setText(u'渲染质量设置为: 高')
                self.pe_high = QtGui.QPalette()
                self.pe_high.setColor(QtGui.QPalette.WindowText, QtCore.Qt.red)
                self.rad_high_quality.setPalette(self.pe_high)
                # 设置camera,diffuse,specular,tranmission,sss,volume参数
                cmds.setAttr("defaultArnoldRenderOptions.AASamples", 4)
                cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples", 4)
                cmds.setAttr("defaultArnoldRenderOptions.GISpecularSamples", 4)
                cmds.setAttr("defaultArnoldRenderOptions.GITransmissionSamples", 4)
                cmds.setAttr("defaultArnoldRenderOptions.GISssSamples", 3)
                cmds.setAttr("defaultArnoldRenderOptions.GIVolumeSamples", 3)
                self.pe_black = QtGui.QPalette()
                self.pe_black.setColor(QtGui.QPalette.WindowText, QtCore.Qt.lightGray)
                self.rad_medium_quality.setPalette(self.pe_black)
                self.rad_low_quality.setPalette(self.pe_black)
            elif self.qua == u'中':
                self.quality_lab.setText(u'渲染质量设置为: 中')
                self.pe_medium = QtGui.QPalette()
                self.pe_medium.setColor(QtGui.QPalette.WindowText, QtCore.Qt.red)
                self.rad_medium_quality.setPalette(self.pe_medium)
                cmds.setAttr("defaultArnoldRenderOptions.AASamples", 3)
                cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples", 2)
                cmds.setAttr("defaultArnoldRenderOptions.GISpecularSamples", 2)
                cmds.setAttr("defaultArnoldRenderOptions.GITransmissionSamples", 1)
                cmds.setAttr("defaultArnoldRenderOptions.GISssSamples", 1)
                cmds.setAttr("defaultArnoldRenderOptions.GIVolumeSamples", 2)
                self.pe_black = QtGui.QPalette()
                self.pe_black.setColor(QtGui.QPalette.WindowText, QtCore.Qt.lightGray)
                self.rad_high_quality.setPalette(self.pe_black)
                self.rad_low_quality.setPalette(self.pe_black)
            elif self.qua == u'低':
                self.quality_lab.setText(u'渲染质量设置为: 低')
                self.pe_low = QtGui.QPalette()
                self.pe_low.setColor(QtGui.QPalette.WindowText, QtCore.Qt.red)
                self.rad_low_quality.setPalette(self.pe_low)
                cmds.setAttr("defaultArnoldRenderOptions.AASamples", 2)
                cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples", 2)
                cmds.setAttr("defaultArnoldRenderOptions.GISpecularSamples", 2)
                cmds.setAttr("defaultArnoldRenderOptions.GITransmissionSamples", 1)
                cmds.setAttr("defaultArnoldRenderOptions.GISssSamples", 1)
                cmds.setAttr("defaultArnoldRenderOptions.GIVolumeSamples", 1)
                self.pe_black = QtGui.QPalette()
                self.pe_black.setColor(QtGui.QPalette.WindowText, QtCore.Qt.lightGray)
                self.rad_medium_quality.setPalette(self.pe_black)
                self.rad_high_quality.setPalette(self.pe_black)
            elif not self.qua:
                QtWidgets.QMessageBox.information(self, u'warning', u"请先选择渲染质量", QtWidgets.QMessageBox.Ok)
        except:
            pass

    def lgt_add_list(self):
        """
            获取combox的值
        :return:
        """
        self.lgt_type_name = self.lgt_type.currentText()

    def lgt_creat(self):
        """
            向listwidget添加item，同时创建灯光
        :return:
        """
        try:
            posit = cmds.xform(cmds.ls(sl=1), q=1, t=1, ws=1)
        except:
            posit = None
        try:
            lgt_name = self.lgt_type_name + '_' + str(randint(0, 100))
            self.lgt_list.addItem(lgt_name)
            if re.match(r'directionalLight', lgt_name):
                try:
                    cmds.directionalLight(name=lgt_name, position=posit)
                except:
                    cmds.directionalLight(name=lgt_name)
            elif re.match(r'pointLight', lgt_name):
                try:
                    cmds.pointLight(name=lgt_name, position=posit)
                except:
                    cmds.pointLight(name=lgt_name)
            elif re.match(r'ambientLight', lgt_name):
                try:
                    cmds.ambientLight(name=lgt_name, position=posit)
                except:
                    cmds.ambientLight(name=lgt_name)
            elif re.match(r'spotLight', lgt_name):
                try:
                    cmds.spotLight(name=lgt_name, position=posit)
                except:
                    cmds.spotLight(name=lgt_name)
            elif re.match(r'aiAreaLight', lgt_name):
                try:
                    mutils.createLocatorWithName('aiAreaLight', nodeName=lgt_name, asLight=True)
                    cmds.move(posit[0], posit[1], posit[2], lgt_name, ws=1)
                except:
                    mutils.createLocatorWithName('aiAreaLight', nodeName=lgt_name, asLight=True)
            elif re.match(r'aiSkyDomeLight', lgt_name):
                mutils.createLocatorWithName('aiSkyDomeLight', nodeName=lgt_name, asLight=True)
            elif re.match(r'aiMeshLight', lgt_name):
                mutils.createMeshLight()
        except:
            lgt_name_default = self.lgt_type.itemText(0) + '_' + str(randint(0, 100))
            self.lgt_list.addItem(lgt_name_default)
            try:
                cmds.directionalLight(name=lgt_name_default, position=posit)
            except:
                cmds.directionalLight(name=lgt_name_default)

    def lgt_list_menu(self, point):
        """
            在鼠标坐标处(同时在item上)弹出菜单
        :param point:
        :return:
        """
        if self.lgt_list.count():
            if self.lgt_list.itemAt(QtWidgets.QWidget.mapFromGlobal(self.lgt_list, QtGui.QCursor.pos())):
                self.popMenu.exec_(QtGui.QCursor.pos())

    def lgt_list_clear(self):
        """
            清除item同时删除灯光
        Returns:

        """
        for i in range(self.lgt_list.count()):
            cmds.delete(self.lgt_list.item(i).text())
        self.lgt_list.clear()

    def lgt_modify_attribute(self):
        """
            获取选择的item的文本信息，然后执行功能
        :return:
        """

        lgt = lgt_func.LgtUI()
        lgt.show()

    def lgt_rename_item(self):
        # 让所选的item重命名
        for item in self.lgt_list.selectedItems():
            self.rename_widget = QtWidgets.QDialog()
            self.rename_widget.setStyleSheet('Font-size:20PX')
            self.rename_widget.setFixedSize(300, 100)
            self.rename_widget.setWindowTitle(u'重命名')
            self.rename_lay_h = QtWidgets.QHBoxLayout(self.rename_widget)
            self.rename_line_edit = QtWidgets.QLineEdit()
            self.rename_btn = QtWidgets.QPushButton(u'确定')
            my_regex = QtCore.QRegExp("[a-zA-Z_]*[0-9a-zA-Z_]*")
            my_validator = QtGui.QRegExpValidator(my_regex, self.rename_line_edit)
            self.rename_line_edit.setValidator(my_validator)
            self.rename_line_edit.setPlaceholderText(item.text())
            self.rename_lay_h.addWidget(self.rename_line_edit)
            self.rename_lay_h.addWidget(self.rename_btn)
            self.rename_widget.show()
            self.rename_line_edit.textChanged.connect(self.lgt_re)
            self.rename_btn.clicked.connect(self.exit_dialog)

    def lgt_re(self):
        """
            重命名
        Returns:

        """
        new_name = self.rename_line_edit.text()
        for i in self.lgt_list.selectedItems():
            try:
                cmds.rename(i.text(), new_name)
                i.setText(new_name)
            except:
                pass

    def exit_dialog(self):
        self.rename_widget.close()

    def lgt_del_item(self):
        """
            删除灯光及item
        :return:
        """
        item_row = self.lgt_list.selectedItems()
        for i in item_row:
            self.lgt_list.takeItem(self.lgt_list.row(i))
            cmds.delete(i.text())

    def lgt_select(self):
        """
            选择item对应的灯光
        :return:

        """
        cmds.select(clear=1)
        item_row = self.lgt_list.selectedItems()
        for i in item_row:
            try:
                cmds.select(i.text(), add=1)
            except:
                pass

    def lgt_refresh(self):
        """
            刷新灯光，若场景内的灯光多于界面内的灯光则将多的灯光添加进界面，反之从界面删除场景内不存在的灯光的item
        Returns:

        """
        lgt_select = []
        item_total = []
        try:
            for num in range(self.lgt_list.count()):
                item = self.lgt_list.item(num)
                item_total.append(item.text())
        except:
            pass
        maya_light = cmds.ls(type='light')
        arnold_light = cmds.ls(type='aiSkyDomeLight')
        arnold_light_one = cmds.ls(type='aiMeshLight')
        arnold_light_two = cmds.ls(type='aiAreaLight')
        if maya_light:
            lgt_select.extend(maya_light)
        if arnold_light:
            lgt_select.append(arnold_light[0])
        if arnold_light_one:
            lgt_select.append(arnold_light_one[0])
        if arnold_light_two:
            lgt_select.append(arnold_light_two[0])
        if lgt_select:
            for lgt in lgt_select:
                for typ in LGT_TYPE:
                    if fuzz.partial_ratio(cmds.objectType(lgt), typ) >= 95:
                        if item_total:
                            if cmds.listRelatives(lgt, p=1)[0] in item_total:
                                pass
                            else:
                                self.lgt_list.addItem(cmds.listRelatives(lgt, p=1)[0])
                        else:
                            self.lgt_list.addItem(cmds.listRelatives(lgt, p=1)[0])
        for ty in item_total:
            if cmds.objExists(ty):
                pass
            else:
                for i in range(self.lgt_list.count()):
                    try:
                        if self.lgt_list.item(i).text() == ty:
                            self.lgt_list.takeItem(self.lgt_list.row(self.lgt_list.item(i)))
                    except:
                        pass

    def layer_add_list(self):
        """
            获取combox的值
        :return:
        """
        self.layer_type_name = self.layer_type.currentText()

    def layer_creat(self):
        """
            向listwidget添加item
        :return:
        """
        try:
            self.layer_list.addItem(self.layer_type_name)
            for i in LAYER_TYPE:
                if self.layer_type_name == i[0]:
                    aovs.AOVInterface().addAOV('%s' % i[0], aovType='%s' % i[1])
        except:
            self.layer_list.addItem(self.layer_type.itemText(0))
            aovs.AOVInterface().addAOV('%s' % self.layer_type.itemText(0), aovType='rgb')

    def layer_list_menu(self, point):
        """
            在鼠标坐标处(同时在item上)弹出菜单
        :param point:
        :return:
        """
        if self.layer_list.count():
            if self.layer_list.itemAt(QtWidgets.QWidget.mapFromGlobal(self.layer_list, QtGui.QCursor.pos())):
                self.popMenu_layer.exec_(QtGui.QCursor.pos())

    def layer_list_clear(self):
        for i in range(self.layer_list.count()):
            aovs.AOVInterface().removeAOVs(self.layer_list.item(i).text())
        self.layer_list.clear()

    def layer_modify_attribute(self):
        """
            获取选择的item的文本信息，然后执行功能，禁用层
        :return:
        """
        item_name = self.layer_list.selectedItems()
        for item in item_name:
            cmds.setAttr("aiAOV_%s.enabled" % item.text(), 0)
            item.setForeground(QtGui.QColor('red'))

    def layer_enable_attribute(self):
        """
            启用层
        :return:
        """
        item_name = self.layer_list.selectedItems()
        for item in item_name:
            cmds.setAttr("aiAOV_%s.enabled" % item.text(), 1)
            item.setForeground(QtGui.QColor('lightGray'))

    def layer_del_item(self):
        """
            删除选中的item
        :return:
        """
        item_row = self.layer_list.selectedItems()
        for i in item_row:
            self.layer_list.takeItem(self.layer_list.row(i))
            aovs.AOVInterface().removeAOVs(i.text())

    def layer_select(self):
        """
            选择层
        :return:
        """
        item_row = self.layer_list.selectedItems()
        for item in item_row:
            for aov in aovs.getAOVNodes(True):
                if item.text() == aov[0]:
                    cmds.select(aov[-1])

    def layer_refresh(self):
        """
            刷新层，若场景内的层多于界面内的层则将多的层添加进界面，反之从界面删除场景内不存在的层的item
        Returns:

        """
        item_total = []
        try:
            for num in range(self.layer_list.count()):
                item = self.layer_list.item(num)
                item_total.append(item.text())
        except:
            pass
        aov_total = []
        for aov in aovs.getAOVNodes(True):
            aov_total.append(aov[0])
        for i in aov_total:
            for j in LAYER_TYPE:
                if i == j[0]:
                    if item_total:
                        if i in item_total:
                            pass
                        else:
                            self.layer_list.addItem(i)
                    else:
                        self.layer_list.addItem(i)
        for ty in item_total:
            if re.findall(r'%s' % ty, str(aov_total)):
                pass
            else:
                for i in range(self.layer_list.count()):
                    try:
                        if self.layer_list.item(i).text() == ty:
                            self.layer_list.takeItem(self.layer_list.row(self.layer_list.item(i)))
                    except:
                        pass

    def render_folder(self):
        """
            打开文件选择对话框
        :return:
        """
        f = QtWidgets.QFileDialog.getExistingDirectory(self, u'文件浏览器', 'C:/')
        self.render_line.setText(f)
        self.render_file_path = self.render_line.text()
        pm.mel.setProject(r"%s" % self.render_file_path)
        if self.render_line.text():
            self.render_btn.setEnabled(True)
        else:
            self.render_btn.setEnabled(False)

    def render_camera(self):
        """
            获取并设置渲染摄像机
        :return:
        """
        self.camera = self.cam_type.currentText()
        # 设置四个默认相机为不是渲染相机，选择的相机设置为渲染相机
        self.cam_index = self.cam_type.currentIndex()
        for index in range(self.cam_type.count()):
            if self.cam_type.itemText(index) == self.camera:
                cmds.setAttr('%s.renderable' % self.cam_type.itemText(index), 1)
            else:
                cmds.setAttr('%s.renderable' % self.cam_type.itemText(index), 0)

    def render_pixel(self):
        """
            获取并设置照片尺寸
        :return:
        """
        self.pixel = self.pixel_type.currentText()
        self.w = int(self.pixel.split('*')[0])
        self.h = int(self.pixel.split('*')[-1])
        # 设置渲染图片的尺寸大小
        cmds.setAttr('defaultResolution.width', self.w)
        cmds.setAttr('defaultResolution.height', self.h)
        if re.search(r'2048', str(self.w)) or re.search(r'4096', str(self.w)):
            cmds.setAttr('defaultResolution.deviceAspectRatio', 1)
        else:
            cmds.setAttr('defaultResolution.deviceAspectRatio', 1.777)

    def render_format(self):
        """
            获取并设置图片格式
        :return:
        """
        self.tex_format = self.render_tex_type.currentText()
        # 设置渲染输出图片格式
        cmds.setAttr("defaultArnoldDriver.ai_translator", self.tex_format, type="string")
        if re.search(r'png', self.tex_format):
            # 设置师徒的比例
            cmds.setAttr("defaultArnoldDriver.pngFormat", 1)

    def render_frame_st(self):
        """
            获得开始帧
        Returns:

        """
        self.frame_start = int(self.render_batch_line_st.text())

    def render_frame_end(self):
        """
            获得结束帧
        Returns:

        """
        self.frame_end = int(self.render_batch_line_end.text()) + 1

    def render_file_name(self):
        self.file_name = self.render_prefix.text()

    def render(self):
        """
            渲染主功能函数
        :return:
        """
        try:
            # 设置序列渲染和静帧渲染
            if self.render_batch_w.isHidden():
                try:
                    cmds.setAttr('defaultRenderGlobals.imageFilePrefix', '%s' % self.file_name, type='string')
                    cmds.arnoldRender(camera=self.camera, w=self.w, h=self.h)
                except:
                    cmds.arnoldRender(camera=self.camera, w=self.w, h=self.h)
            else:
                for num in range(self.frame_start, self.frame_end):
                    try:
                        cmds.setAttr('defaultRenderGlobals.imageFilePrefix', '%s%s' % (self.file_name, num),
                                     type='string')
                        cmds.arnoldRender(b=True, seq='%s' % num, camera=self.camera, w=self.w, h=self.h)
                    except:
                        cmds.setAttr('defaultRenderGlobals.imageFilePrefix', '%s' % num, type='string')
                        cmds.arnoldRender(b=True, seq='%s' % num, camera=self.camera, w=self.w, h=self.h)
        except:
            try:
                try:
                    self.pixel_one = self.pixel_type.itemText(0)
                    self.w_one = int(self.pixel_one.split('*')[0])
                    self.h_one = int(self.pixel_one.split('*')[-1])
                    cmds.setAttr('defaultResolution.width', self.w_one)
                    cmds.setAttr('defaultResolution.height', self.h_one)
                    if re.search(r'2048', str(self.w_one)) or re.search(r'4096', str(self.w_one)):
                        cmds.setAttr('defaultResolution.deviceAspectRatio', 1)
                    else:
                        cmds.setAttr('defaultResolution.deviceAspectRatio', 1.777)
                    if self.render_batch_w.isHidden():
                        try:
                            cmds.setAttr('defaultRenderGlobals.imageFilePrefix', '%s' % self.file_name,
                                         type='string')
                            cmds.arnoldRender(camera=self.camera, w=self.w_one, h=self.h_one)
                        except:
                            cmds.arnoldRender(camera=self.camera, w=self.w_one, h=self.h_one)
                    else:
                        for num in range(self.frame_start, self.frame_end):
                            try:
                                cmds.setAttr('defaultRenderGlobals.imageFilePrefix', '%s%s' % (self.file_name, num),
                                             type='string')
                                cmds.arnoldRender(b=True, seq='%s' % num, camera=self.camera, w=self.w_one,
                                                  h=self.h_one)
                            except:
                                cmds.setAttr('defaultRenderGlobals.imageFilePrefix', '%s' % num,
                                             type='string')
                                cmds.arnoldRender(b=True, seq='%s' % num, camera=self.camera, w=self.w_one,
                                                  h=self.h_one)
                                # cmds.arnoldRender(camera=self.camera,w=self.w_one,h=self.h_one)
                except:
                    self.camera_one = self.cam_type.itemText(0)
                    # 设置四个默认相机为不是渲染相机，选择的相机设置为渲染相机
                    for index in range(self.cam_type.count()):
                        if self.cam_type.itemText(0) == self.camera_one:
                            cmds.setAttr('%s.renderable' % self.cam_type.itemText(0), 1)
                        else:
                            cmds.setAttr('%s.renderable' % self.cam_type.itemText(index), 0)
                    cmds.setAttr('defaultResolution.width', self.w)
                    cmds.setAttr('defaultResolution.height', self.h)
                    if self.render_batch_w.isHidden():
                        try:
                            cmds.setAttr('defaultRenderGlobals.imageFilePrefix', '%s' % self.file_name, type='string')
                            cmds.arnoldRender(camera=self.camera_one, w=self.w, h=self.h)
                        except:
                            cmds.arnoldRender(camera=self.camera_one, w=self.w, h=self.h)
                    else:
                        for num in range(self.frame_start, self.frame_end):
                            try:
                                cmds.setAttr('defaultRenderGlobals.imageFilePrefix', '%s%s' % (self.file_name, num),
                                             type='string')
                                cmds.arnoldRender(b=True, seq='%s' % num, camera=self.camera_one, w=self.w, h=self.h)
                            except:
                                cmds.setAttr('defaultRenderGlobals.imageFilePrefix', '%s' % num, type='string')
                                cmds.arnoldRender(b=True, seq='%s' % num, camera=self.camera_one, w=self.w, h=self.h)
                                # cmds.arnoldRender(camera=self.camera_one,w=self.w,h=self.h)
            except:
                self.camera_two = self.cam_type.itemText(0)
                # 设置四个默认相机为不是渲染相机，选择的相机设置为渲染相机
                for index in range(self.cam_type.count()):
                    if self.cam_type.itemText(0) == self.camera_two:
                        cmds.setAttr('%s.renderable' % self.cam_type.itemText(0), 1)
                    else:
                        cmds.setAttr('%s.renderable' % self.cam_type.itemText(index), 0)
                self.pixel_two = self.pixel_type.itemText(0)
                self.w_two = int(self.pixel_two.split('*')[0])
                self.h_two = int(self.pixel_two.split('*')[-1])
                cmds.setAttr('defaultResolution.width', self.w_two)
                cmds.setAttr('defaultResolution.height', self.h_two)
                if re.search(r'2048', str(self.w_two)) or re.search(r'4096', str(self.w_two)):
                    cmds.setAttr('defaultResolution.deviceAspectRatio', 1)
                else:
                    cmds.setAttr('defaultResolution.deviceAspectRatio', 1.777)
                if self.render_batch_w.isHidden():
                    try:
                        cmds.setAttr('defaultRenderGlobals.imageFilePrefix', '%s' % self.file_name, type='string')
                        cmds.arnoldRender(camera=self.camera_two, w=self.w_two, h=self.h_two)
                    except:
                        cmds.arnoldRender(camera=self.camera_two, w=self.w_two, h=self.h_two)
                else:
                    for num in range(self.frame_start, self.frame_end):
                        try:
                            cmds.setAttr('defaultRenderGlobals.imageFilePrefix', '%s%s' % (self.file_name, num),
                                         type='string')
                            cmds.arnoldRender(b=True, seq='%s' % num, camera=self.camera_two, w=self.w_two,
                                              h=self.h_two)
                        except:
                            cmds.setAttr('defaultRenderGlobals.imageFilePrefix', '%s' % num, type='string')
                            cmds.arnoldRender(b=True, seq='%s' % num, camera=self.camera_two, w=self.w_two,
                                              h=self.h_two)
                            # cmds.arnoldRender(camera=self.camera_two, w=self.w_two, h=self.h_two)


if __name__ == '__main__':
    a = MainFunc()
    a.show()
