#-*- coding:utf-8 -*-
import maya.mel as mel
import maya.cmds as cmd
import re
def optimize():
    #删除不使用的节点
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    #先获取不使用的层，然后删除
    ceng=cmd.ls(type='displayLayer')
    for i in ceng:
        if re.search('default',i):
            pass
        else:
            cmd.delete(i)
    #场景优化
    mel.eval("OptimizeScene")
