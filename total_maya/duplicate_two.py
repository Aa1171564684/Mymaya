#-*- coding:utf-8 -*-
import maya.cmds as cmd
import re
def dup():
    select = cmd.ls(dag=True, long=True, v=True, typ='transform')
    select.sort(key=len, reverse=True)
    # print select
    dup_total=[]
    for i in select:
        index = select.index(i)
        # print i,select[index]
        childrens = cmd.listRelatives(i, children=True, f=True) or []
        # print childrens
        if len(childrens) == 1:
            objectType = cmd.objectType(childrens)
        else:
            objectType = cmd.objectType(i)
        # print objectType
        if objectType == 'mesh':
            node=cmd.listConnections(childrens,c=False,d=False,s=True)
            #print node
            dup_total.append(node)
    del select[0:]
    test_total=[]
    dupli_total=([])
    for j in dup_total:
        if j==None:
            continue
        if j not in test_total:
            test_total.append(j)
        else:
            dupli_total.append(j)
    return dupli_total
    # if len(final_total)>0:
    #     print '有关联复制的物体'
    #     for p in final_total:
    #         cmd.select(cmd.listConnections(p,s=True),add=True)
    # else:
    #     print '没有关联复制的物体'