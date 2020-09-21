#-*- coding:utf-8 -*-
import maya.cmds as cmd
def chao():
    select = cmd.ls(dag=True, long=True, v=True, typ='transform')
    select.sort(key=len, reverse=True)
    total_num = []
    chaoUV_total = []
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
            uv_map = cmd.polyListComponentConversion(select[index], tuv=True)
            # print uv_map
            cmd.select(uv_map, add=True)
            b = cmd.polyEvaluate(select[index], uvc=True)
            for i in range(b):
                name = '%s.map[%s]' % (select[index], i)
                # print name
                zuobiao = cmd.polyEditUV(name, q=True)
                if zuobiao == None:
                    continue
                cmd.select(clear=True)
                # print name,zuobiao
                for j in zuobiao:
                    if j > 1 or j < 0:
                        total_num.append(j)
                        if select[index] not in chaoUV_total:
                            chaoUV_total.append(select[index])
                        else:
                            continue
                    else:
                        continue
    del select[0:]
    return chaoUV_total