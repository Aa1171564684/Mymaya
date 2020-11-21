#-*- coding:utf-8 -*-
import maya.cmds as cmd
def is_group(groupName):
    try:
        children = cmd.listRelatives(groupName, children=True)
        for child in children:
            if not cmd.ls(child, transforms = True):
                return False
        return True
    except:
        return False
def one():
    select=cmd.ls()
    onegrp_total=[]
    for item in select:
        if is_group(item):
            cmd.xform(item,rp=[0,0,0],ws=True)
            fath=cmd.listRelatives(item,parent=True)
            if fath==None:
                continue
            if len(fath)>0:
                #print fath
                onegrp_total.append(item)
        else:
            pass
    return onegrp_total
    # if len(onegrp_total)>0:
    #     print '有物体不符合一个组的原则',onegrp_total
