#-*- coding:utf-8 -*-
import maya.cmds as cmd
def stop():
    select = cmd.ls(dag=True, long=True,v=True, typ='transform',lt=False)
    select.sort(key=len, reverse=True)
    total_num=[]
    stopUV_total=[]
    # print select
    for i in select:
        #print select
        index = select.index(i)
        #short = i.split('|')[-1]
        #print short
        #print select[index]
        childrens = cmd.listRelatives(i, children=True, f=True) or []
        #print childrens
        if len(childrens) == 1:
            objectType = cmd.objectType(childrens)
            # print objectType
        else:
            objectType = cmd.objectType(i)
        #print objectType
        if objectType == 'mesh':
            uv_map = cmd.polyListComponentConversion(select[index], tuv=True)
            #print uv_map
            cmd.select(uv_map, add=True)
            b = cmd.polyEvaluate(select[index], uvc=True)
            # print childrens[-1]
            for i in range(b):
                name = '%s.map[%s]' % (select[index], i)
                #print name
                zuobiao = cmd.polyEditUV(name, q=True)
                if zuobiao==None:
                    continue
                #print zuobiao
                cmd.select(clear=True)
                for j in zuobiao:
                    if j == 0 :
                        total_num.append(j)
                        if select[index] not in stopUV_total:
                            stopUV_total.append(select[index])
                        else:
                            continue
                    else:
                        continue
    del select[0:]
    return stopUV_total