import sys
import importlib

# Add-on Metadata

bl_info = {
    "name": "SWTOR Character Assembler",
    "author": "ZeroGravitas",
    "version": (3, 0, 0),
    "blender": (3, 1, 0),
    "category": "SWTOR",
    "location": "View 3D > Sidebar > ZG SWTOR",
    "description": "SWTOR Character Importer and Assembler",
    "doc_url": "https://github.com/SWTOR-Slicers/swtor_character_assembler",
    "tracker_url": "",
}

# Add-on modules loader:
# Simplifies coding the loading of the modules to keeping a list of their names
# (See https://b3d.interplanety.org/en/creating-multifile-add-on-for-blender/ )

modulesNames = [
    'ui',
    'preferences',
    'deduplicate_materials',
    'deduplicate_nodegroups',
    'character_assembler',
    'prefixer',
    'convert_to_legacy_materials'
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