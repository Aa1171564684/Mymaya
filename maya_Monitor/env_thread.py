# coding=utf8
import os
import sys
import re
import maya.standalone as standalone
import maya.cmds as cmds

sys_path_list = []
before_environ_list = []
standalone.initialize()


def begin():
    if not sys_path_list:
        for i in sys.path:
            sys_path_list.append(i)
    if not before_environ_list:
        for i in os.environ.keys():
            key_and_value_one = i + ':' + os.environ[i]
            before_environ_list.append(key_and_value_one)


def check_sys(path):
    '''
    获取env,sys.path的数量
    :return:
    '''

    cmds.file(path, o=1, f=1)
    if sys_path_list == sys.path:
        print 'sys is normal'
    else:
        for i in sys.path:
            if i not in sys_path_list:
                print 'new sys.path:{}'.format(i)
    right_env = []
    for i in os.environ.keys():
        if re.search(r'MTOA_PATH',i) or re.search(r'MTOA_EXTENSIONS_PATH',i) or re.search(r'ARNOLD_PLUGIN_PATH',i):
            pass
        else:
            key_and_value = i + ':' + os.environ[i]
            # print key_and_value
            if key_and_value in before_environ_list:
                pass
            else:
                right_env.append(key_and_value)
                print 'Environmental variable change:{}'.format(i)
    if not right_env:
        print 'env is normal'


begin()
path = sys.argv[-1]
check_sys(path)
standalone.uninitialize()
