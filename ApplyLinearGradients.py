import cv2
import numpy as np
import bpy

def create_linear_gradient(height, ratio=[0.1, 0.4, 0.4, 0.1]):
    gradient = np.zeros((height, 1), dtype=np.float32)
    h1, h2, h3, h4 = [int(height * r) for r in ratio]
    

    # White to black.
    gradient[:h1] = np.linspace(0, 1, h1, dtype=np.float32)[:, np.newaxis]
    
    # Black to black.
    gradient[h1:h1+h2] = 1
    
    # Black to white.
    gradient[h1+h2:h1+h2+h3] = np.linspace(1, 0.1, h3, dtype=np.float32)[:, np.newaxis]
    
    # White to white.
    gradient[h1+h2+h3:] = 0.1
#    gradient[:50] = 0

    return gradient

def create_linear_gradient2(height, ratio=[0.1, 0.4, 0.4, 0.1]):
    gradient = np.zeros((height, 1), dtype=np.float32)
    h1, h2, h3, h4 = [int(height * r) for r in ratio]
    

    # White to black.
    gradient[:h1] = np.linspace(1, 0, h1, dtype=np.float32)[:, np.newaxis]
    
    # Black to black.
    gradient[h1:h1+h2] = 0
    
    # Black to white.
    gradient[h1+h2:h1+h2+h3] = np.linspace(0, .7, h3, dtype=np.float32)[:, np.newaxis]
    
    # White to white.
    gradient[h1+h2+h3:] = .7
    gradient[-50:] = 0
    gradient[:50] = 0
    
    return gradient

def multiply_depth_texture_with_gradient(depth_texture_path, gradient, output_texture_path):
    depth_texture = cv2.imread(depth_texture_path, cv2.IMREAD_GRAYSCALE)
    depth_texture = depth_texture.astype(np.float32) / 255.0
    
    gradient_repeated = np.repeat(gradient, depth_texture.shape[1], axis=1)
    multiplied_texture = depth_texture * gradient_repeated
    
    cv2.imwrite(output_texture_path, (multiplied_texture * 255).astype(np.uint8))
    cv2.imwrite(bpy.path.abspath("//temp_depth_texture_grad.png"), (gradient_repeated * 255).astype(np.uint8))
    
def add_depth_texture_with_gradient(depth_texture_path, gradient, output_texture_path):
    depth_texture = cv2.imread(depth_texture_path, cv2.IMREAD_GRAYSCALE)
    depth_texture = depth_texture.astype(np.float32) / 255.0
    
    gradient_repeated = np.repeat(gradient, depth_texture.shape[1], axis=1)
    multiplied_texture = depth_texture + gradient_repeated
    
    cv2.imwrite(output_texture_path, (multiplied_texture * 255).astype(np.uint8))
    cv2.imwrite(bpy.path.abspath("//temp_depth_texture_grad2.png"), (gradient_repeated * 255).astype(np.uint8))
    

# Get the depth texture from the Displacement modifier.
skybox_object = bpy.data.objects["Skybox"]
depth_texture = skybox_object.modifiers['Displacement'].texture.image

# Save the depth texture to a temporary file.
temp_depth_texture_path = bpy.path.abspath("//temp_depth_texture.png")
#depth_texture.filepath_raw = temp_depth_texture_path
#depth_texture.save()

# Create a custom linear gradient.
gradient = create_linear_gradient(depth_texture.size[1], [0.1, 0.4, 0.4, 0.1])
gradient2 = create_linear_gradient2(depth_texture.size[1], [0.1, 0.4, 0.4, 0.1])

# Set the output modified texture path.
output_texture_path = bpy.path.abspath("//temp_modified_depth_texture.png")

# Multiply the depth texture with the custom gradient and save the new texture.
multiply_depth_texture_with_gradient(temp_depth_texture_path, gradient, output_texture_path)
# Set the output modified texture path.
output_texture_path2 = bpy.path.abspath("//modified_depth_texture.png")
add_depth_texture_with_gradient(output_texture_path, gradient2, output_texture_path2)
#depth_texture.filepath_raw = output_texture_path2
#depth_texture.save()