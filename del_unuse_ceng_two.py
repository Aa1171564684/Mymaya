#-*- coding:utf-8 -*-
import maya.mel as mel
def unuse():
    #删除不使用的节点
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    #删除不出不使用的动画层
    mel.eval('deleteEmptyAnimLayers()')
    #删除不使用的display层
    mel.eval('layerEditorSelectUnused;layerEditorDeleteLayer""')