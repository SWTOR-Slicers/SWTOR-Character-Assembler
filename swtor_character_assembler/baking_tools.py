import bpy
import os
from pathlib import Path


def merge_material_nodes(source_material_name, destination_material_name):
    # Get the source and destination materials
    source_material = bpy.data.materials.get(source_material_name)
    destination_material = bpy.data.materials.get(destination_material_name)

    # Check if both materials exist
    if not source_material or not destination_material:
        print("Error: One or both materials do not exist.")
        return

    # Get the node trees of the materials
    source_node_tree = source_material.node_tree
    destination_node_tree = destination_material.node_tree

    # Create a mapping between source and destination nodes
    node_mapping = {}

    # Add nodes to the destination node tree
    for source_node in source_node_tree.nodes:
        new_node = destination_node_tree.nodes.new(type=source_node.bl_idname)
        new_node.name = source_node.name
        new_node.label = source_node.label
        new_node.location = source_node.location
        new_node.hide = source_node.hide
        new_node.use_custom_color = source_node.use_custom_color
        new_node.color = source_node.color


        # Add the mapping between source and destination nodes
        node_mapping[source_node] = new_node

    # Add links to the destination node tree
    for source_link in source_node_tree.links:
        source_socket = node_mapping.get(source_link.from_node).outputs[source_link.from_socket.name]
        destination_socket = node_mapping.get(source_link.to_node).inputs[source_link.to_socket.name]
        destination_node_tree.links.new(source_socket, destination_socket)



# -------------------------------------------------------------
class SWTOR_OT_baking_tools(bpy.types.Operator):
    bl_idname = "swtor.baking_tools"
    bl_label = "Bake Legacy SWTOR Materials into simple Principled BSDF Shader ones"
    bl_description = "Converts all Legacy SWTOR materials in the Blender project to simple Principled Shader-based ones\nwith just baked texturemaps or direct values as inputs, ready for exporting as FBX.\n\n• Requires the presence of Legacy-type SWTOR Materials"
    bl_options = {'REGISTER', 'UNDO'}


    # Check that there is a selection of objects either
    # in the 3D Viewer or in any Outliner in order to
    # enable the operator.
    @classmethod
    def poll(cls,context):
        true_or_false = False
        if bpy.context.selected_objects and bpy.context.mode == "OBJECT":
            true_or_false = True
        else:
            for window in context.window_manager.windows:
                screen = window.screen
                for area in screen.areas:
                    if area.type == 'OUTLINER':
                        with context.temp_override(window=window, area=area):
                            if context.selected_ids:
                                true_or_false = True
                                break
        return true_or_false



    # # Property for the UI buttons to call different actions.
    # # See: https://b3d.interplanety.org/en/calling-functions-by-pressing-buttons-in-blender-custom-ui/
    # action: bpy.props.EnumProperty(
    #     name="Bake Channel",
    #     items=[
    #         ("DIFFUSE", "Diffuse", "Diffuse"),
    #         ("NORMAL", "Normals", "Normals"),
    #         ("GLOSSY", "Glossiness", "Glossiness"),
    #         ("EMIT", "Emissiveness", "Emissiveness"),
    #         ("TRANSMISSION", "Opacity", "Opacity"),
    #         ]
    #     )

    # Property for the UI buttons to call different actions.
    # See: https://b3d.interplanety.org/en/calling-functions-by-pressing-buttons-in-blender-custom-ui/
    use_selection_only: bpy.props.BoolProperty(
        name="Selection-only",
        description='Applies the material processing to the current selection of objects only',
        default = False,
        options={'HIDDEN'}
        )


    # @staticmethod
    # def bake_diffuse():
    #     bpy.context.window.cursor_set("WAIT")
    #     for mat in bpy.data.materials:
    #         if " - LGC" in mat.name:
    #             for node in mat.node_tree.nodes:
    #                 if node.label == "BAKED MATERIAL'S DIFFUSE":
    #                     mat.node_tree.nodes.active = node
    #                     context.scene["Scene"].cycles.bake_type = 'DIFFUSE'
    #                     context.scene.render.bake.use_pass_direct = False
    #                     context.scene.render.bake.use_pass_indirect = False
    #                     context.scene.render.bake.use_pass_color = True
    #                     context.scene.render.bake.use_pass_color = True
    #                     context.scene.render.bake.view_from = 'ABOVE_SURFACE'
    #                     context.scene.render.bake.use_clear = True
    #                     break




    def execute(self, context):

        # # Make duplicates of the objects' materials, prefixing them as "BAKEDMAT"
        # # and assign them, unless they exist and are assigned already

        # for obj in bpy.data.objects:
        #     pass
            

        # Append the baked material template from the auxiliary .blend file inside the Add-on 
        
        aux_blendfile_name = "Legacy SWTOR Shaders and Materials.blend"
        
        legacy_materials_blend_filepath = os.path.join(os.path.dirname(__file__), aux_blendfile_name)

        if Path(legacy_materials_blend_filepath).exists() == False:
            self.report({"WARNING"}, "Unable to find the custom SWTOR shaders .blend file inside this Addon's directory.")
            return {"CANCELLED"}

        legacy_materials_path = bpy.path.native_pathsep(legacy_materials_blend_filepath + "/Material")

        baked_mat_template_name = "BAKED MATERIAL TEMPLATE"
        if baked_mat_template_name not in bpy.data.materials:
            try:
                bpy.ops.wm.append(
                filename=baked_mat_template_name,
                directory=legacy_materials_path,
                do_reuse_local_id=True,  # This seems to be failing, hence the checking
                set_fake=True,
                link=False,
                )
            except:
                self.report({"WARNING"}, "Unable to find the " + baked_mat_template_name + " in the .blend file holding the Legacy SWTOR Materials in this Addon's directory.")
                return {"CANCELLED"}
            
        
        # Append the baked material template node tree's nodes
        # to the existing Legacy SWTOR materials in the project
        
        for mat in bpy.data.materials:
            if " - LGC" in mat.name and "BAKED MATERIAL'S OUTPUT" not in mat.node_tree.nodes:
                merge_material_nodes(baked_mat_template_name, mat.name)
        
        
        # Set general render and baking settings
                
        # Render engine
        context.scene.render.engine = "CYCLES"
        
        # Bake settings
        context.scene.render.use_bake_multires = True
        context.scene.cycles.bake_type = 'DIFFUSE'
        context.scene.render.bake.view_from = "ABOVE_SURFACE"
        
        context.scene.render.bake.use_pass_direct = False
        context.scene.render.bake.use_pass_indirect = False
        context.scene.render.bake.use_pass_color = True
        
        context.scene.render.bake.use_selected_to_active = False

        context.scene.render.bake.target = 'IMAGE_TEXTURES'
        context.scene.render.bake.use_clear = True
        
        context.scene.render.bake.margin_type = 'ADJACENT_FACES'
        context.scene.render.bake.margin = 16

        # Color management
        
        context.scene.display_settings.display_device = 'sRGB'
        context.scene.view_settings.look = 'None'
        context.scene.view_settings.use_curve_mapping = False
        context.scene.view_settings.exposure = 0
        context.scene.view_settings.gamma = 1

        # Cycle through materials, set target, and bake

        for mat in bpy.data.materials:
            nodes=mat.node_tree.nodes
            if "BAKED MATERIAL'S OUTPUT" in nodes:
                
                # Determine texturemap size
                if "_d DiffuseMap" in nodes:
                    tx_size = nodes["_d DiffuseMap"].width
                else:
                    tx_size = 1024
                    
                # Create texturemap image and assign to baking target
                tx_name = mat.name + "DIFFUSE"
                if not tx_name in bpy.data.images:
                    bpy.ops.image.new(
                        name=tx_name,
                        width=tx_size,
                        height=tx_size,
                        color=None,
                        alpha=False,
                    )
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        self.report({'INFO'}, "Conversion finished")
        return {"FINISHED"}
                   
                   

# -------------------------------------------------------------
# Registrations

def register():
    bpy.utils.register_class(SWTOR_OT_baking_tools)



def unregister():
    bpy.utils.unregister_class(SWTOR_OT_baking_tools)

if __name__ == "__main__":
    register()