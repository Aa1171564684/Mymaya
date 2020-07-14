# coding=utf8
# Copyright (c) 2019 GVF
import os
import maya.standalone as standalone
import sys

def node_check(path):
    standalone.initialize()
    import maya.cmds as cmds
    cmds.file(path, o=True, f=True,executeScriptNodes=False)  # 打开一个测试文件
    script_node = cmds.ls(typ='script')
    maya_env_list = []
    for key in os.environ.keys():
        if 'MAYA' in key:
            maya_env_list.append(key)  # 获取maya相关的环境变量
    waring_list=[]
    for script in script_node:  # 若环境变量存在于script node中，则打印出script node的名字
        for word in maya_env_list:
            if word in cmds.getAttr(script + '.before'):
                waring_list.append(u'ScriptNode: {0} find the environment:{1}\n'.format(script,word))
    if waring_list:
        print waring_list
    else:
        print 'No problem'
    standalone.uninitialize()
path=sys.argv[-1]
node_check(sys.argv[-1])



