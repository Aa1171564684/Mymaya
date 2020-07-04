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
    select_mesh = None
    select_mesh = cmds.ls(sl=1)
    return select_mesh


def reset_object_position(select_mesh):
    """
    reset the absolute acorrdinate
    Returns:

    """
    check_uv_count(select_mesh)
    if select_mesh:
        for obj in select_mesh:
            cmds.makeIdentity(obj, apply=True, t=True, r=True, s=True, n=0)
            cmds.select(obj, r=1)
            cmds.move(a=1, x=0, y=0, z=0)
    cmds.select(cl=1)
    return True


def check_uv_count(select_mesh):
    """
    Check if the shape contain uv sets less than 2
    Args:
        mesh:

    Returns:
        bool: True for less than 2, False otherwise
    """
    uv_set_num = cmds.polyUVSet(select_mesh, query=True, allUVSets=True)
    cmds.select(cl=1)
    if uv_set_num:
        if len(uv_set_num) >= 2:
            return RuntimeError(u'模型超过了2个UV')
    else:
        pass
    return True


def set_export_argument(select_mesh, fbx_path):
    """

    Args:
        select_mesh:
        fbx_path:

    Returns:

    """
    cmds.select(select_mesh)
    # 设置导出信息
    mel.eval('FBXExportSmoothingGroups -v true')
    mel.eval('FBXExportSmoothMesh -v true')
    # 执行导出
    cmds.file(fbx_path, force=1, options='v=0', typ="FBX export", pr=1, es=1)
    # json_path=os.path.dirname(fbx_path)+'/'+'fbx_path_json'
    # with open(json_path,'w')as f:
    #     json.dump(os.path.dirname(fbx_path),f)
    cmds.select(cl=1)


def check_uv_overlap(select_mesh):
    '''

    Args:
        select_mesh:

    Returns:
        overlap_uv:Coincident UV
    '''
    uv_name_list = []
    for mesh_face in select_mesh:
        uv_num = cmds.polyEvaluate(mesh_face, f=1)
        for num in range(uv_num):
            # 获取面名称
            uv_name = '{}.f[{}]'.format(mesh_face, num)
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


# 查询模型是否有多于四边的面
def query_face_dege(select_mesh):
    '''

    Args:
        select_mesh:

    Returns:
        face_edge_dict:
    '''
    face_edge_dict = {}
    for mesh_face in select_mesh:
        # 获取面数量
        mesh_face_num = cmds.polyEvaluate(mesh_face, f=1)
        for num in range(mesh_face_num):
            mesh_face_name = '{}.f[{}]'.format(mesh_face, num)
            # 获取边数量
            mesh_edge = cmds.polyInfo(mesh_face_name, fe=1)
            mesh_edge_index = mesh_edge[0].split(':')[-1].split(' ')[:-1]
            # 过滤空格字符串
            mesh_edge_num = len(filter(set_filter(mesh_edge_index), mesh_edge_index))
            face_edge_dict[mesh_face_name] = int(mesh_edge_num)
    cmds.select(cl=1)
    return face_edge_dict


# 查询模型面数
def check_face_num(select_mesh):
    '''

    Args:
        select_mesh:

    Returns:
        status:Three diffrerent status
    '''
    # 查询模型的全路径
    file_path = cmds.file(select_mesh, q=1, sn=1)
    face_num = cmds.polyEvaluate(select_mesh, f=1)
    cmds.select(cl=1)
    if re.search(r'Assets/Char', file_path) and isinstance(face_num, int):
        if face_num >= 500000:
            return 'char'
    elif re.search(r'Assets/Envir', file_path) and isinstance(face_num, int):
        if face_num >= 10000:
            return 'envir'
    else:
        return 'error'


def chech_point_overlap(select_mesh):
    '''

    Args:
        select_mesh:

    Returns:
        point_position_list:position of the point
    '''
    point_position_list = []
    for mesh_face in select_mesh:
        point_num = cmds.polyEvaluate(mesh_face, v=1)
        for num in range(point_num):
            point_name = '{}.vtx[{}]'.format(mesh_face, num)
            # 查询点的坐标
            point_position = cmds.xform(point_name, q=1, t=1, ws=1)
            point_position_list.append(point_position)
    cmds.select(cl=1)
    return point_position_list
