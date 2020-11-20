#-*- coding:utf-8 -*-
import maya.cmds as cmd
def fill():
    select = cmd.ls(dag=True, v=True, long=True, typ='transform',lt=False)
    # print select
    fill_total = []
    fill_total_name=[]
    for i in select:
        short=i.split('|')[-1]
        childrens = cmd.listRelatives(i, children=True, f=True) or []
        # print childrens
        if len(childrens) == 1:
            objectType = cmd.objectType(childrens)
            # print objectType
        else:
            objectType = cmd.objectType(i)
        # print objectType
        if objectType == 'mesh':
            chi=[]
            cmd.polySelect(i,elb=1)
            a=cmd.ls(sl=True)
            bian_mian=cmd.polyInfo(a,ef=True)
            cmd.select(clear=True)
            for k in bian_mian:
                k_two=int(str(k).split(':')[0][4:].split(' ')[-1])
                #print k_two
                chi.append(k_two)
            #print chi
            two=[]
            edge_num = cmd.polyEvaluate(i, e=True)
            for j in range(edge_num):
                two.append(j)
            for l in two:
                if l in chi:
                    continue
                # print l
                edge_name = '%s.e[%s]' % (short,l)
                #print edge_name
                every_face = str(cmd.polyInfo(edge_name,ef=True))
                #print every_face
                main = every_face.split(':')[-1]
                main_two = main.split(' ')
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
                #print children
                if len(children)==1:
                    fill_total.append(edge_name)
                    fill_total_name.append(i)
    del select[0:]
    return fill_total,fill_total_name