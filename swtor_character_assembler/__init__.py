import sys
import importlib

# Add-on Metadata

bl_info = {
    "name": "SWTOR Character Assembler",
    "author": "ZeroGravitas",
    "version": (1, 0, 0),
    "blender": (3, 1, 0),
    "category": "SWTOR",
    "location": "View 3D > Sidebar > SWTOR Tools",
    "description": "Processes SWTOR characters and NPCs' folders exported from TORCommunity.com,\ngathering their files from a game asset extraction and assembling them",
    "doc_url": "https://github.com/SWTOR-Slicers/swtor-character-locator",
    "tracker_url": "",
}

# Add-on modules loader:
# Simplifies coding the loading of the modules to keeping a list of their names
# (See https://b3d.interplanety.org/en/creating-multifile-add-on-for-blender/ )

modulesNames = [
    'preferences',
    'swtor_character_assembler',
    ]
  
modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))

for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)


def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()

def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()
 
if __name__ == "__main__":
    register()#