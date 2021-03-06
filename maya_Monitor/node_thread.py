# coding=utf8
import os
import maya.standalone as standalone
import sys


def node_check(path):
    standalone.initialize()
    import maya.cmds as cmds
    cmds.file(path, o=True, f=True, executeScriptNodes=False)  # 打开一个测试文件
    script_node = cmds.ls(typ='script')
    expressions = cmds.ls(typ='expression')
    maya_env_list = []
    maya_env_list.append('import')
    maya_env_list.append('eval')
    maya_env_list.append('python')
    maya_env_list.append('os.sys')
    maya_env_list.append('os.system')
    maya_env_list.append('setx')
    for key in os.environ.keys():
        if 'MAYA' in key:
            maya_env_list.append(key)  # 获取maya相关的环境变量
    waring_list = []
    for script in script_node:  # 若环境变量存在于script node中，则打印出script node的名字
        for word in maya_env_list:
            if not cmds.getAttr(script + '.before'):
                pass
            else:
                if word in cmds.getAttr(script + '.before'):
                    waring_list.append('ScriptNode: {0} find the key_word:{1}'.format(script, word))
    for expression in expressions:
        for maya_env in maya_env_list:
            if maya_env in cmds.getAttr(expression + '.expression'):
                waring_list.append('There are environment variables in expression{0}:{1}'.format(expression, maya_env))
    if waring_list:
        print waring_list
    else:
        print 'No problem'
    standalone.uninitialize()

# path = "C:/Users/ruansenlin/Desktop/ffff.ma"
path = sys.argv[-1]
node_check(path)
