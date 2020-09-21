#-*- coding:utf-8 -*-
import maya.cmds as cmd
HOU={'mesh':'GEO','joint':None,'nurbsSurface':None,'camera':None,'nurbsCircle':None,
     'pointLight':None,'areaLight':None,'volumeLight':None,'directionalLight':None,
     'ambientLight':None,'spotLight':None
     }
DEFOU='GRP'
def rename(selection=False):
    objects=cmd.ls(selection=selection,dag=True,long=True,v=True,typ='transform')
    if selection and not objects:
        raise RuntimeError(u'请选择需要更改名字的物体')
    objects.sort(key=len, reverse=True)
    for obj in objects:
        # print objects[index]
        shortName=obj.split('|')[-1]
        #print obj
        children = cmd.listRelatives(obj,children=True,f=True)or[]
        #print children
        if len(children)==1:
            child=children[0]
            objectType=cmd.objectType(child)
            #print children,objectType
        else:
            objectType=cmd.objectType(obj)
            #print children,objectType
        hou=HOU.get(objectType,DEFOU)
        if hou ==HOU['camera']:
            continue
        if hou == HOU['pointLight']:
            continue
        if hou == HOU['areaLight']:
            continue
        if hou == HOU['volumeLight']:
            continue
        if hou == HOU['spotLight']:
            continue
        if hou == HOU['directionalLight']:
            continue
        if hou == HOU['nurbsSurface']:
            continue
        if hou == HOU['nurbsCircle']:
            continue
        if hou == HOU['joint']:
            continue
        if shortName.endswith('_'+hou):
            continue
        newName='%s_%s'%(shortName,hou)
        cmd.rename(obj,newName)
        index = objects.index(obj)
        objects[index]=obj.replace(shortName,newName)
    del objects[0:]