import bpy
import addon_utils
from pathlib import Path


class SWTOR_PT_files_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SWTOR Character Tools"
    bl_label = "SWTOR Character Assembler"

    def draw(self, context):

        # Checks:
        
        # Extracted SWTOR assets' "resources" folder. 
        swtor_resources_folderpath = bpy.context.preferences.addons[__package__].preferences.swtor_resources_folderpath
        resources_folder_exists = ( Path(swtor_resources_folderpath) / "art/shaders/materials").exists()
        
        # .gr2 Importer Addon
        modern_gr2_addon_is_enabled = addon_utils.check("io_scene_gr2")[1]
        legacy_gr2_addon_is_enabled = addon_utils.check("io_scene_gr2_legacy")[1]






        # Checks and Status display
        
        layout = self.layout

        # Show whether the 'resources' folder is set correctly in Preferences.
        swtor_addon_status = layout.column(align=True)
        swtor_addon_status.scale_y = 0.75
        
        swtor_addon_status.alert = False  # Reset alert
        if resources_folder_exists:
            swtor_addon_status.label(text="• 'resources' Folder: SET")
        else:
            swtor_addon_status.alert = True
            swtor_addon_status.label(text="• 'resources' Folder: NOT SET")


        swtor_addon_status.alert = False  # Reset alert
        if modern_gr2_addon_is_enabled is True:
            swtor_addon_status.label(text="• Modern .gr2 Addon: SET")
        else:
            swtor_addon_status.alert = True
            swtor_addon_status.label(text="• Modern .gr2 Addon: NOT SET")


        swtor_addon_status.alert = False  # Reset alert
        if resources_folder_exists is False or modern_gr2_addon_is_enabled is False:
            swtor_addon_status.label(text=" ")
            swtor_addon_status.label(text="Check the Character Assembler's")
            swtor_addon_status.label(text="requirements in its Tooltips.")






        # CHECKS:
        # Extracted SWTOR assets' "resources" folder. 
        swtor_resources_folderpath = bpy.context.preferences.addons[__package__].preferences.swtor_resources_folderpath
        resources_folder_exists = ( Path(swtor_resources_folderpath) / "art/shaders/materials").exists()
        # .gr2 Importer Addon
        modern_gr2_addon_is_enabled = addon_utils.check("io_scene_gr2")[1]


        # character_assembler UI
        tool_section = layout.box().column(align=True)
        tool_section.scale_y = 1.0
        tool_section.enabled = resources_folder_exists
        tool_section.alert = tool_section.enabled is False
        
        tool_section.label(text="Character Assembler")
        tool_section.operator("swtor.character_assembler", text="Select 'paths.json' File")
        # tool_section.prop(context.scene, "swca_prefix_str", text="Prefix")

        tool_section_props = tool_section.column(align=True)
        tool_section_props.scale_y = 0.75
        tool_section_props.prop(context.scene, "swca_gather_only_bool", text="Gather Assets only")
        tool_section_props.prop(context.scene, "swca_dont_overwrite_bool", text="Don't Overwrite Assets")
        tool_section_props.prop(context.scene, "swca_collect_bool", text="Collect By In-Game Names")
        tool_section_props.prop(context.scene, "swca_import_armor_only", text="Import Armor Gear Only")
        tool_section_props.prop(context.scene, "swca_import_skeleton_bool", text="Import Rigging Skeleton")
        tool_section_props.prop(context.scene, "swca_bind_to_skeleton_bool", text="Bind Objects To Skeleton",)
        



class SWTOR_PT_renaming_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SWTOR Character Tools"
    bl_label = "Renaming Tools"

    def draw(self, context):

        layout = self.layout        
        tool_section = layout.box()
        
        col_info=tool_section.column(align=False)
        col_info.scale_y = 0.7
        col_info.label(text="STRONGLY RECOMMENDED:")
        col_info.label(text="after importing a character,")
        col_info.label(text="change the Objects, Materials,")
        col_info.label(text="and Skeleton's names to avoid")
        col_info.label(text="problems with further imports.")

        col=tool_section.column(align=False)
        col.scale_y = 1
        col.operator("swtor.prefixer", text="Prefix Selected Items' Names")
        col.prop(context.scene, "prefix", text = "Prefix")
        col.prop(context.scene, "prefix_mats_skeletons_bool", text="Prefix their Mats./Skels. too")





class SWTOR_PT_baking_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SWTOR Character Tools"
    bl_label = "Baking Tools"

    def draw(self, context):

        # LEGACY MATERIALS SECTION

        layout = self.layout        
        tool_section = layout.box()

        col_info=tool_section.column(align=False)
        col_info.scale_y = 0.7
        col_info.label(text="In order to bake the character's")
        col_info.label(text="texturemaps, a conversion to")
        col_info.label(text="an older, \"Legacy\" PBR-friendly")
        col_info.label(text="version of our SWTOR Materials")
        col_info.label(text="is recommended.")


        tool_section = tool_section.column(align=True)
        tool_section.operator("swtor.convert_to_legacy_materials", text="Convert All Materials")
        tool_section.prop(context.scene, "add_baking_targets_bool", text="Add Baking Texture Nodes")


        # tool_section = layout.box()
        # tool_section.operator("swtor.baking_tools", text="Add Targets")
        # diffuse = tool_section.operator("swtor.baking_tools", text="Add Targets")









# Registrations

classes = [
    SWTOR_PT_files_tools,
    SWTOR_PT_renaming_tools,
    SWTOR_PT_baking_tools,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    
if __name__ == "__main__":
    register()