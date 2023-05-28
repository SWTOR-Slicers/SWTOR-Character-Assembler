import bpy
import os
from pathlib import Path

class SWCL_addonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    # Preferences properties --------------------

    # resources folderpath
    swtor_resources_folderpath: bpy.props.StringProperty(
        name = "SWTOR Resources",
        description = 'Path to the "resources" folder produced by a SWTOR assets extraction',
        subtype = "DIR_PATH",
        default = "Choose or type the folder's path",
        maxlen = 1024
    )


    # UI ----------------------------------------
    
    def draw(self, context):
        layout = self.layout

        # resources folderpath preferences UI
        pref_box = layout.box()
        col=pref_box.column()
        col.scale_y = 0.7
        col.label(text="Path to the 'resources' folder in a SWTOR assets extraction")
        col.label(text="produced by the Slicers GUI app, EasyMYP, or any similar tool.")
        pref_box.prop(self, 'swtor_resources_folderpath', expand=True)



# Registrations

def register():
    bpy.utils.register_class(SWCL_addonPreferences)

def unregister():
    bpy.utils.unregister_class(SWCL_addonPreferences)

if __name__ == "__main__":
    register()