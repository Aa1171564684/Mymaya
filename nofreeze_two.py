#-*- coding:utf-8 -*-
import maya.cmds as cmd
def nofree():
    select = cmd.ls(dag=True,v=True,long=True,typ='transform')
    select.sort(key=len, reverse=True)
    nofreeze_total=[]
    for i in select:
        short = i.split('|')[-1]
        index = select.index(i)
        #print short
        childrens = cmd.listRelatives(i, children=True,f=True) or []
        #print childrens
        if len(childrens) == 1:
            objectType = cmd.objectType(childrens)
            #print objectType
        else:
            objectType = cmd.objectType(i)
        #print short,objectType
        if objectType=='transform' or objectType=='mesh':
            #print select[index]
            message=cmd.xform(select[index],q=True,t=True)
            rota=cmd.xform(select[index],q=True,ro=True)
            scal=cmd.xform(select[index],q=True,scale=True,r=True)
            if message==[0,0,0,] and rota==[0,0,0] and scal==[1,1,1]:
                continue
            else:
                nofreeze_total.append(select[index])
    del select[0:]
    return nofreeze_total