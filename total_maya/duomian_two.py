#-*- coding:utf-8 -*-
import maya.cmds as cmd
def duo():
    select = cmd.ls(dag=True, v=True, long=True, typ='transform',lt=False)
    # print select
    duomian_total = []
    for i in select:
        index = select.index(i)
        childrens = cmd.listRelatives(i, children=True, f=True) or []
        # print childrens
        if len(childrens) == 1:
            objectType = cmd.objectType(childrens)
            # print objectType
        else:
            objectType = cmd.objectType(i)
        # print objectType
        if objectType == 'mesh':
            face_num = cmd.polyEvaluate(select[index], f=True)
            for j in range(face_num):
                face_name = '%s.f[%s]' % (select[index], j)
                every_edge = str(cmd.polyInfo(face_name, fe=True))
                #print every_edge
                main = every_edge.split(':')[-1]
                main_two = main.split(' ')
                #print main_two
                children = []
                for h in main_two:
                    if h == '':
                        continue
                    if h == 'n':
                        continue
                    if h == "\\n']":
                        continue
                    else:
                        children.append(h)
                if len(children) > 4:
                    duomian_total.append(face_name)
    del select[0:]
    return duomian_total