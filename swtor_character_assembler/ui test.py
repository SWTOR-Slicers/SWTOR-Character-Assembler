import bpy
import addon_utils
from pathlib import Path


# Addon Status sub-panel
class SWTOR_PT_status(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SWTOR Character Tools"
    bl_label = "Tool Status"

    def draw(self, context):

        # Checks:
        
        # Extracted SWTOR assets' "resources" folder. 
        swtor_resources_folderpath = bpy.context.preferences.addons[__package__].preferences.swtor_resources_folderpath
        resources_folder_exists = ( Path(swtor_resources_folderpath) / "art/shaders/materials").exists()
        
        # .gr2 Importer Addon
        gr2_addon_exists = addon_utils.check("io_scene_gr2")[1]
        legacy_gr2_addon_exists = addon_utils.check("io_scene_gr2_legacy")[1]
        

        layout = self.layout
        layout.scale_y = 0.65

        # Show whether the 'resources' folder is set correctly in Preferences.
        zgswtor_addon_status = layout.column(align=True)
        
        zgswtor_addon_status.alert = False
        if gr2_addon_exists == True:
            zgswtor_addon_status.label(text="• .gr2 Add-on: SET")
        else:
            if legacy_gr2_addon_exists == True:
                zgswtor_addon_status.label(text="• .gr2 Add-on: LEGACY VERSION")
            else:
                zgswtor_addon_status.alert = True
                zgswtor_addon_status.label(text="• .gr2 Add-on: NOT SET")


        zgswtor_addon_status.alert = False
        if resources_folder_exists == True:
            zgswtor_addon_status.label(text="• 'resources' Folder: SET")
        else:
            zgswtor_addon_status.alert = True
            zgswtor_addon_status.label(text="• 'resources' Folder: NOT SET")


# Character Tools sub-panel
class SWTOR_PT_character_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SWTOR Character Tools"
    bl_label = "Character Tools"

    def draw(self, context):

        # CHECKS:
        
        # Extracted SWTOR assets' "resources" folder. 
        swtor_resources_folderpath = bpy.context.preferences.addons[__package__].preferences.swtor_resources_folderpath
        resources_folder_exists = ( Path(swtor_resources_folderpath) / "art/shaders/materials").exists()
        
        # .gr2 Importer Addon
        gr2_addon_exists = addon_utils.check("io_scene_gr2")[1]
        

        gral_y_scaling_factor = 0.9
        info_y_scaling_factor = 0.75

        layout = self.layout
        layout.scale_y = gral_y_scaling_factor


        # character_assembler UI
        tool_section = layout.box().column(align=True)
        
        tool_section.label(text="Character Assembler")

        if not resources_folder_exists:
        # tool_section.enabled = resources_folder_exists
            tool_section_info = tool_section.column(align=True)
            tool_section_info.scale_y = info_y_scaling_factor
            tool_section_info.alert = True
            tool_section_info.label(text="Without setting a resources")
            tool_section_info.label(text="folder, success will depend")
            tool_section_info.label(text="on the PC/NPC folder already")
            tool_section_info.label(text="having the required assets.")
            tool_section_info.label(text="")
            tool_section_info.alert = False

        tool_section.scale_y = 1.0
        tool_section.operator("swtor.character_assembler", text="Select 'paths.json' File")
        
        # Options whose availability depends on a 'resources' folder in Preferences
        tool_section_dimmables = tool_section.column(align=True)
        tool_section_dimmables.enabled = resources_folder_exists
        tool_section_dimmables.prop(context.scene, "swca_gather_only_bool", text="Gather Assets only")
        tool_section_dimmables.prop(context.scene, "swca_dont_overwrite_bool", text="Don't Overwrite Assets")
        tool_section = tool_section.column(align=True)
        tool_section.prop(context.scene, "swca_collect_bool", text="Collect By In-Game Names")
        tool_section.prop(context.scene, "swca_import_armor_only", text="Import Armor Gear Only")
        tool_section.prop(context.scene, "swca_import_skeleton_bool", text="Import Rigging Skeleton")
        tool_section.prop(context.scene, "swca_bind_to_skeleton_bool", text="Bind Objects To Skeleton",)
        
        tool_section_info = tool_section.column(align=True)
        tool_section_info.scale_y = info_y_scaling_factor
        tool_section_info.label(text="")
        tool_section_info.label(text="It is advisable to change the")
        tool_section_info.label(text="character's Objects, Materials")
        tool_section_info.label(text="and Skeleton names to avoid")
        tool_section_info.label(text="conflicts with further imports")
        tool_section_info.label(text="(see Prefix tool in the")
        tool_section_info.label(text="Misc. Tools section).")
        



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
    bl_options = {'DEFAULT_CLOSED'}

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


        tool_section = layout.box()
        tool_section.operator("swtor.baking_tools", text="Add Targets")









# Registrations

classes = [
    SWTOR_PT_status,
    SWTOR_PT_character_tools,
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