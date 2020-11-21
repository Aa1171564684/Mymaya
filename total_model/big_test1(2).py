#-*- coding:utf-8 -*-
from PySide2.QtWidgets import *
import shiboken2
import maya.OpenMayaUI as mul
import maya.cmds as cmd
import rename_two
reload(rename_two)
import repoint_two
reload(repoint_two)
import checkUV_two
reload(checkUV_two)
import chaoUV_two
reload(chaoUV_two)
import stop_UV_two
reload(stop_UV_two)
import duomian_two
reload(duomian_two)
import mian_shade_two
reload(mian_shade_two)
import chong_name_two
reload(chong_name_two)
import nofreeze_two
reload(nofreeze_two)
import no_central_two
reload(no_central_two)
import one_grp_two
reload(one_grp_two)
import reference_two
reload(reference_two)
import duplicate_two
reload(duplicate_two)
import fill_hole_two
reload(fill_hole_two)
import change_central_two
reload(change_central_two)
import chao_diban_two
reload(chao_diban_two)
import del_unuse_ceng_two
reload(del_unuse_ceng_two)
import sence_youhua_two
reload(sence_youhua_two)
import duo_UVSet_two
reload(duo_UVSet_two)
#import del_light(台式机上)

class Test(QMainWindow):
    def __init__(self,parent=None):
        super(Test,self).__init__(parent)
        self.setWindowTitle('Check')
        self.a = Tool()
        self.setCentralWidget(self.a)

        self.edit = self.menuBar().addMenu('Edit')
        self.help = self.menuBar().addMenu('Help')
        self.openFile = QAction('Open', self)
        self.edit.addAction(self.openFile)
        self.close = QAction('Close',self)
        self.edit.addAction(self.close)

        Tool()
class Fix(QWidget):
    def __init__(self,parent=None):
        super(Fix,self).__init__(parent)
        self.fix(self)
    def fix(self,a):
        self.check_ = QCheckBox(a)
        self.check_Button = QPushButton('check')
        self.select_Button = QPushButton('select')
        self.fix_Button = QPushButton('fix')
        self.check_Button.setEnabled(False)
        self.select_Button.setEnabled(False)
        self.fix_Button.setEnabled(False)
        self.layout_ = QHBoxLayout()
        self.layout_.addWidget(self.check_Button)
        self.layout_.addWidget(self.select_Button)
        self.layout_.addWidget(self.fix_Button)
        self.layoutt_ = QHBoxLayout()
        self.layoutt_.addWidget(self.check_)
        self.layoutt_.addLayout(self.layout_)
        self.layoutt_.setStretch(0,1)
        self.check_.stateChanged.connect(self.check_Button.setEnabled)
        self.check_.stateChanged.connect(self.select_Button.setEnabled)
        self.check_.stateChanged.connect(self.fix_Button.setEnabled)
        return self.layoutt_
class Check(QWidget):
    def __init__(self,parent = None):
        super(Check, self).__init__(parent)
        self.check(self)
    def check(self,b):
        self.check_1 = QCheckBox(b)
        self.check_1Button = QPushButton('check')
        self.select_1Button = QPushButton('select')
        self.check_1Button.setEnabled(False)
        self.select_1Button.setEnabled(False)
        self.la = QLabel('       ')
        self.layout_1 = QHBoxLayout()
        self.layout_1.addWidget(self.check_1Button)
        self.layout_1.addWidget(self.select_1Button)
        self.layout_1.addWidget(self.la)
        self.layoutt_1 = QHBoxLayout()
        self.layoutt_1.addWidget(self.check_1)
        self.layoutt_1.addLayout(self.layout_1)
        self.layoutt_1.setStretch(0,1)
        self.check_1.stateChanged.connect(self.check_1Button.setEnabled)
        self.check_1.stateChanged.connect(self.select_1Button.setEnabled)
        return self.layoutt_1

class Per(QWidget):
    def __init__(self, parent=None):
        super(Per, self).__init__(parent)
        self.per(self)
    def per(self,c):
        self.check_2 = QCheckBox(c)
        self.per_2=QPushButton('perform')
        self.per_2.setEnabled(False)
        self.lable = QLabel('                    ')
        self.layout_2 = QHBoxLayout()
        self.layout_2.addWidget(self.per_2)
        self.layout_2.addWidget(self.lable)
        self.layoutt_2 = QHBoxLayout()
        self.layoutt_2.addWidget(self.check_2)
        self.layoutt_2.addLayout(self.layout_2)
        self.layoutt_2.setStretch(0,1)
        self.check_2.stateChanged.connect(self.per_2.setEnabled)
        return self.layoutt_2
class Tool(QToolBox):
    def __init__(self,parent=None):
        super(Tool,self).__init__(parent)
        Fix()
        Check()
        Per()
        self.tool1()
        self.tool2()
        self.tool3()
        self.tool4()
        self.tool5()
    def tool1(self):
        self.group1 = QGroupBox()
        self.vlay1 = QVBoxLayout(self.group1)
        a=Fix()
        self.vlay1.addLayout(a.fix(u'查找开口边-可为开口处补洞'))
        a.check_Button.clicked.connect(self.hole)
        self.select___button_fillhole=a.select_Button
        self.select___button_fillhole.clicked.connect(self.select_fillhole)
        self.fix__button_fillhole=a.fix_Button
        self.fix__button_fillhole.clicked.connect(self.fix_fillhole)
        b=Fix()
        self.vlay1.addLayout(b.fix(u'查找开口边-可为开口处加1圈环绕'))
        b.check_Button.clicked.connect(self.add)
        c=Fix()
        self.vlay1.addLayout(c.fix(u'检查点重合'))
        c.check_Button.clicked.connect(self.every_point1)
        self.select___button_repoint=c.select_Button
        self.select___button_repoint.clicked.connect(self.select_repoint)
        d=Fix()
        self.vlay1.addLayout(d.fix(u'检查多边面'))
        d.check_Button.clicked.connect(self.duomian)
        self.select___button_mian=d.select_Button
        self.select___button_mian.clicked.connect(self.select_mian)
        e=Fix()
        self.vlay1.addLayout(e.fix(u'是否有非法面'))
        e.check_Button.clicked.connect(self.feimian)
        f=Per()
        self.vlay1.addLayout(f.per(u'如果场景中存在Reference物体就给予警告'))
        f.per_2.clicked.connect(self.reference)
        g=Check()
        self.vlay1.addLayout(g.check(u'是否存在关联复制物体'))
        g.check_1Button.clicked.connect(self.recopy)
        self.select___button_duplicate=g.select_1Button
        self.select___button_duplicate.clicked.connect(self.select_dup)
        g=Per()
        self.vlay1.addLayout(g.per(u'删除所有历史'))
        g.per_2.clicked.connect(self.delhistory)
        i=Check()
        self.vlay1.addLayout(i.check(u'是否存在面赋予材质的物体'))
        i.check_1Button.clicked.connect(self.mianfuyu)
        self.select___button_mianfuyu=i.select_1Button
        self.select___button_mianfuyu.clicked.connect(self.select_mianfuyu)
        h=Fix()
        self.vlay1.addLayout(h.fix(u'检查多边形面的法线是否正确(单片物体可以忽略检查)'))
        h.check_Button.clicked.connect(self.normal)
        self.vlay1.addStretch(1)
        self.addItem(self.group1,'GEO CHECK')

    def tool2(self):
        self.group2 = QGroupBox()
        self.vlay2 = QVBoxLayout(self.group2)
        a=Check()
        self.vlay2.addLayout(a.check(u'是否有几何体与地面穿插'))
        a.check_1Button.clicked.connect(self.chuacha)
        self.select___button_chuancha=a.select_1Button
        self.select___button_chuancha.clicked.connect(self.select_chuan)
        b=Per()
        self.vlay2.addLayout(b.per(u'检查物体顶层是否符合只有一个组的规范并把该组轴心归零'))
        b.per_2.clicked.connect(self.fuhezu)
        c=Per()
        self.vlay2.addLayout(c.per(u'冻结变形属性'))
        c.per_2.clicked.connect(self.freeze)
        d=Fix()
        self.vlay2.addLayout(d.fix(u'是否有几何体和组未冻结'))
        d.check_Button.clicked.connect(self.nofreeze)
        self.select___button_nofreeze=d.select_Button
        self.select___button_nofreeze.clicked.connect(self.select_nofreeze)
        self.fix__button_nofreeze=d.fix_Button
        self.fix__button_nofreeze.clicked.connect(self.fix_nofreeze)
        e=Fix()
        self.vlay2.addLayout(e.fix(u'是否有几何体和组的中心轴不在世界坐标0点位置'))
        e.check_Button.clicked.connect(self.nocenter)
        self.select___button_nocenter=e.select_Button
        self.select___button_nocenter.clicked.connect(self.select_nocen)
        self.fix__button_nocenter=e.fix_Button
        self.fix__button_nocenter.clicked.connect(self.fix_nocen)
        f=Fix()
        self.vlay2.addLayout(f.fix(u'是否有几何体和组的中心轴被改动'))
        f.check_Button.clicked.connect(self.centerchange)
        self.select___button_change=f.select_Button
        self.select___button_change.clicked.connect(self.select_change)
        self.fix__button_change=f.fix_Button
        self.fix__button_change.clicked.connect(self.fix_change)
        self.vlay2.addStretch(1)
        self.addItem(self.group2,'TRANSFORM CHECK')
    def tool3(self):
        self.group3 = QGroupBox()
        self.vlay3 = QVBoxLayout(self.group3)
        a=Per()
        self.vlay3.addLayout(a.per(u'为所有的几何体和组赋予规范编号'))
        a.per_2.clicked.connect(self.givebianhao)
        b=Per()
        self.vlay3.addLayout(b.per(u'为所有的几何体和组赋予规范后缀_GEO/_PLY/_GRP'))
        b.per_2.clicked.connect(self.givename)
        c=Check()
        self.vlay3.addLayout(c.check(u'是否存在重命名的几何体或组'))
        c.check_1Button.clicked.connect(self.renamee)
        self.select___button = c.select_1Button
        self.select___button.clicked.connect(self.select_name)
        self.vlay3.addStretch(1)
        self.addItem(self.group3,'NAMING CONVENSIONS')

    def tool4(self):
        self.group4 = QGroupBox()
        self.vlay4 = QVBoxLayout(self.group4)
        a=Check()
        self.vlay4.addLayout(a.check(u'是否存在为缝合的UV'))
        a.check_1Button.clicked.connect(self.splitUV)
        b=Check()
        self.vlay4.addLayout(b.check(u'是否有UV卡在象限边界(与边界重合)'))
        b.check_1Button.clicked.connect(self.chongheUV)
        self.select___button_stopUV=b.select_1Button
        self.select___button_stopUV.clicked.connect(self.select_stopUV)
        c=Check()
        self.vlay4.addLayout(c.check(u'是否有UV不在第一象限内'))
        c.check_1Button.clicked.connect(self.noone)
        self.select___button_chaoUV=c.select_1Button
        self.select___button_chaoUV.clicked.connect(self.select_chaoUV)
        d=Check()
        self.vlay4.addLayout(d.check(u'是否存在无UV的物体'))
        d.check_1Button.clicked.connect(self.noUV)
        self.select___button_noUV = d.select_1Button
        self.select___button_noUV.clicked.connect(self.select_noUV)
        e=Fix()
        self.vlay4.addLayout(e.fix(u'是否存在一个物体有多个UVSet'))
        e.check_Button.clicked.connect(self.duoUVset)
        self.select___button_duoset=e.select_Button
        self.select___button_duoset.clicked.connect(self.select_duoset)
        self.fix__button_duoset=e.fix_Button
        self.fix__button_duoset.clicked.connect(self.fix_duoset)
        self.vlay4.addStretch(1)
        self.addItem(self.group4, 'UV CHECKING')

    def tool5(self):
        self.group5 = QGroupBox()
        self.vlay5 = QVBoxLayout(self.group5)
        a=Per()
        self.vlay5.addLayout(a.per(u'删除所有层和所有不使用的节点并做常规清理(模型元素使用)'))
        a.per_2.clicked.connect(self.delunusenode)
        b=Per()
        self.vlay5.addLayout(b.per(u'删除所有用户创建的Turtle节点/自定义插件节点'))
        b.per_2.clicked.connect(self.delmakenode)
        c=Per()
        self.vlay5.addLayout(c.per(u'删除所有用户创建的灯光/摄像机/灯光连接'))
        c.per_2.clicked.connect(self.dellight)
        d=Per()
        self.vlay5.addLayout(d.per(u'删除不使用的层和节点(绑定与动画场景使用)'))
        d.per_2.clicked.connect(self.delonenode)
        self.vlay5.addStretch(1)
        self.addItem(self.group5, 'SENCE CHECKE')
    def hole(self):
        self.fill_total,self.fill_total_name=fill_hole_two.fill()
        if len(self.fill_total) == 0:
            button_no = QMessageBox.information(self, u'提示', u'没有模型需要补洞', QMessageBox.Ok | QMessageBox.Close,
                                                QMessageBox.Ok)
            if button_no == QMessageBox.Ok or QMessageBox.Close:
                self.select___button_fillhole.setEnabled(False)
                self.fix__button_fillhole.setEnabled(False)
        else:
            button = QMessageBox.information(self, u'提示', u'请点击select列出属性未冻结的模型,用Fix将属性冻结', QMessageBox.Ok | QMessageBox.Close,
                                             QMessageBox.Ok)
            if button == QMessageBox.Ok:
                self.select___button_fillhole.setEnabled(True)
                self.fix__button_fillhole.setEnabled(True)
    def select_fillhole(self):
        cmd.select(self.fill_total_name,add=True)
    def fix_fillhole(self):
        cmd.select(clear=True)
        for n in self.fill_total:
            cmd.select(n)
            cmd.polyCloseBorder()
    def add(self):
        print 'add'
    def every_point1(self):
        self.list_point_total=repoint_two.rep()
        if len(self.list_point_total) == 0:
            button_no=QMessageBox.information(self, u'提示', u'没有重合的点', QMessageBox.Ok | QMessageBox.Close, QMessageBox.Ok)
            if button_no==QMessageBox.Ok or QMessageBox.Close:
                self.select___button_repoint.setEnabled(False)
        else:
            button = QMessageBox.information(self, u'提示', u'请点击select选择重合点', QMessageBox.Ok | QMessageBox.Close,
                                             QMessageBox.Ok)
            if button == QMessageBox.Ok:
                self.select___button_repoint.setEnabled(True)
    def select_repoint(self):
        cmd.select(self.list_point_total, add=True)
    def duomian(self):
        self.duomian_total=duomian_two.duo()
        #print  total
        if len(self.duomian_total) == 0:
            button_no=QMessageBox.information(self, u'提示', u'没有多边面的模型', QMessageBox.Ok | QMessageBox.Close, QMessageBox.Ok)
            if button_no==QMessageBox.Ok or QMessageBox.Close:
                self.select___button_mian.setEnabled(False)
        else:
            button = QMessageBox.information(self, u'提示', u'请点击select列出多边面', QMessageBox.Ok | QMessageBox.Close,
                                             QMessageBox.Ok)
            if button == QMessageBox.Ok:
                self.select___button_mian.setEnabled(True)
                # return self.total
    def select_mian(self):
        cmd.select(self.duomian_total, add=True)
        print u'多边面是',set(self.duomian_total)
    def feimian(self):
        pass
    def reference(self):
        self.reference_total=reference_two.refe()
        if len(self.reference_total)==0:
            QMessageBox.warning(self, u'提示', u'场景内没有reference的物体', QMessageBox.Ok)
        else:
            QMessageBox.warning(self, u'提示', u'场景内存在reference的物体', QMessageBox.Ok)
    def recopy(self):
        self.dupli_total=duplicate_two.dup()
        if len(self.dupli_total) == 0:
            button_no = QMessageBox.information(self, u'提示', u'没有关联复制的物体', QMessageBox.Ok | QMessageBox.Close,
                                                QMessageBox.Ok)
            if button_no == QMessageBox.Ok or QMessageBox.Close:
                self.select___button_duplicate.setEnabled(False)
        else:
            button = QMessageBox.information(self, u'提示', u'请点击select列出关联复制的物体', QMessageBox.Ok | QMessageBox.Close,
                                             QMessageBox.Ok)
            if button == QMessageBox.Ok:
                self.select___button_duplicate.setEnabled(True)
    def select_dup(self):
        for p in self.dupli_total:
            cmd.select(cmd.listConnections(p,s=True),add=True)
    def delhistory(self):
        select=cmd.ls(sl=True)
        if len(select) <= 0:
            QMessageBox.warning(self, u'提示', u'请选择物体', QMessageBox.Ok | QMessageBox.Close,
                                            QMessageBox.Ok)
        else:
            print '历史已删除'
            cmd.delete(select,ch=True)
    def mianfuyu(self):
        self.shade_total=mian_shade_two.shade()
        if len(self.shade_total)<=0:
            button_no=QMessageBox.warning(self, u'提示', u'场景内没有模型被赋予面材质', QMessageBox.Ok | QMessageBox.Close, QMessageBox.Ok)
            if button_no == QMessageBox.Ok or QMessageBox.Close:
                self.select___button_mianfuyu.setEnabled(False)
        else:
            button = QMessageBox.information(self, u'提示', u'请点击select列出面赋予材质的模型', QMessageBox.Ok | QMessageBox.Close,
                                             QMessageBox.Ok)
            if button == QMessageBox.Ok:
                self.select___button_mianfuyu.setEnabled(True)
    def select_mianfuyu(self):
        cmd.select(self.shade_total,add=True)
        print '有多边面赋予的模型是:',self.shade_total
    def normal(self):
        pass
    def chuacha(self):
        self.diban_total=chao_diban_two.diban()
        if len(self.diban_total) == 0:
            button_no = QMessageBox.information(self, u'提示', u'没有物体与地面穿插', QMessageBox.Ok | QMessageBox.Close,
                                                QMessageBox.Ok)
            if button_no == QMessageBox.Ok or QMessageBox.Close:
                self.select___button_chuancha.setEnabled(False)
        else:
            button = QMessageBox.information(self, u'提示', u'请点击select列出与地面穿插的物体', QMessageBox.Ok | QMessageBox.Close,
                                             QMessageBox.Ok)
            if button == QMessageBox.Ok:
                self.select___button_chuancha.setEnabled(True)
    def select_chuan(self):
        cmd.select(self.diban_total,add=True)
    def fuhezu(self):
        self.onegrp_total=one_grp_two.one()
        if len(self.onegrp_total) <= 0:
            QMessageBox.warning(self, u'提示', u'所有的组符合规范', QMessageBox.Ok | QMessageBox.Close,
                                QMessageBox.Ok)
        else:
            print '已选中不符合规范的组，并把轴心归零'
            for p in self.onegrp_total:
                cmd.select(p,add=True)
    def freeze(self):
        select=cmd.ls(sl=True)
        if len(select) <= 0:
            QMessageBox.warning(self, u'提示', u'请选择物体', QMessageBox.Ok | QMessageBox.Close,
                                            QMessageBox.Ok)
        else:
            print '属性已冻结'
        cmd.FreezeTransformations(select)
    def nofreeze(self):
        self.nofreeze_total=nofreeze_two.nofree()
        if len(self.nofreeze_total) == 0:
            button_no = QMessageBox.information(self, u'提示', u'所有物体属性已经冻结', QMessageBox.Ok | QMessageBox.Close,
                                                QMessageBox.Ok)
            if button_no == QMessageBox.Ok or QMessageBox.Close:
                self.select___button_nofreeze.setEnabled(False)
                self.fix__button_nofreeze.setEnabled(False)
        else:
            button = QMessageBox.information(self, u'提示', u'请点击select列出属性未冻结的模型,用Fix将属性冻结', QMessageBox.Ok | QMessageBox.Close,
                                             QMessageBox.Ok)
            if button == QMessageBox.Ok:
                self.select___button_nofreeze.setEnabled(True)
                self.fix__button_nofreeze.setEnabled(True)
    def select_nofreeze(self):
        cmd.select(self.nofreeze_total, add=True)
        print self.nofreeze_total, u'的属性未冻结'
    def fix_nofreeze(self):
        cmd.FreezeTransformations(self.nofreeze_total)
    def nocenter(self):
        self.nocentral_total = no_central_two.nocentra()
        if len(self.nocentral_total) == 0:
            button_no = QMessageBox.information(self, u'提示', u'没有物体的组不在世界坐标中心', QMessageBox.Ok | QMessageBox.Close,
                                                QMessageBox.Ok)
            if button_no == QMessageBox.Ok or QMessageBox.Close:
                self.select___button_nocenter.setEnabled(False)
                self.fix__button_nocenter.setEnabled(False)
        else:
            button = QMessageBox.information(self, u'提示', u'请点击select列出物体的组不在世界坐标中心的模型,用Fix将轴心归零',
                                             QMessageBox.Ok | QMessageBox.Close,
                                             QMessageBox.Ok)
            if button == QMessageBox.Ok:
                self.select___button_nocenter.setEnabled(True)
                self.fix__button_nocenter.setEnabled(True)
    def select_nocen(self):
        cmd.select(self.nocentral_total, add=True)
    def fix_nocen(self):
        for p in self.nocentral_total:
            cmd.xform(p, rp=[0, 0, 0], ws=True)
    def centerchange(self):
        self.chcentral_total = change_central_two.chcentra()
        if len(self.chcentral_total) == 0:
            button_no = QMessageBox.information(self, u'提示', u'没有组或物体的中心轴被改变过', QMessageBox.Ok | QMessageBox.Close,
                                                QMessageBox.Ok)
            if button_no == QMessageBox.Ok or QMessageBox.Close:
                self.select___button_change.setEnabled(False)
                self.fix__button_change.setEnabled(False)
        else:
            button = QMessageBox.information(self, u'提示', u'请点击select列出中心轴被改变过的物体或组,用Fix将轴心归零',
                                             QMessageBox.Ok | QMessageBox.Close,
                                             QMessageBox.Ok)
            if button == QMessageBox.Ok:
                self.select___button_change.setEnabled(True)
                self.fix__button_change.setEnabled(True)
    def select_change(self):
        for j in self.chcentral_total:
            cmd.select(j, add=True)
    def fix_change(self):
        pass
    def givebianhao(self):
        print 'givebianhao'
    def givename(self):
        rename_two.rename()
    def renamee(self):
        self.k,self.l=chong_name_two.ren()
        if len(self.k)==0 and len(self.l)== 0:
            button_no=QMessageBox.information(self, u'提示', u'没有名称重名称的模型和模型', QMessageBox.Ok|QMessageBox.Close,QMessageBox.Ok)
            if button_no==QMessageBox.Ok or QMessageBox.Close:
                self.select___button.setEnabled(False)
        if not len(self.k)==0 or not len(self.l)==0:
            button=QMessageBox.question(self, u'提示', u'请用select列出重名称的模型或组', QMessageBox.Ok|QMessageBox.Close,QMessageBox.Ok)
            if button==QMessageBox.Ok:
                self.select___button.setEnabled(True)
    def select_name(self):
        GEO=set(self.k)
        GRP=set(self.l)
        for i in GEO:
            print i, u'物体的名称重复了'
            #cmd.select(i,add=True)
        for j in GRP:
            print j, u'组的名称重复了'
            #cmd.select(j,add=True)
    def splitUV(self):
        print 'splitUV'
    def chongheUV(self):
        self.stopUV_total=stop_UV_two.stop()
        # print total_name
        if len(self.stopUV_total) == 0:
            button_no = QMessageBox.information(self, u'提示', u'没有物体的UV卡在象限边界', QMessageBox.Ok | QMessageBox.Close,
                                                QMessageBox.Ok)
            if button_no == QMessageBox.Ok or QMessageBox.Close:
                self.select___button_stopUV.setEnabled(False)
        else:
            button = QMessageBox.information(self, u'提示', u'请点击select列出UV卡在象限边界的模型', QMessageBox.Ok | QMessageBox.Close,
                                             QMessageBox.Ok)
            if button == QMessageBox.Ok:
                self.select___button_stopUV.setEnabled(True)

    def select_stopUV(self):
        cmd.select(self.stopUV_total, add=True)
        print self.stopUV_total, u'的UV卡在象限边界'
    def noone(self):
        self.chaoUV_total=chaoUV_two.chao()
        if len(self.chaoUV_total) == 0:
            button_no=QMessageBox.information(self, u'提示', u'没有物体的UV超出第一象限', QMessageBox.Ok | QMessageBox.Close,
                                             QMessageBox.Ok)
            if button_no==QMessageBox.Ok or QMessageBox.Close:
                self.select___button_chaoUV.setEnabled(False)
        else:
            button = QMessageBox.information(self, u'提示', u'请点击select列出UV超出第一象限的模型', QMessageBox.Ok | QMessageBox.Close,
                                      QMessageBox.Ok)
            if button==QMessageBox.Ok:
                self.select___button_chaoUV.setEnabled(True)
    def select_chaoUV(self):
        cmd.select(self.chaoUV_total, add=True)
        print self.chaoUV_total, u'的UV超出第一象限'
    def noUV(self):
        self.noUV_total=checkUV_two.no()
        if not len(self.noUV_total) == 0:
            button = QMessageBox.information(self, u'提示', u'请点击select列出没有UV的模型', QMessageBox.Ok | QMessageBox.Close,
                                        QMessageBox.Ok)
            if button==QMessageBox.Ok:
                self.select___button_noUV.setEnabled(True)
        else:
            button_two = QMessageBox.information(self, u'提示', u'所有模型都有UV', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Ok)
            if button_two==QMessageBox.Ok or QMessageBox.Close:
                self.select___button_noUV.setEnabled(False)
    def select_noUV(self):
        if not len(self.noUV_total) == 0:
            cmd.select(self.noUV_total, add=True)
            print self.noUV_total
        else:
            pass
    def duoUVset(self):
        self.set_total = duo_UVSet_two.duo_set()
        if len(self.set_total) == 0:
            button_no = QMessageBox.information(self, u'提示', u'所有模型都只有一个UVSet', QMessageBox.Ok | QMessageBox.Close,
                                                QMessageBox.Ok)
            if button_no == QMessageBox.Ok or QMessageBox.Close:
                self.select___button_duoset.setEnabled(False)
                self.fix__button_duoset.setEnabled(False)
        else:
            button = QMessageBox.information(self, u'提示', u'请点击select列出存在多个UVSet的模型',
                                             QMessageBox.Ok | QMessageBox.Close,
                                             QMessageBox.Ok)
            if button == QMessageBox.Ok:
                self.select___button_duoset.setEnabled(True)
                self.fix__button_duoset.setEnabled(True)
    def select_duoset(self):
        cmd.select(self.set_total, add=True)
    def fix_duoset(self):
        pass
    def delunusenode(self):
        sence_youhua_two.optimize()
    def delmakenode(self):
        print 'delmakenode'
    def dellight(self):
        print 'dellight'
    def delonenode(self):
        del_unuse_ceng_two.unuse()

if __name__=='__main__':
    a = Test()
    a.show()