#-*- coding:utf-8 -*-
import maya.cmds as cmd
def refe():
    select=cmd.ls(dag=True,v=True)
    reference_total=[]
    for i in select:
        refer=cmd.referenceQuery(i,inr=True)
        if refer==False:
            continue
        else:
            reference_total.append(i)
    del select[0:]
    return reference_total