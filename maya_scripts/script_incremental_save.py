import maya.cmds as cmds
from os import path, remove, listdir
from shutil import copyfile

window = cmds.window(title = "SupeRig", iconName = "SupeRig", widthHeight = (200, 400), sizeable = False, resizeToFitChildren = True)
cmds.columnLayout(adjustableColumn = True)

cmds.scrollField("comment_textfield", wordWrap = True, enterCommand = ("submitCommand()"))
cmds.button("submit_button", label = "Submit", command = ("submitCommand()"))
cmds.button("cancel_button", label = "Cancel", command = ("cmds.deleteUI(\'" + window + "\', window = True)"))
cmds.showWindow(window)

def submitCommand():
    comment = cmds.scrollField("comment_textfield", q = True, text = True)
    incrementalSave(comment)
    cmds.deleteUI(window, window = True)

def incrementalSave(comment):
    current_file_ext = cmds.file(query = True, expandName = True)
    current_file = current_file_ext.strip(".ma")
    directory = path.dirname(current_file_ext)
    file_name = path.basename(current_file)

    version = int(file_name[-2:]) + 1

    if "edits" in directory:
        for f in listdir(directory + "/.."):
            if file_name[:-2] in f:
                current_file_ext = f
                current_file = current_file_ext.strip(".ma")
                version = int(current_file[-2:]) + 1

    if version < 10:
        new_file_name = file_name[:-2] + "0" + str(version)
    else:
        new_file_name = file_name[:-2] + str(version)

    ## COMMENT ##
    final_comment = file_name + ".ma\n---\n" + comment + "\n---\n"
    if "edits" in directory:
        with open(directory + "/../../data/versions_data.spi", "a") as f:
            f.write(final_comment)
    else:
        with open(directory + "/../data/versions_data.spi", "a") as f:
            f.write(final_comment)
        f.close()

    ## SCREENSHOT ##
    frm = cmds.getAttr("defaultRenderGlobals.imageFormat")
    cmds.setAttr("defaultRenderGlobals.imageFormat", 0)
    if "edits" in directory:
        if not path.isdir(directory + "/../../images/screenshots"):
            mkdir(directory + "/../../images/screenshots")
        cmds.playblast(frame = 1, format = "image", cf = directory + "/../../images/screenshots/" + new_file_name + ".gif", v = False, wh = (498, 270), p = 100, orn = False, os = True)
        cmds.playblast(frame = 1, format = "image", cf = directory + "/../../images/screenshots/" + new_file_name + "_small.gif", v = False, wh = (249, 135), p = 100, orn = False, os = True)
    else:
        if not path.isdir(directory + "/../images/screenshots"):
            mkdir(directory + "/../images/screenshots")
        cmds.playblast(frame = 1, format = "image", cf = directory + "/../images/screenshots/" + new_file_name + ".gif", v = False, wh = (498, 270), p = 100, orn = False, os = True)
        cmds.playblast(frame = 1, format = "image", cf = directory + "/../images/screenshots/" + new_file_name + "_small.gif", v = False, wh = (249, 135), p = 100, orn = False, os = True)

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

    ## CREATE REFERENCE ##
    if "edits" in directory:
        if path.isfile(directory + "/../reference_" + file_name + ".ma"):
            remove(directory + "/../reference_" + file_name + ".ma")
        copyfile(directory + "/../" + new_file_name + ".ma", directory + "/../reference_" + file_name.split("_")[0] + ".ma")
    else:
        if path.isfile(directory + "/reference_" + file_name + ".ma"):
            remove(directory + "/reference_" + file_name + ".ma")
        copyfile(directory + "/" + new_file_name + ".ma", directory + "/reference_" + file_name.split("_")[0] + ".ma")