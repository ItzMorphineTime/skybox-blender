import bpy
from bpy.props import PointerProperty, FloatProperty

# Custom panel to modify base color texture, depth texture, and displacement strength.
class OBJECT_PT_CustomSkyboxPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_CustomSkyboxPanel"
    bl_label = "Skybox Settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Skybox'

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj.type == 'MESH' and obj.data.materials:
            material = obj.data.materials[0]
            layout.prop(material, "custom_base_color_texture")
            layout.prop(material, "custom_depth_texture")

            if obj.modifiers:
                for mod in obj.modifiers:
                    if mod.type == 'DISPLACE':
                        layout.prop(mod, "strength")

# Update function to change base color texture.
def update_base_color_texture(self, context):
    material = self
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    base_color_texture_node = nodes.get("Image Texture")

    if base_color_texture_node:
        base_color_texture_node.image = material.custom_base_color_texture

# Update function to change depth texture.
def update_depth_texture(self, context):
    obj = context.active_object
    depth_texture_node = obj.modifiers['Displacement'].texture

    if depth_texture_node:
        depth_texture_node.image = self.custom_depth_texture

# Register the custom properties.
def register():
    bpy.types.Material.custom_base_color_texture = PointerProperty(
        type=bpy.types.Image,
        name="Base Color Texture",
        description="Base color texture for the skybox",
        update=update_base_color_texture
    )

    bpy.types.Material.custom_depth_texture = PointerProperty(
        type=bpy.types.Image,
        name="Depth Texture",
        description="Depth texture for the skybox",
        update=update_depth_texture
    )

    bpy.utils.register_class(OBJECT_PT_CustomSkyboxPanel)

# Unregister the custom properties.
def unregister():
    bpy.utils.unregister_class(OBJECT_PT_CustomSkyboxPanel)
    del bpy.types.Material.custom_base_color_texture
    del bpy.types.Material.custom_depth_texture

if __name__ == "__main__":
    register()