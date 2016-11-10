import maya.cmds as cmds
from os import path, listdir, mkdir, remove
from shutil import copyfile

current_file_ext = cmds.file(query = True, expandName = True)
current_file = current_file_ext.strip(".ma")
directory = path.dirname(current_file_ext)
file_name = path.basename(current_file)

## SCREENSHOT ##
frm = cmds.getAttr("defaultRenderGlobals.imageFormat")
cmds.setAttr("defaultRenderGlobals.imageFormat", 0)
if "edits" in directory:
    if not path.isdir(directory + "/../../images/screenshots"):
        mkdir(directory + "/../../images/screenshots")
    cmds.playblast(frame = 1, format = "image", cf = directory + "/../../images/screenshots/" + file_name + ".gif", v = False, wh = (498, 270), p = 100, orn = False, os = True)
    cmds.playblast(frame = 1, format = "image", cf = directory + "/../../images/screenshots/" + file_name + "small.gif", v = False, wh = (249, 135), p = 100, orn = False, os = True)
else:
    if not path.isdir(directory + "/../images/screenshots"):
        mkdir(directory + "/../images/screenshots")
    cmds.playblast(frame = 1, format = "image", cf = directory + "/../images/screenshots/" + file_name + ".gif", v = False, wh = (498, 270), p = 100, orn = False, os = True)
    cmds.playblast(frame = 1, format = "image", cf = directory + "/../images/screenshots/" + file_name + "_small.gif", v = False, wh = (249, 135), p = 100, orn = False, os = True)

cmds.setAttr("defaultRenderGlobals.imageFormat", frm)

## SAVE ##
cmds.file(rename = current_file_ext)
cmds.file(save = True, type = "mayaAscii")

## CREATE REFERENCE ##
if "edits" in directory:
	if path.isfile(directory + "/../reference_" + file_name + ".ma"):
		remove(directory + "/../reference_" + file_name + ".ma")
	copyfile(directory + "/" + file_name + ".ma", directory + "/../reference_" + file_name.split("_")[0] + ".ma")
else:
	if path.isfile(directory + "/reference_" + file_name + ".ma"):
		remove(directory + "/reference_" + file_name + ".ma")
	copyfile(directory + "/" + file_name + ".ma", directory + "/reference_" + file_name.split("_")[0] + ".ma")