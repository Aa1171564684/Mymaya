#-*- coding:utf-8 -*-
import maya.cmds as cmd
def diban():
    select = cmd.ls(dag=True, long=True, v=True, typ='transform')
    select.sort(key=len, reverse=True)
    diban_total=[]
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
            #获取点的数量
            num_point=cmd.polyEvaluate(select[index],v=True)
            for j in range(0, num_point):
                every_point = '%s.vtx[%s]' % (select[index], str(j))
                #获取点的世界坐标
                tran = cmd.xform(every_point, q=True, t=True, ws=True)[1]
                #print tran
                if tran<0:
                    diban_total.append(select[index])
    del select[0:]
    #print diban_total
    return diban_total
    # if len(diban_total)>0:
    #     print '有模型与地面穿插',diban_total
    #     cmd.select(total_diban,add=True)
    # else:
    #     print '没有模型与地面穿插'
