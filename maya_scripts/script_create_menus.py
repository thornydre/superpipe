import maya.cmds as cmds

cmds.menu(l = "SuperPipe", p = "MayaWindow")
cmds.menuItem(l = "Increment and Save", c = "test")
cmds.menuItem(l = "Save", c = "test")