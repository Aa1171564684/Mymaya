#-*- coding:utf-8 -*-
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import sys
import math

nodeName='Ripple_Deformer'
nodeID=OpenMaya.MTypeId(0x1022fff)

class Ripple(OpenMayaMPx.MPxDeformerNode):

    input_Ampliyude=OpenMaya.MObject()
    input_Displayer=OpenMaya.MObject()
    input_Matrix=OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxDeformerNode.__init__(self)

    def deform(self,dataBlock,geoIterator,matrix,geometryIndex):
        #获取默认input的属性
        input = OpenMayaMPx.cvar.MPxGeometryFilter_input
        #将一个手柄附加给输入数据数组
        inputArrayHanddle=dataBlock.outputArrayValue(input)
        #利用手柄的索引获取特殊的组合属性
        inputArrayHanddle.jumpToElement(geometryIndex)
        #将一个手柄附加给这个特殊的组合属性
        inputHanddle=inputArrayHanddle.outputValue()
        #获取组合属性的需求子属性并且附加一个手柄给这个子属性
        inputGeom=OpenMayaMPx.cvar.MPxGeometryFilter_inputGeom
        inputGeomHanddle=inputHanddle.child(inputGeom)
        #获取属性的内容
        inmesh=inputGeomHanddle.asMesh()

        envelope=OpenMayaMPx.cvar.MPxGeometryFilter_envelope
        inputenvelopeHanddle=dataBlock.inputValue(envelope)
        envelopeValue=inputenvelopeHanddle.asFloat()

        inputAmpliyudeHanddle=dataBlock.inputValue(self.input_Ampliyude)
        AmpliyudeValue=inputAmpliyudeHanddle.asFloat()

        inputDisplayerHanddle=dataBlock.inputValue(self.input_Displayer)
        DisplayerValue=inputDisplayerHanddle.asFloat()

        mVector=OpenMaya.MFloatVectorArray()
        mfn_mesh=OpenMaya.MFnMesh(inmesh)
        mfn_mesh.getVertexNormals(False,mVector,OpenMaya.MSpace.kObject)

        inputMatrixHanddle=dataBlock.inputValue(self.input_Matrix)
        MatrixValue=inputMatrixHanddle.asMatrix()

        mfn_transform=OpenMaya.MTransformationMatrix(MatrixValue)
        translateValue=mfn_transform.getTranslation(OpenMaya.MSpace.kObject)

        mpoint_array=OpenMaya.MPointArray()
        while not geoIterator.isDone():
            position = geoIterator.position()
            weight = self.weightValue(dataBlock, geometryIndex, geoIterator.index())
            position.x = position.x+math.sin(geoIterator.index()+DisplayerValue+translateValue[0])*AmpliyudeValue\
                                  *mVector[geoIterator.index()].x*weight*envelopeValue
            position.y = position.y + math.sin(geoIterator.index() + DisplayerValue+translateValue[0]) * AmpliyudeValue \
                                      * mVector[geoIterator.index()].y *weight* envelopeValue
            position.z = position.z + math.sin(geoIterator.index() + DisplayerValue+translateValue[0]) * AmpliyudeValue \
                                      * mVector[geoIterator.index()].z * weight*envelopeValue
            mpoint_array.append(position)
            geoIterator.next()
        geoIterator.setAllPositions(mpoint_array)

    def accessoryNodeSetup(self,dagModifier):
        locator=dagModifier.createNode('locator')
        mfn_Depend=OpenMaya.MFnDependencyNode(locator)
        mfn_Plug=mfn_Depend.findPlug('worldMatrix')
        input_WorldSapce=mfn_Plug.attribute()
        connect_Att=dagModifier.connect(locator,input_WorldSapce,self.thisMObject(),Ripple.input_Matrix)
        return connect_Att

    def accessoryAttribute(self):
        return Ripple.input_Matrix

def NodeCreator():
    Node_Ptr=OpenMayaMPx.asMPxPtr(Ripple())
    return Node_Ptr

def Node_Initializer():
    mfn_Attr=OpenMaya.MFnNumericAttribute()
    Ripple.input_Ampliyude=mfn_Attr.create('AttributeValue','AttrVal',OpenMaya.MFnNumericData.kFloat,0.0)
    mfn_Attr.setKeyable(1)
    mfn_Attr.setMin(0.0)
    mfn_Attr.setMax(1.0)

    Ripple.input_Displayer=mfn_Attr.create('DisplaceValue','DispVal',OpenMaya.MFnNumericData.kFloat,0.0)
    mfn_Attr.setKeyable(1)
    mfn_Attr.setMin(0.0)
    mfn_Attr.setMax(10.0)

    mfn_matrixAttr=OpenMaya.MFnMatrixAttribute()
    Ripple.input_Matrix=mfn_matrixAttr.create('MatrixAttribute','Matrix')
    mfn_matrixAttr.setStorable(False)
    mfn_matrixAttr.setConnectable(True)

    try:
        Ripple.addAttribute(Ripple.input_Ampliyude)
        Ripple.addAttribute(Ripple.input_Displayer)
        Ripple.addAttribute(Ripple.input_Matrix)

        outputGeom = OpenMayaMPx.cvar.MPxGeometryFilter_outputGeom
        Ripple.attributeAffects(Ripple.input_Displayer,outputGeom)
        Ripple.attributeAffects(Ripple.input_Ampliyude,outputGeom)
        Ripple.attributeAffects(Ripple.input_Matrix,outputGeom)
    except:
        sys.stderr.write("Failed to create attributes of %s node\n"%'kPluginNodeTypeName')



def initializePlugin(mobject):
    mplugin=OpenMayaMPx.MFnPlugin(mobject,'Senlin')
    try:
        mplugin.registerNode(nodeName,nodeID,NodeCreator,Node_Initializer, OpenMayaMPx.MPxNode.kDeformerNode)
    except:
        sys.stderr.write('Failed register to command',nodeName)

def uninitializePlugin(mobject):
    mplugin=OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(nodeName)
    except:
        sys.stderr.write('Failed deregister from command',nodeName)

