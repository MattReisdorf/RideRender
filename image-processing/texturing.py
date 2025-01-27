import os
import bpy

def assign_two_textures_by_normal(model_path, pos_y_image_path, neg_y_image_path):
  bpy.ops.object.select_all(action = "SELECT")
  bpy.ops.object.delete(use_global = False)
  
  bpy.ops.wm.obj_import(filepath = model_path)

  imported_objects = bpy.context.selected_objects

  if not imported_objects:
    print("No Object Found")
  
  else:
    for i, obj in enumerate(imported_objects):

      top_mat = bpy.data.materials.new("Snowboard_Top")
      top_mat.use_nodes = True
      nodes_top = top_mat.node_tree.nodes
      links_top = top_mat.node_tree.links

      for node in nodes_top:
        nodes_top.remove(node)

      out_top = nodes_top.new(type = "ShaderNodeOutputMaterial")
      bsdf_top = nodes_top.new(type = "ShaderNodeBsdfPrincipled")
      tex_top = nodes_top.new(type = "ShaderNodeTexImage")

      top_image_path = pos_y_image_path
      top_image = bpy.data.images.load(top_image_path)
      tex_top.image = top_image

      bsdf_top.location = (0, 0)
      tex_top.location = (-300, 0)
      out_top.location = (200, 0)

      links_top.new(tex_top.outputs['Color'], bsdf_top.inputs['Base Color'])
      links_top.new(bsdf_top.outputs['BSDF'], out_top.inputs['Surface'])

      bottom_mat = bpy.data.materials.new("Snowboard_Bottom")
      bottom_mat.use_nodes = True
      nodes_bottom = bottom_mat.node_tree.nodes
      links_bottom = bottom_mat.node_tree.links

      for node in nodes_bottom:
          nodes_bottom.remove(node)

      out_bottom = nodes_bottom.new(type='ShaderNodeOutputMaterial')
      bsdf_bottom = nodes_bottom.new(type='ShaderNodeBsdfPrincipled')
      tex_bottom = nodes_bottom.new(type='ShaderNodeTexImage')

      bottom_image_path = neg_y_image_path
      bottom_image = bpy.data.images.load(bottom_image_path)
      tex_bottom.image = bottom_image

      bsdf_bottom.location = (0, 0)
      tex_bottom.location = (-300, 0)
      out_bottom.location = (200, 0)

      links_bottom.new(tex_bottom.outputs['Color'], bsdf_bottom.inputs['Base Color'])
      links_bottom.new(bsdf_bottom.outputs['BSDF'], out_bottom.inputs['Surface'])

      mesh = obj.data

      mesh.materials.clear()
      mesh.materials.append(top_mat)
      mesh.materials.append(bottom_mat)

      bpy.ops.object.mode_set(mode = "OBJECT")

      for poly in mesh.polygons:
        if poly.normal.y >= 0.0:
          poly.material_index = 0
        else:
          poly.material_index = 1


      bpy.ops.object.mode_set(mode='EDIT')
      bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
      bpy.ops.object.mode_set(mode='OBJECT')


      export_path = os.path.join(board_path, f"{board}.obj")
      bpy.ops.wm.obj_export(filepath = export_path, export_materials = True)



base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'boards')

for brand in os.listdir(base_path):
  brand_path = os.path.join(base_path, brand)
  for board in os.listdir(brand_path):
    board_path = os.path.join(brand_path, board)
    for model in os.listdir(board_path):
      if '.obj' not in model:
        continue
      assign_two_textures_by_normal(os.path.join(base_path, brand, board, model), os.path.join(base_path, brand, board, f"{board}-top.png"), os.path.join(base_path, brand, board, f"{board}-bottom.png"))
      