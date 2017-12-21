You can add the shelf to maya by adding the file "scripts/maya_scripts/shelf_Superpipe.mel" to your "MyDocuments/maya/20**/prefs/shelves/"" folder. That will add some preview of your shots in Superpipe.

You can add the Superpipe add-on for Blender by going into "File > User Preferences > Add-ons" and click on "Install Add-on from file" and pick "scripts/blender_scripts/superpipe_addon.py".

It works only with Maya (shots and assets) and Houdini (assets) at the moment. It might be unstable using Blender.

The ".ma" files in the "src" folder can be modified if you want a different default files as you create a new asset or shot in Superpipe.

Known issues:
  - Mind when moving a shot, a shot s00p00 stays in the shot folder, don't delete it is the shot you wanted to move !
