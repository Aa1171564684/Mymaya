# coding=utf8

import time
import os
import fnmatch
import hashlib
import re
import json


# 遍历路径下的ma，mb文件
def search_files(env_path):
    fnexps = "*.ma|*.mb"
    for root, dirs, files in os.walk(env_path):
        for fnexp in fnexps.split('|'):
            for filename in fnmatch.filter(files, fnexp):
                yield os.path.join(root, filename)


# 获取文件修改时间
def DFS_file_search(dict_name):
    """

    Args:
        dict_name:

    Returns:
        result_txt
    """
    stack = []
    result_txt = []
    stack.append(dict_name)
    while len(stack) != 0:  # 栈空代表所有目录均已完成访问
        temp_name = stack.pop()
        try:
            temp_name2 = os.listdir(temp_name)  # list ["","",...]
            for eve in temp_name2:
                stack.append(temp_name + "\\" + eve)  # 维持绝对路径的表达
        except:
            result_txt.append(temp_name)
    return result_txt


# 获取唯一的MD5值
def judge_time_fod(pttq_path):
    """

    Args:
        pttq_path:

    Returns:
            获取此文件的md5
    """
    pttq_path_list = []
    time_list = []  # pttq_path1下所有文件修改日期的列表
    for i in DFS_file_search(pttq_path):
        # print i
        file_time = time.ctime(os.stat(i).st_mtime)  # 文件的修改时间
        if file_time in time_list:
            pass
        else:
            time_list.append(file_time)
    for root_dir, sub_dir, sub_files in os.walk(pttq_path):
        if sub_dir:
            pttq_path_list.append(sub_dir)
        if sub_files:
            pttq_path_list.append(sub_files)
    m1 = hashlib.md5()
    m1.update(str(pttq_path_list) + str(time_list))
    md5 = m1.hexdigest()  # md5值
    return md5


def creat_json(path, json_list):
    if re.search('.ma', path) or re.search('.mb', path):
        dirname = os.path.dirname(path.replace('\\', '/'))
        if os.path.isdir(dirname + '/error'):
            pass
        else:
            os.makedirs(dirname + '/error')
        json_path = '{}/error/log.json'.format(dirname)
        with open(json_path, 'w') as f:
            json.dump(json_list, f, indent=4)
    else:
        if os.path.isdir(path.replace('\\', '/') + '/error'):
            pass
        else:
            os.makedirs(path.replace('\\', '/') + '/error')
        json_path = '{}/error/log.json'.format(path.replace('\\', '/'))
        with open(json_path, 'w') as f:
            json.dump(json_list, f, indent=4)

# def get_maya_location(self):
#     '''
#     获取maya安装目录
#     :return: C:\Program Files\Autodesk\Maya2017
#     '''
#     list_install = []
#     for i in (os.environ):
#         if i == 'MAYA_LOCATION':
#             list_install.append(i)
#     if not list_install:
#         # print u'系统未识别到MAYA_LOCATION'
#         return False
#     else:
#         # print os.environ.get(list[0]) #maya安装目录
#         return os.environ.get(list_install[0])
