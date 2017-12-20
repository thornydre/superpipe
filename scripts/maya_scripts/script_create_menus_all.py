import maya.cmds as cmds
from os import path, listdir, mkdir, remove
from shutil import copyfile

cmds.menu(l = "SuperPipe", p = "MayaWindow")
cmds.menuItem(l = "Save", c = "override_save()")
cmds.menuItem(l = "Increment and Save", c = "incremental_save()")

def override_save():
    current_file_ext = cmds.file(query = True, sceneName = True)
    current_file = current_file_ext.strip(".ma")
    directory = path.dirname(current_file_ext)
    file_name = path.basename(current_file)
    
    ## SCREENSHOT ##
    frm = cmds.getAttr("defaultRenderGlobals.imageFormat")
    cmds.setAttr("defaultRenderGlobals.imageFormat", 0)
    if "edits" in directory:
        if not path.isdir(directory + "/../../images/screenshots"):
            mkdir(directory + "/../../images/screenshots")
        cmds.playblast(frame = 1, format = "image", cf = directory + "/../../images/screenshots/" + file_name + ".gif", v = False, wh = (498, 270), p = 100, orn = False)
    else:
        if not path.isdir(directory + "/../images/screenshots"):
            mkdir(directory + "/../images/screenshots")
        cmds.playblast(frame = 1, format = "image", cf = directory + "/../images/screenshots/" + file_name + ".gif", v = False, wh = (498, 270), p = 100, orn = False)
    
    cmds.setAttr("defaultRenderGlobals.imageFormat", frm)
    
    ## SAVE ##
    cmds.file(save = True, type = "mayaAscii")
    
def incremental_save():
    current_file_ext = cmds.file(query = True, sceneName = True)
    current_file = current_file_ext.strip(".ma")
    directory = path.dirname(current_file_ext)
    file_name = path.basename(current_file)
    
    if "edits" in directory:
        for f in listdir(directory + "/.."):
            if file_name[:-2] in f:
                current_file_ext = f
                current_file = current_file_ext.strip(".ma")
                version = int(current_file[-2:]) + 1
    else:
        version = int(file_name[-2:]) + 1
    
    if version < 10:
        new_file_name = file_name[:-2] + "0" + str(version)
    else:
        new_file_name = file_name[:-2] + str(version)
    
    ## SCREENSHOT ##
    frm = cmds.getAttr("defaultRenderGlobals.imageFormat")
    cmds.setAttr("defaultRenderGlobals.imageFormat", 0)
    if "edits" in directory:
        if not path.isdir(directory + "/../../images/screenshots"):
            mkdir(directory + "/../../images/screenshots")
        cmds.playblast(frame = 1, format = "image", cf = directory + "/../../images/screenshots/" + new_file_name + ".gif", v = False, wh = (498, 270), p = 100, orn = False)
    else:
        if not path.isdir(directory + "/../images/screenshots"):
            mkdir(directory + "/../images/screenshots")
        cmds.playblast(frame = 1, format = "image", cf = directory + "/../images/screenshots/" + new_file_name + ".gif", v = False, wh = (498, 270), p = 100, orn = False)
    
    cmds.setAttr("defaultRenderGlobals.imageFormat", frm)
    
    ## SAVE ##
    if "edits" in directory:
        cmds.file(rename = directory + "/../" + new_file_name + ".ma")
        cmds.file(save = True, type = "mayaAscii")
        copyfile(directory + "/../" + current_file_ext, directory + "/" + current_file_ext)
        remove(directory + "/../" + current_file_ext)
    else:
        cmds.file(rename = directory + "/" + new_file_name + ".ma")
        cmds.file(save = True, type = "mayaAscii")
        copyfile(current_file_ext, directory + "/edits/" + file_name + ".ma")
        remove(current_file_ext)