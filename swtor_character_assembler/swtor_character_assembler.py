import bpy
from bpy.props import StringProperty, BoolProperty
from bpy.types import Operator

import os
from pathlib import Path
import shutil

import json
import xml.etree.ElementTree as ET



# Aux Functions

def get_wrinkles_and_directionmaps(mat_file_abs_path):
    '''Reads a shader .mat file and returns any DirectionMap
    and WrinkleMap paths in an "as is" basis
    (slashes, backslashes, initial ones or not…)'''
    
    relative_paths = []
    with open(mat_file_abs_path, 'r') as mat_file:
        tree = ET.parse(mat_file)
        root = tree.getroot()

        # The diverse camelCases are as per BioWare's horrific inconsistency.
        # Same goes for initial backslash. For consistency, we add it if missing.
        # backslash vs. slash is solved vía pathlib later on.

        DirectionMap = root.find("./input/[semantic='DirectionMap']")
        if DirectionMap != None:
            texturemap_path = DirectionMap.find("value").text + ".dds"
            if texturemap_path[0] != "\\":
                texturemap_path = "\\" + texturemap_path
            relative_paths.append(texturemap_path)

        animatedWrinkleMap = root.find("./input/[semantic='animatedWrinkleMap']")
        if animatedWrinkleMap != None:
            texturemap_path = animatedWrinkleMap.find("value").text + ".dds"
            if texturemap_path[0] != "\\":
                texturemap_path = "\\" + texturemap_path
            relative_paths.append(texturemap_path)

        animatedWrinkleMask = root.find("./input/[semantic='animatedWrinkleMask']")
        if animatedWrinkleMask != None:
            texturemap_path = animatedWrinkleMask.find("value").text + ".dds"
            if texturemap_path[0] != "\\":
                texturemap_path = "\\" + texturemap_path
            relative_paths.append(texturemap_path)

    return(relative_paths)

def black_dds(swtor_resources_folderpath):
    addon_directory = os.path.dirname(__file__)

    black_dds_origin = Path(addon_directory) / "black.dds"
    black_dds_destination = Path(swtor_resources_folderpath) / "art/defaultassets/black.dds"
    
    if black_dds_destination.exists() == False:
        print ("'black.dds' file missing in 'resources\\art\\defaultassets'. Placing a copy of the file \(included in this Addon\) there.")
        print()
        print()
        try:
            shutil.copy2( str(black_dds_origin), str(black_dds_destination) )
        except Exception as e:
            print("ERROR: Copying the 'black.dds' file to the resources folder failed:")
            print(e)
            print()

    return




# Class

class SWTOR_OT_character_assembler(Operator):
    bl_label = "SWTOR Character Locator"
    bl_idname = "swtor.character_assembler"
    bl_description = "Processes the 'path.json' file in a Player Character/NPC folder\nexported by TORCommunity.com, filling its subfolders with all\nrelated objects and textures, then importing the Character\n\n• Requires setting the path to a 'resources' folder in this addon's Preferences"
    filepath: StringProperty(subtype='FILE_PATH')


    # Some properties
    
    gather_only_bool: bpy.props.BoolProperty(
        name="Gather Assets Only",
        description="Don't Import The Character, and just copy the required assets\nto the Character's folder",
        default = False,
        options={'HIDDEN'}
    )

    dont_overwrite_bool: bpy.props.BoolProperty(
        name="Don't overwrite Existing assets",
        description="If the character's folder contains some assets already, don't overwrite those.\nThat will preserve any changes done to them, such as manual retouchings",
        default = True,
        options={'HIDDEN'}
    )



    def execute(self, context):
        # Terminal's VT100 escape codes (most terminals understand them).
        # See: http://www.climagic.org/mirrors/VT100_Escape_Codes.html
        # (replacing ^[ in terminal codes with \033)
        CLEAR_TERMINAL = '\033[2J'      # Clear entire screen.
        CURSOR_HOME = '\033[H'          # Move cursor to upper left corner.
        CLEAR_EOL = '\r\033[K'          # Erase to end of current line.
        LINE_BACK_1ST_COL = '\033[F'    # Move cursor one line up, 1st column.


        # Sync properties with their UI matches
        self.gather_only_bool = context.scene.gather_only_bool
        self.dont_overwrite_bool = context.scene.dont_overwrite_bool


        # Get the extracted SWTOR assets' "resources" folder from the add-on's preferences. 
        swtor_resources_folderpath = bpy.context.preferences.addons[__package__].preferences.swtor_resources_folderpath
        swtor_shaders_path = swtor_resources_folderpath + "/art/shaders/materials"
        # Test the existence of the shaders subfolder to validate the SWTOR "resources" folder
        if Path(swtor_shaders_path).exists() == False:
            self.report({"WARNING"}, "Please check this add-on's preferences' path to the extracted assets 'resources' folder.")
            return {"CANCELLED"}


        print(CLEAR_TERMINAL + CURSOR_HOME)
        print("=================================")
        print("CHARACTER FOLDER'S ASSETS LOCATOR")
        print("=================================")
        print()
        print()

        # Check for the existence of a "black.dds" file in resources/art/defaultassets and add one if missing
        black_dds(swtor_resources_folderpath)


        if self.filepath.endswith("paths.json") == False:
            self.report({"WARNING"}, "The selected file isn't a 'path.json' file. Please select a correct one.")
            return {"CANCELLED"}
        
        # list of origins and destinations for copying. Each element is:
        # [slotName, type of asset, origin, destination, some report text if needed]
        
        files_to_copy = []
        
        with open(self.filepath, 'r') as file:
            json_data = json.load(file)
            
            # Fill list of files to copy to character folder
            
            character_models_folderpath = str( Path(self.filepath).parent / "models" )
            character_materials_folderpath = str( Path(self.filepath).parent / "materials" )
            character_skeleton_folderpath = str( Path(self.filepath).parent / "skeleton" )

            
            for element in json_data:
                slotName = element["slotName"]
                
                
                if slotName != "skinMats":
                    
                    # NOT SKIN MATERIALS
                    
                    if "models" in element:
                        models =  element["models"]
                        if models:
                            for model in models:
                                origin = str( Path(swtor_resources_folderpath) / Path(model[1:]) )
                                destination = str( Path(character_models_folderpath) / slotName / Path(model).name )
                                files_to_copy.append([slotName, "model", origin, destination, ""])
                            
                    if "materialInfo" in element:
                        materialInfo = element["materialInfo"]
                        
                        if "matPath" in materialInfo:
                            origin = str( Path(swtor_resources_folderpath) / Path(materialInfo["matPath"][1:]) )
                            destination = str( Path(character_materials_folderpath) / slotName / Path(materialInfo["matPath"]).name )
                            files_to_copy.append([slotName, "material definition", origin, destination, ""])
                            
                            additional_texturemaps = get_wrinkles_and_directionmaps(origin)
                            if additional_texturemaps:
                                for additional_texturemap in additional_texturemaps:
                                    origin = str( Path(swtor_resources_folderpath) / Path(additional_texturemap[1:]) )
                                    destination = str( Path(character_materials_folderpath) / slotName / Path(additional_texturemap).name )
                                    files_to_copy.append([slotName, "material definition", origin, destination, ""])

                        if "ddsPaths" in materialInfo:
                            ddsPaths = materialInfo["ddsPaths"]
                            if ddsPaths:
                                for ddsPath in ddsPaths:
                                    if ddsPaths[ddsPath].endswith(".dds"):
                                        origin = str( Path(swtor_resources_folderpath) / Path(ddsPaths[ddsPath][1:]) )
                                        destination = str( Path(character_materials_folderpath) / slotName / Path(ddsPaths[ddsPath]).name )
                                        files_to_copy.append([slotName, "texture map", origin, destination, ""])

                        if "eyeMatInfo" in materialInfo:
                            if "ddsPaths" in materialInfo["eyeMatInfo"]:
                                ddsPaths = materialInfo["eyeMatInfo"]["ddsPaths"]
                                if ddsPaths:
                                    for ddsPath in ddsPaths:
                                        if ddsPaths[ddsPath].endswith(".dds"):
                                            origin = str( Path(swtor_resources_folderpath) / Path(ddsPaths[ddsPath][1:]) )
                                            destination = str( Path(character_materials_folderpath) / "eye" / Path(ddsPaths[ddsPath]).name )
                                            files_to_copy.append(["eye", "texture map", origin, destination, ""])


                else:

                    # SKIN MATERIALS (the dict hierarchy gets deeper and more confusing)
                    
                    if "materialInfo" in element:
                        if "mats" in element["materialInfo"]:
                            mats = element["materialInfo"]["mats"]
                            for mat in mats:
                                mat_slotName = mat["slotName"]
                                
                                if "materialInfo" in mat:
                                    mat_materialInfo = mat["materialInfo"]

                                    if "matPath" in mat_materialInfo:
                                        origin = str( Path(swtor_resources_folderpath) / Path(mat_materialInfo["matPath"][1:]) )
                                        destination = str( Path(character_materials_folderpath) / slotName / mat_slotName / Path(mat_materialInfo["matPath"]).name )
                                        files_to_copy.append([slotName + ": " + mat_slotName, "material definition", origin, destination, ""])
                            
                                        additional_texturemaps = get_wrinkles_and_directionmaps(origin)
                                        if additional_texturemaps:
                                            for additional_texturemap in additional_texturemaps:
                                                origin = str( Path(swtor_resources_folderpath) / Path(additional_texturemap[1:]) )
                                                destination = str( Path(character_materials_folderpath) / slotName / Path(additional_texturemap).name )
                                                files_to_copy.append([slotName, "material definition", origin, destination, ""])

                                if "ddsPaths" in mat:
                                    mat_ddsPaths = mat["ddsPaths"]
                                    if mat_ddsPaths:
                                        for ddsPath in mat_ddsPaths:
                                            if mat_ddsPaths[ddsPath].endswith(".dds"):
                                                origin = str( Path(swtor_resources_folderpath) / Path(mat_ddsPaths[ddsPath][1:]) )
                                                destination = str( Path(character_materials_folderpath) / slotName / mat_slotName / Path(mat_ddsPaths[ddsPath]).name )
                                                files_to_copy.append([slotName + ": " + mat_slotName, "texture map", origin, destination, ""])


            # If there is a companion "skeleton.json" file, process it too.
            skeleton_filepath = Path(self.filepath).parent / "skeleton.json"
            with open(skeleton_filepath, 'r') as skeleton_file:
                json_data = json.load(skeleton_file)
                if "path" in json_data:
                    skeleton_model = json_data["path"]
                    if skeleton_model:
                        origin = str( Path(swtor_resources_folderpath) / Path(skeleton_model[1:]) )
                        destination = str( Path(character_skeleton_folderpath) / Path(skeleton_model).name )
                        files_to_copy.append(["Skeleton", "model", origin, destination, ""])


            # Process list of files to copy to character folder
            
            errors_report = []
            
            if files_to_copy:
                for element in files_to_copy:
                    body_part = element[0]
                    asset_type = element[1]
                    origin = element[2]
                    destination = element[3]
                    report = element[4]
                    
                    print(body_part, "-", asset_type, "\n",origin, "\n",destination)

                    # If any of the destination folders doesn't exist, create it
                    # ('eye', typically, plus any new one such as 'skeleton')
                    if Path(destination).parent.exists() == False:
                        try:
                            Path(destination).parent.mkdir(parents=False, exist_ok=True)
                            print("Creating " + str(Path(destination).parent) + "folder.\n")
                        except Exception as e:
                            print("ERROR!!!--------: The folder ",destination," didn't exist and when trying to create it an error occurred:\n",e,"\n")
                    
                    if Path(destination).exists() == True and self.dont_overwrite_bool == True:
                        print("FILE ALREADY EXISTS IN DESTINATION. PRESERVED")
                    else:
                        # File copy as such:
                        try:
                            shutil.copy2(origin, destination)
                            print("COPIED")
                        except Exception as e:
                            print("ERROR!!!-------- ", str(e))
                            print()
                            errors_report.append(body_part + " - " + asset_type + " - " + str(origin))
                    
                    print()
                        
        print("ASSETS GATHERING DONE!")
        print()
        if errors_report:
            print("Some files failed to be copied:\n")
            for error_report in errors_report:
                print("     " + error_report)
            print("\nPlease check the console for their related error messages, and their entries in the 'paths.json' and/or related .mat files.")
            
            self.report({'INFO'}, "Character's Assets copied to its folder. SOME FILES FAILED TO BE COPIED! Check the console's output." )
        else:
            self.report({'INFO'}, "Character's Assets copied to its folder" )
            
        
        # Calling Darth Atroxa's Character Importer in his .gr2 Importer Addon.
        if self.gather_only_bool == False:
            print("IMPORTING CHARACTER")
            print("Importing and assembling the character assets")
            print()
            bpy.ops.import_mesh.gr2_json(filepath = str( self.filepath ))
            print()
            print("DONE!")
            
        return {'FINISHED'}


    # File Browser for selecting paths.json file
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}









# 3D VIEWPORT PANEL ---------------------------------------------

# Files Tools sub-panel
class SWTOR_PT_character_assembler(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SWTOR Tools"
    bl_label = "SWTOR Character Assembler"

    def draw(self, context):

        # Check that there is a "resources" folder set in Preferences
        swtor_resources_folderpath = bpy.context.preferences.addons[__package__].preferences.swtor_resources_folderpath
        resources_folder_exists = ( Path(swtor_resources_folderpath) / "art/shaders/materials").exists()


        layout = self.layout

        # Show a warning if the 'resources' folder isn't set in the addon's prefs.
        addon_advice = layout.column(align=True)
        addon_advice.scale_y = 0.7        
        if resources_folder_exists != True:
            addon_advice.label(text="Please select a 'resources' folder")
            addon_advice.label(text="in this add-on's Preferences")
        else:
            addon_advice.label(text="Opening the Console window is")
            addon_advice.label(text="recommended for error-checking")


        # locate_characters_assets UI
        tool_section = layout.box().column(align=True)
        tool_section.enabled = resources_folder_exists
        tool_section.operator("swtor.character_assembler", text="Select 'paths.json' File")
        tool_section.prop(context.scene, "gather_only_bool", text="Gather Assets only.")
        tool_section.prop(context.scene, "dont_overwrite_bool", text="Don't Overwrite Assets.")





# REGISTRATIONS ---------------------------------------------

classes = [
    SWTOR_OT_character_assembler,
    SWTOR_PT_character_assembler,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.gather_only_bool = bpy.props.BoolProperty(
        name="Gather Assets Only",
        description="Don't import the character, just copy the required assets\nto the Character's folder",
        default = False,
    )
    bpy.types.Scene.dont_overwrite_bool = bpy.props.BoolProperty(
        name="Don't overwrite Existing assets",
        description="If the character's folder contains some assets already, don't overwrite those.\nThat will preserve any changes done to them, such as manual retouchings",
        default = True,
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls) 
        
    del bpy.types.Scene.gather_only_bool
    del bpy.types.Scene.dont_overwrite_bool

if __name__ == "__main__":
    register()