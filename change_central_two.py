#-*- coding:utf-8 -*-
import maya.cmds as cmd
def chcentra():
    select = cmd.ls(dag=True,v=True,long=True,typ='transform')
    select.sort(key=len, reverse=True)
    chcentral_total=[]
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
            central=cmd.xform('%s.rotatePivot'%select[index],q=True,t=True)
            if not central==[0,0,0]:
                chcentral_total.append(childrens)
            #print childrens,central
    del select[0:]
    #print chcentral_total
    return chcentral_total
    # if len(chcentral_total) > 0:
    #     print '有物体或者组的中心轴被改动', chcentral_total
    #     for j in chcentral_total:
    #         cmd.select(j, add=True)
    # else:
    #     print '没有物体或者组的中心轴被改动'
