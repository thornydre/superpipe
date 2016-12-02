import maya.cmds as cmds
from os import path, mkdir

current_file_ext = cmds.file(query = True, expandName = True)
current_file = current_file_ext.strip(".ma")
directory = path.dirname(current_file_ext)
file_name = path.basename(current_file)

end_frame = cmds.playbackOptions(q = True, animationEndTime = True)

## EXPORT ##
if "edits" in directory:
    if not path.isdir(directory + "/../../cache/alembic"):
        mkdir(directory + "/../../cache/alembic")
    cmds.AbcExport(j = "-frameRange 800 " + str(end_frame) + " -dataFormat ogawa -file " + directory + "/../../cache/alembic/" + file_name + ".abc")
else:
    if not path.isdir(directory + "/../cache/alembic"):
        mkdir(directory + "/../cache/alembic")
    cmds.AbcExport(j = "-frameRange 800 " + str(end_frame) + " -dataFormat ogawa -file " + directory + "/../cache/alembic/" + file_name + ".abc")
