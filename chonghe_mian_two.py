#-*- coding:utf-8 -*-
import maya.cmds as cmd
import pprint
#悬空面
def chong():
    select = cmd.ls(dag=True, long=True, v=True, typ='transform')
    select.sort(key=len, reverse=True)
    # print select
    dict={}
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
            #获取面数量
            mian_num=cmd.polyEvaluate(select[index],f=True)
            #print i,mian
            for j in range(mian_num):
                #获取每个面名称
                mian_name='%s.f[%s]' % (select[index], j)
                #print mian_name
                dian=str(cmd.polyInfo(mian_name,fv=True)).split(':')[-1].split(' ')
                children = []
                a=[]
                for h in dian:
                    if h == '':
                        continue
                    if h == 'n':
                        continue
                    if h == "\\n']":
                        continue
                    else:
                        children.append(int(h))
                        dian_nam='%s.vtx[%s]' % (select[index],int(h))
                        #print mian_name,man
                        #获取面上四个点的坐标
                        dian_posi=cmd.xform(dian_nam,q=True,t=True,ws=True)
                        # a.append(dian_posi)
                        #print dian_posi
                        b=[]
                        #调整精度
                        for l in dian_posi:
                            b.append(round(l,5))
                        a.append(b)
                #print mian_name,a
                #将点坐标作为键，面的名称作为值，放进dict字典
                dict[mian_name]=a
    print dict
    del select[0:]
    #pprint.pprint(dict.values())
    #创一个列表来筛选相同坐标的点
    chonghe_total=dict.values()
    #chonghe_total.append(dict.values())
    #pprint.pprint(chonghe_total)
    final_total=[]
    # for p in dict.values():
    #     pprint.pprint(p)
        #pprint.pprint(p)
        # if p not in chonghe_total:
        #     final_total.append(p)
        #     print final_total


chong()
