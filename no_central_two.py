#-*- coding:utf-8 -*-
import maya.cmds as cmd
def nocentra():
    select = cmd.ls(dag=True,v=True,long=True,typ='transform')
    select.sort(key=len, reverse=True)
    nocentral_total=[]
    for i in select:
        index = select.index(i)
        childrens = cmd.listRelatives(i, children=True,f=True) or [i]
        #print childrens
        if len(childrens) == 1:
            objectType = cmd.objectType(childrens)
            #print objectType
        else:
            objectType = cmd.objectType(i)
        #print short,objectType
        if objectType=='transform' or objectType=='mesh':
            #查询每个物体的世界坐标
            central=cmd.xform('%s.rotatePivot'%select[index],q=True,ws=True,t=True)
            if not central==[0,0,0]:
                #将坐标不在世界坐标原点的物体加入列表存储
                nocentral_total.append(select[index])
            #print central,select[index]
    #print nocentral_total
    del select[0:]
    return nocentral_total
    # if len(nocentral_total)>0:
    #     print '有物体的组不在世界坐标中心',nocentral_total
    #     cmd.select(nocentral_total,add=True)
    # else:
    #     print '没有物体的组不在世界坐标中心'
