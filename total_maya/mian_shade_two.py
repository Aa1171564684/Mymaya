#-*- coding:utf-8 -*-
import maya.cmds as cmd
def shade():
    select = cmd.ls(dag=True, long=True, v=True, typ='transform')
    select.sort(key=len, reverse=True)
    shade_total=[]
    # print select
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
            #找出一个模型的拥有的材质的节点
            shade_jie=cmd.listConnections(childrens,t='shadingEngine',s=True,d=True)
            #print select[index],shade_jie
            if len(shade_jie)>1:
                shade_total.append(select[index])
    del select[0:]
    #print shade_total
    return shade_total
    # if len(shade_total)>0:
    #     print '有模型被赋予面材质',shade_total
    #     cmd.select(shade_total,add=True)
    # else:
    #     print '没有模型被赋予面材质'
