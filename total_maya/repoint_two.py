#-*- coding:utf-8 -*-
import maya.cmds as cmd
import re
def rep():
    select = cmd.ls(dag=True, v=True, typ='transform',lt=False)
    # print select
    l = []
    y = []
    k = []
    m = {}
    for i in select:
        #short = i.split('|')[-1]
        index = select.index(i)
        # print short
        childrens = cmd.listRelatives(i, children=True, f=True) or []
        # print childrens
        if len(childrens) == 1:
            objectType = cmd.objectType(childrens)
        else:
            objectType = cmd.objectType(i)
        # print objectType
        if objectType == 'mesh':
            if re.search('Shape',select[index]):
                    continue
            else:
                num_point=cmd.polyEvaluate(select[index],v=True)

                for i in range(0,num_point):
                    tran=[]
                    every_point='%s.vtx[%s]'%(select[index],str(i))
                    zuobiao= cmd.xform(every_point, q=True, t=True,ws=True)
                    for di in zuobiao:
                        tran.append(round(di,2))
                    #print tran
                    l.append(tran)
                    y.append(every_point)
                    m[str(tran)]=every_point
    list_point_total=[]
    #print m
    del select[0:]
    for h in l:
        if h not in k:
            k.append(h)
        else:
            list_point_total.append(m.get(str(h)))
    #print list_point_total
    return list_point_total
    # if len(list_point)>0:
    #     #print list_point
    #     cmd.select(list_point, add=True)
    #     print u'有重合点的物体是:',[set(f.split('.')[0] for f in list_point)]
    # else:
    #     print u'没有重合的点'


