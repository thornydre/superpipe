bl_info = {
    "name": "Superpipe Save",
    "author": "Lucas BOUTROT",
    "version": (1, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Tools > Superpipe",
    "description": "Save scene for Superpipe",
    "warning": "",
    "wiki_url": "",
    "category": "Superpipe",
    }

import bpy
from os import path, remove, listdir, rename
from shutil import copyfile
 
## CREATE UI ##
class SuperpipePanel(bpy.types.Panel):
    bl_label = "Superpipe"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Superpipe"
    
    def draw(self, context):
        self.layout.operator("superpipe.save")
        self.layout.operator("superpipe.incremental_save")

class CommentPopup(bpy.types.Operator):
    bl_idname = "superpipe.comment_popup"
    bl_label = "Superpipe"

    comment = bpy.props.StringProperty(name="Comment")

    def execute(self, context):
        superpipe_incremental_save(self.comment)
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

## LINK THE BUTTONS TO THE COMMANDS
class button_superpipe_save(bpy.types.Operator):
    bl_idname = "superpipe.save"
    bl_label = "Save"
 
    def execute(self, context):
        superpipe_save()
        return{"FINISHED"}

class button_superpipe_incremental_save(bpy.types.Operator):
    bl_idname = "superpipe.incremental_save"
    bl_label = "Incremental Save"
 
    def execute(self, context):
        bpy.ops.superpipe.comment_popup("INVOKE_DEFAULT")
        return{"FINISHED"}

## COMMANDS ##
def superpipe_save():
    directory = bpy.path.abspath("//")
    file_name = path.splitext(bpy.path.basename(bpy.context.blend_data.filepath))[0]
    current_file = directory + file_name
    current_file_ext = current_file + ".blend"

    ## SAVE PROPERTIES VALUES ##
    ori_width = bpy.context.scene.render.resolution_x
    ori_height = bpy.context.scene.render.resolution_y
    temp_percentage = bpy.context.scene.render.resolution_percentage

    temp_type = bpy.context.scene.render.image_settings.file_format
    temp_path = bpy.data.scenes["Scene"].render.filepath

    ## CHANGES PROPERTIES VALUES ##
    new_width = 512.0
    new_height = 512.0

    if ori_width > ori_height:
        new_height = round(new_width / ori_width * ori_height)
    elif ori_height > ori_width:
        new_width = round(new_height / ori_height * ori_width)

    bpy.context.scene.render.resolution_x = new_width
    bpy.context.scene.render.resolution_y = new_height
    bpy.context.scene.render.resolution_percentage = 100

    bpy.context.scene.render.image_settings.file_format = "JPEG"
    if "edits" in directory:
        bpy.data.scenes["Scene"].render.filepath = directory + "../../images/screenshots/" + file_name + ".jpg"
    else:
        bpy.data.scenes["Scene"].render.filepath = directory + "../images/screenshots/" + file_name + ".jpg"
    
    ## RENDER ##
    bpy.ops.render.opengl(write_still = True)
    
    ## RESET PROPERTIES VALUES ##
    bpy.context.scene.render.resolution_x = ori_width
    bpy.context.scene.render.resolution_y = ori_height
    bpy.context.scene.render.resolution_percentage = temp_percentage
    
    bpy.data.scenes["Scene"].render.filepath = temp_path
    bpy.context.scene.render.image_settings.file_format = temp_type
    
    ## SAVE ##
    bpy.ops.wm.save_mainfile()
    
    ## CREATE REFERENCE ##
    if "edits" in directory:
        if path.isfile(directory + "../reference_" + file_name + ".blend"):
            remove(directory + "../reference_" + file_name + ".blend")
        copyfile(directory + file_name + ".blend", directory + "../reference_" + path.splitext(file_name)[0][:-4] + ".blend")
    else:
        if path.isfile(directory + "reference_" + file_name + ".blend"):
            remove(directory + "reference_" + file_name + ".blend")
        copyfile(directory + file_name + ".blend", directory + "reference_" + path.splitext(file_name)[0][:-4] + ".blend")

def superpipe_incremental_save(comment):
    directory = bpy.path.abspath("//")
    file_name = path.splitext(bpy.path.basename(bpy.context.blend_data.filepath))[0]
    current_file = directory + file_name
    current_file_ext = current_file + ".blend"
    
    ## SAVE PROPERTIES VALUES ##
    ori_width = bpy.context.scene.render.resolution_x
    ori_height = bpy.context.scene.render.resolution_y
    temp_percentage = bpy.context.scene.render.resolution_percentage

    temp_type = bpy.context.scene.render.image_settings.file_format
    temp_path = bpy.data.scenes["Scene"].render.filepath

    ## CREATE NEW VERSON NUMBER ##
    version = int(file_name[-2:]) + 1
    
    if "edits" in directory:
        for f in listdir(directory + ".."):
            if file_name[:-2] in f:
                current_file_ext = f
                current_file = path.splitext(current_file_ext)[0]
                version = int(current_file[-2:]) + 1

    if version < 10:
        new_file_name = file_name[:-2] + "0" + str(version)
    else:
        new_file_name = file_name[:-2] + str(version)
    
    ## COMMENT ##
    if "edits" in directory:
        versions_file = directory + "../../superpipe/versions_data.spi"
    else:
        versions_file = directory + "../superpipe/versions_data.spi"

    with open(versions_file, "r") as f:
        all_comments = f.read()
    f.close()

    comments_list = all_comments.split("\n---\n")
    i = 0
    comments_dict = {}
    for version_name in comments_list[:-1:2]:
        print(version_name)
        print(comments_list[i + 1])
        comments_dict[version_name] = comments_list[i + 1]
        i += 2

    comments_dict[new_file_name + ".ma"] = comment

    print(comments_dict)

    final_comment = ""
    for version_name, version_comment in comments_dict.items():
        final_comment += version_name + "\n---\n" + version_comment + "\n---\n"

    with open(versions_file, "w") as f:
        f.write(final_comment)
    f.close()
        
    ## CHANGES PROPERTIES VALUES ##
    new_width = 512.0
    new_height = 512.0

    if ori_width > ori_height:
        new_height = round(new_width / ori_width * ori_height)
    elif ori_height > ori_width:
        new_width = round(new_height / ori_height * ori_width)

    bpy.context.scene.render.resolution_x = new_width
    bpy.context.scene.render.resolution_y = new_height
    bpy.context.scene.render.resolution_percentage = 100
    
    bpy.context.scene.render.image_settings.file_format = "JPEG"
    if "edits" in directory:
        bpy.data.scenes["Scene"].render.filepath = directory + "../../images/screenshots/" + new_file_name + ".jpg"
    else:
        bpy.data.scenes["Scene"].render.filepath = directory + "../images/screenshots/" + new_file_name + ".jpg"
    
    ## RENDER ##
    bpy.ops.render.opengl(write_still = True)
    
    ## RESET PROPERTIES VALUES ##
    bpy.context.scene.render.resolution_x = ori_width
    bpy.context.scene.render.resolution_y = ori_height
    bpy.context.scene.render.resolution_percentage = temp_percentage
    
    bpy.data.scenes["Scene"].render.filepath = temp_path
    bpy.context.scene.render.image_settings.file_format = temp_type
    
    ## SAVE ##
    if "edits" in directory:
        copyfile(directory + "../" + current_file_ext, directory + current_file_ext)
        bpy.ops.wm.save_as_mainfile(filepath = directory + "../" + new_file_name + ".blend")
        remove(directory + "../" + current_file_ext)
    else:
        print(directory + "edits/" + file_name + ".blend")
        copyfile(current_file_ext, directory + "edits/" + file_name + ".blend")
        bpy.ops.wm.save_as_mainfile(filepath = directory + new_file_name + ".blend")
        remove(current_file_ext)
    
    ## CREATE REFERENCE ##
    if "edits" in directory:
        if path.isfile(directory + "../reference_" + file_name + ".blend"):
            remove(directory + "../reference_" + file_name + ".blend")
        copyfile(directory + "../" + new_file_name + ".blend", directory + "../reference_" + path.splitext(file_name)[0][:-4] + ".blend")
    else:
        if path.isfile(directory + "reference_" + file_name + ".blend"):
            remove(directory + "reference_" + file_name + ".blend")
        copyfile(directory + new_file_name + ".blend", directory + "reference_" + path.splitext(file_name)[0][:-4] + ".blend")

## REGISRTATION ##
def register():
    bpy.utils.register_class(SuperpipePanel)
    bpy.utils.register_class(CommentPopup)
    bpy.utils.register_class(button_superpipe_save)
    bpy.utils.register_class(button_superpipe_incremental_save)

## UNREGISRTATION ##
def unregister():
    bpy.utils.unregister_class(SuperpipePanel)
    bpy.utils.unregister_class(CommentPopup)
    bpy.utils.unregister_class(button_superpipe_save)
    bpy.utils.unregister_class(button_superpipe_incremental_save)


if __name__ == "__main__":
    register()
