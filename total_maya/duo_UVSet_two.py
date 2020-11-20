#-*- coding:utf-8 -*-
import maya.cmds as cmd
def duo_set():
    select = cmd.ls(dag=True, long=True, v=True, typ='transform')
    select.sort(key=len, reverse=True)
    # print select
    set_total=[]
    total_set_two=[]
    for i in select:
        childrens = cmd.listRelatives(i, children=True, f=True) or []
        # print childrens
        if len(childrens) == 1:
            objectType = cmd.objectType(childrens)
        else:
            objectType = cmd.objectType(i)
        # print objectType
        if objectType == 'mesh':
            num_set=cmd.polyUVSet(i,q=True,auv=True)#查询每个模型的UVSet的数量
            # print num_set
            if len(num_set)>1:
                set_total.append(i)#将UVSet数量大于一的模型添加进total_set列表
    del select[0:]
    return set_total
    # if len(total_set)>0:
    #     print total_set,'存在多个UVSet'
    #     cmd.select(total_set,add=True)
    # else:
    #     print '所有模型都只有一个UVSet'
