#-*- coding:utf-8 -*-
import maya.cmds as cmd
def ren():
    select = cmd.ls(dag=True, long=True, v=True, typ='transform', lights=False)
    select.sort(key=len, reverse=True)
    total_grp = []
    total_geo = []
    # print select
    for i in select:
        # print select
        short = i.split('|')[-1]
        childrens = cmd.listRelatives(i, children=True, f=True) or []
        # print childrens
        if len(childrens) == 1:
            objectType = cmd.objectType(childrens)
            # print objectType
        else:
            objectType = cmd.objectType(i)
            # print i,objectType
        if objectType == 'transform':
            total_grp.append(short)
        if objectType == 'mesh':
            total_geo.append(short)
        # print total_geo
        # print total_grp
    list_geo = []
    list_grp = []
    k = []
    l = []
    for j in total_geo:
        # print j
        if j not in list_geo:
            list_geo.append(j)
        else:
            k.append(j)
    for h in total_grp:
        if h not in list_grp:
            list_grp.append(h)
        else:
            l.append(h)
    del select[0:]
    return k,l