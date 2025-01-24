import os
import bpy




def smooth_and_extrude(model_path: str, board_path: str, board: str):

  print(model_path)
  print(board_path)
  print(board)

  bpy.ops.object.select_all(action = "SELECT")
  bpy.ops.object.delete(use_global = False)
  
  bpy.ops.wm.obj_import(filepath = model_path)

  imported_objects = bpy.context.selected_objects

  if not imported_objects:
    print("No Object Found")
  
  else:
    # print("Object Found")
    for i, obj in enumerate(imported_objects):
      print(f"imported {i} original name: {obj.name}")

      bpy.context.view_layer.objects.active = obj
      bpy.ops.object.mode_set(mode = "EDIT")
      bpy.ops.mesh.select_all(action = "SELECT")
      bpy.ops.mesh.vertices_smooth(repeat = 10, factor = 0.5)
      bpy.ops.mesh.extrude_region_shrink_fatten(TRANSFORM_OT_shrink_fatten={"value": 0.04})
      bpy.ops.object.mode_set(mode = "OBJECT")
      print(f"smoothing applied to {obj.name}")

  export_path = os.path.join(board_path, f"{board}.obj")
  bpy.ops.wm.obj_export(filepath = export_path, export_materials = False)


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
      smooth_and_extrude(os.path.join(base_path, brand, board, model), board_path, board)

      

      