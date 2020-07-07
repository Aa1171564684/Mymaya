# coding=utf8
# Copyright (c) 2020 GVF

import re
import json
import os
import maya.cmds as cmds
import maya.mel as mel


# 1.世界目标清零
# 2.冻结变换
# 3.清历史
def select_mesh():
    select_mesh=None
    select_mesh = cmds.ls(sl=1)
    cmds.select(cl=1)
    return select_mesh


def reset_object_position(log_mesh):
    """
    reset the absolute acorrdinate
    Returns:

    """
    check_uv_count(log_mesh)
    if log_mesh:
        # for obj in select_mesh:
        cmds.select(log_mesh, r=1)
        cmds.move(a=1, x=0, y=0, z=0)
        cmds.makeIdentity(log_mesh, apply=True, t=True, r=True, s=True, n=0)
        cmds.select(cl=1)
        return True


def check_uv_count(log_mesh):
    """
    Check if the shape contain uv sets less than 2
    Args:
        mesh:

    Returns:
        bool: True for less than 2, False otherwise
    """
    uv_set_num = cmds.polyUVSet(log_mesh, query=True, allUVSets=True)
    cmds.select(cl=1)
    if uv_set_num:
        if len(uv_set_num) >= 2:
            return RuntimeError(u'存在模型超过了2个UV')
    else:
        pass
    return True


def set_export_argument(log_mesh, fbx_path):
    """

    Args:
        select_mesh:
        fbx_path:

    Returns:

    """

    cmds.loadPlugin("fbxmaya.mll")
    cmds.select(log_mesh)
    # 设置导出信息
    mel.eval('FBXExportSmoothingGroups -v true')
    mel.eval('FBXExportSmoothMesh -v true')
    # 执行导出
    cmds.file(fbx_path + '/' + log_mesh, force=1, typ="FBX export", pr=1, es=1)
    cmds.select(cl=1)


def check_uv_overlap(log_mesh):
    '''

    Args:
        select_mesh:

    Returns:
        overlap_uv:Coincident UV
    '''
    overlap_uv=None
    uv_name_list = []
    uv_num = cmds.polyEvaluate(log_mesh, f=1)
    for num in range(uv_num):
        # 获取面名称
        uv_name = '{}.f[{}]'.format(log_mesh, num)
        uv_name_list.append(uv_name)
    cmds.select(uv_name_list, add=1)
    # 判断UV是否重合
    overlap_uv = cmds.polyUVOverlap(oc=1)
    cmds.select(cl=1)
    return overlap_uv


def set_filter(edge_num):
    '''

    Args:
        edge_num:

    Returns:
        None
    '''
    for element in edge_num:
        if element == ' ':
            pass


def query_face_dege(log_mesh):
    '''

    Args:
        select_mesh:

    Returns:
        face_edge_dict:
    '''
    # 获取面数量
    face_edge_dict = {}
    mesh_face_num = cmds.polyEvaluate(log_mesh, f=1)
    for num in range(mesh_face_num):
        mesh_face_name = '{}.f[{}]'.format(log_mesh, num)
        # 获取边数量
        mesh_edge = cmds.polyInfo(mesh_face_name, fe=1)
        mesh_edge_index = mesh_edge[0].split(':')[-1].split(' ')[:-1]
        # 过滤空格字符串
        mesh_edge_num = len(filter(set_filter(mesh_edge_index), mesh_edge_index))
        face_edge_dict[mesh_face_name] = int(mesh_edge_num)
    cmds.select(cl=1)
    return face_edge_dict


# 查询模型面数
def check_face_num(log_mesh):
    '''

    Args:
        select_mesh:

    Returns:
        status:Three diffrerent status
    '''
    # 查询模型的全路径
    file_path=None
    face_num=None
    file_path = cmds.file(log_mesh, q=1, sn=1)
    face_num = cmds.polyEvaluate(log_mesh, f=1)
    cmds.select(cl=1)
    return file_path, face_num


def chech_point_overlap(log_mesh):
    '''

    Args:
        select_mesh:

    Returns:
        point_position_list:position of the point
    '''
    point_position_list = []
    # for mesh_face in select_mesh:
    point_num = cmds.polyEvaluate(log_mesh, v=1)
    for num in range(point_num):
        point_name = '{}.vtx[{}]'.format(log_mesh, num)
        # 查询点的坐标
        point_position = cmds.xform(point_name, q=1, t=1, ws=1)
        point_position_list.append(point_position)
    cmds.select(cl=1)
    return point_position_list


def get_export_path():
    return cmds.fileDialog2(fm=3)[0]
