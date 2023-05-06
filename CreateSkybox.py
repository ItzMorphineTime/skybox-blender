import bpy
import os

# Set your equirectangular texture and depth texture paths.
equirectangular_texture_path = "Forest.jpg" # Set paths here
depth_texture_path = "ForestDepth.jpg"

# Function to create a UV Sphere.
def create_uv_sphere(name, radius, segments, rings, location):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, radius=radius, location=location)
    sphere = bpy.context.active_object
    sphere.name = name
    return sphere

# Function to create a material for the sphere.
def create_material(name, color, equirectangular_texture_path):
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]

    # Load equirectangular texture.
    equirectangular_texture = bpy.data.images.load(equirectangular_texture_path)
    texture_node = material.node_tree.nodes.new('ShaderNodeTexImage')
    texture_node.image = equirectangular_texture
    material.node_tree.links.new(bsdf.inputs['Base Color'], texture_node.outputs['Color'])

    return material


# Create UV Sphere with more segments and rings.
sphere = create_uv_sphere("Skybox", 10, 200, 100, (0, 0, 0))

# Create and apply material.
material = create_material("Skybox_Material", (1, 1, 1, 1), equirectangular_texture_path)
sphere.data.materials.append(material)

# Add a displacement modifier.
#depth_texture_path = "path/to/your/4k_depth_texture.png"
displacement = sphere.modifiers.new("Displacement", 'DISPLACE')
displacement.texture = bpy.data.textures.new("Depth_Displacement", 'IMAGE')
displacement.texture.image = bpy.data.images.load(depth_texture_path)
displacement.texture_coords = 'UV'
displacement.strength = -20

# Enable smooth shading.
bpy.ops.object.shade_smooth()