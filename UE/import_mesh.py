import unreal
import os
mesh = 'D:/test_mesh.FX'
skeletal = 'D:/test_skele.FBX'

def creat_task(filename,destination_path,option=None):
    task = unreal.AssetImportTask()
    task.set_editor_property('automated',True)
    task.set_editor_property('destination_name','')
    task.set_editor_property('filename',filename)
    task.set_editor_property('destination_path',destination_path)
    task.set_editor_property('replace_existing',True)
    task.set_editor_property('options',option)
    task.set_editor_property('save',False)
    return task

def creat_mesh_task():
    options = unreal.FbxImportUI()
    options.set_editor_property('import_mesh',True)
    options.set_editor_property('import_texture',False)
    options.set_editor_property('import_materials',True)
    options.set_editor_property('import_as_skeletal',False)
    options.static_mesh_import_data.set_editor_property('import_translation',unreal.Vector(50,0,0))
    options.static_mesh_import_data.set_editor_property('import_rotation',unreal.Rotator(0,110,0))
    options.static_mesh_import_data.set_editor_property('import_uniform_scale',1)
    options.static_mesh_import_data.set_editor_property('combine_meshes',True)
    options.static_mesh_import_data.set_editor_property('generate_lightmap_u_vs',True)
    options.static_mesh_import_data.set_editor_property('auto_generate_collision',True)
    return options
def creat_skele_task():
    options = unreal.FbxImportUI()
    options.set_editor_property('import_mesh',True)
    options.set_editor_property('import_textures',False)
    options.set_editor_property('import_materials',True)
    options.set_editor_property('import_as_skeletal',True)
    options.skeletal_mesh_import_data.set_editor_property('import_rotation',unreal.Vector(50,0,0))
    options.skeletal_mesh_import_data.set_editor_property('import_translation',unreal.Rotator(0,110,0))
    options.skeletal_mesh_import_data.set_editor_property('import_uniform_scale',1)
    options.skeletal_mesh_import_data.set_editor_property('generate_lightmap_u_vs',True)
    options.skeletal_mesh_import_data.set_editor_property('auto_generate_collision',False)
    return options
def excute_task(tasks):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    for i in tasks:
        print ('导入路径为:'+i.get_editor_property('destination_path'))

def main():
    if os.path.exist(mesh):
        mesh_task = creat_task(mesh,'/Game/Meshs',option=creat_mesh_task())
        excute_task([mesh_task])
    if os.path.exist(skeletal):
        skele_task = creat_task(skeletal,'/Game/Skeletals'.option = creat_skele_task())
        excute_task([skele_task])
    
