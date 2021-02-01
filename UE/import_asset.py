import unreal
texture = 'D:/test.png'
music = 'D:/test.WAV'

def creat_task(filename,destination_path):
    task = unreal.AssetImportTask()
    task.set_editor_property('automated',True)
    task.set_editor_property('destination_name','')
    task.set_editor_property('filename',filename)
    task.set_editor_property('destination_path',destination_path)
    task.set_editor_property('replace_existing',True)
    task.set_editor_property('save',False)
    return task

def excute_task(tasks):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    for i in tasks:
        print ('导入路径为:'+i.get_editor_property('destination_path'))

def main():
    texture_task = creat_task(texture,'/Game/Texture')
    music_task = creat_task(music,'/Game/music')
    excute_task([texture_task,music_task])
