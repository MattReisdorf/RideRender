import os
import bpy



def create_material_with_texture(mat_name: str, image_path: str):
  # Create Material
  mat = bpy.data.materials.new(name = mat_name)
  mat.use_nodes = True

  # Clear Existing Nodes
  nodes = mat.node_tree.nodes
  nodes.clear()

  # Create Needed Nodes
  output_node = nodes.new(type = 'ShaderNodeOutputMaterial')
  output_node.location = (300, 0)

  principled_node = nodes.new(type = 'ShaderNodeBsdfPrincipled')
  principled_node.location = (0, 0)

  tex_image_node = nodes.new(type = 'ShaderNodeTexImage')
  tex_image_node.location = (-300, 0)

  # Load Image
  if os.path.isfile(image_path):
    tex_image_node.image = bpy.data.images.load(image_path)
  else:
    raise FileNotFoundError(f"Image not found at {image_path}")
  
  links = mat.node_tree.links
  links.new(tex_image_node.outputs['Color'], principled_node.inputs['Base Color'])
  links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])

  return mat

def assign_two_textures_by_normal(model_path, pos_y_image_path, neg_y_image_path):
  bpy.ops.object.select_all(action = "SELECT")
  bpy.ops.object.delete(use_global = False)
  
  bpy.ops.wm.obj_import(filepath = model_path)

  imported_objects = bpy.context.selected_objects

  if not imported_objects:
    print("No Object Found")
  
  else:
    # print("Object Found")
    for i, obj in enumerate(imported_objects):
      # print(f"imported {i} original name: {obj.name}")

      # Create Top Sheet Material
      top_mat = bpy.data.materials.new("Snowboard_Top")
      top_mat.use_nodes = True
      nodes_top = top_mat.node_tree.nodes
      links_top = top_mat.node_tree.links

      # Clear Default Nodes
      for node in nodes_top:
        nodes_top.remove(node)

      # Create Output, BSDF, and Image Nodes for Top Material
      out_top = nodes_top.new(type = "ShaderNodeOutputMaterial")
      bsdf_top = nodes_top.new(type = "ShaderNodeBsdfPrincipled")
      tex_top = nodes_top.new(type = "ShaderNodeTexImage")

      # Load Image for Top Sheet
      top_image_path = pos_y_image_path
      top_image = bpy.data.images.load(top_image_path)
      tex_top.image = top_image

      # Arrange Nodes
      bsdf_top.location = (0, 0)
      tex_top.location = (-300, 0)
      out_top.location = (200, 0)

      # Link color output of the image to Base Color of Principled BSDF
      links_top.new(tex_top.outputs['Color'], bsdf_top.inputs['Base Color'])
      # Link BSDF to Material Output
      links_top.new(bsdf_top.outputs['BSDF'], out_top.inputs['Surface'])

      # Create "Bottom" material
      bottom_mat = bpy.data.materials.new("Snowboard_Bottom")
      bottom_mat.use_nodes = True
      nodes_bottom = bottom_mat.node_tree.nodes
      links_bottom = bottom_mat.node_tree.links

      # Clear default nodes
      for node in nodes_bottom:
          nodes_bottom.remove(node)

      # Create output, BSDF, and image nodes for the bottom material
      out_bottom = nodes_bottom.new(type='ShaderNodeOutputMaterial')
      bsdf_bottom = nodes_bottom.new(type='ShaderNodeBsdfPrincipled')
      tex_bottom = nodes_bottom.new(type='ShaderNodeTexImage')

      # Load image for the bottom side
      bottom_image_path = neg_y_image_path
      bottom_image = bpy.data.images.load(bottom_image_path)
      tex_bottom.image = bottom_image

      # Arrange nodes (optional, purely cosmetic)
      bsdf_bottom.location = (0, 0)
      tex_bottom.location = (-300, 0)
      out_bottom.location = (200, 0)

      # Link color output of the image to Base Color of Principled BSDF
      links_bottom.new(tex_bottom.outputs['Color'], bsdf_bottom.inputs['Base Color'])
      # Link BSDF to Material Output
      links_bottom.new(bsdf_bottom.outputs['BSDF'], out_bottom.inputs['Surface'])

      # for mat in bpy.data.materials:
      #   print(mat.name)

      # Assign Materials to Mesh
      mesh = obj.data

      mesh.materials.clear()
      mesh.materials.append(top_mat)
      mesh.materials.append(bottom_mat)

      # print(mesh.materials[:])
      
      # Select Faces by Normal and Assign
      bpy.ops.object.mode_set(mode = "OBJECT")

      for poly in mesh.polygons:
        # print(poly.normal)
        if poly.normal.y >= 0.0:
          print(poly.normal)
          poly.material_index = 0
        else:
          poly.material_index = 1


      bpy.ops.object.mode_set(mode='EDIT')
      # You can choose different unwrap methods or mark seams as needed
      bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
      bpy.ops.object.mode_set(mode='OBJECT')


      # export_path = os.path.join(board_path, f"{board}.gltf")
      # # bpy.ops.wm.obj_export(filepath = export_path, export_materials = True)
      # bpy.ops.export_scene.gltf(
      #   filepath = export_path,
      #   export_format = 'GLB',
      #   export_materials = 'EXPORT',
      #   # export_images = 'COPY'
      # )



base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'boards')

for brand in os.listdir(base_path):
  brand_path = os.path.join(base_path, brand)
  # print(brand_path)
  for board in os.listdir(brand_path):
    board_path = os.path.join(brand_path, board)
    # print(board_path)
    # masks = []
    for model in os.listdir(board_path):
      if '.obj' not in model:
        continue
      # print(os.path.join(base_path, brand, board, f"{board}-top.png"))
      # create_material_with_texture(f"{board}-top-material", os.path.join(base_path, brand, board, f"{board}-top.png"))
      assign_two_textures_by_normal(os.path.join(base_path, brand, board, model), os.path.join(base_path, brand, board, f"{board}-top.png"), os.path.join(base_path, brand, board, f"{board}-bottom.png"))
      # if 'texture.obj' in model:
      #   os.remove(os.path.join(base_path, brand, board, model))
      