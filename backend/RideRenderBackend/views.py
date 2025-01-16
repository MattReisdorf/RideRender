from django.shortcuts import render

import os
from django.conf import settings
from django.http import JsonResponse

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

import json




from split_image import split_image
from PIL import Image
import cv2
import numpy as np
import trimesh

import bpy

# Create your views here.

@csrf_exempt
@require_http_methods(["GET"])
def get_boards_json(request):
    images_directory = os.path.join(settings.BASE_DIR.parent, 'frontend/public/images/mens')

    brands = {}

    for brand in os.listdir(images_directory):
        brand_path = os.path.join(images_directory, brand)
        if os.path.isdir(brand_path):
            boards = []
            for board in os.listdir(brand_path):
                board_path = os.path.join(brand_path, board)
                if not os.path.isdir(board_path):
                    brand_folder = board_path.split(os.sep)[-2]
                    board_name = board_path.split(os.sep)[-1].replace('-', ' ').replace('.jpg', '')
                    if brand_folder == 'Yes':
                        boards.append(board_name.replace('Yes. ', ''))
                    else:
                        boards.append(board_name.replace(brand_folder + ' ', ''))
            brands[brand] = boards
    
    return JsonResponse (
        {
            "Success": True,
            "boards": brands
        }
    )

@csrf_exempt
@require_http_methods(["POST"])
def check_board_existence(request):
    image_exists = False

    data = json.loads(request.body)
    brand = data['brand']
    board = data['board']

    # print(data)

    images_directory = os.path.join(settings.BASE_DIR.parent, 'frontend/public/images/mens/')

    if brand == 'Yes':
        full_image_path = os.path.join(images_directory, f"{brand}/{brand.replace(' ', '-') + '.' if data['brand'] else ''}-{board.replace(' ', '-') if data['board'] else ''}.jpg")
    else:
        full_image_path = os.path.join(images_directory, f"{brand}/{brand.replace(' ', '-') if data['brand'] else ''}-{board.replace(' ', '-') if data['board'] else ''}.jpg")

    if os.path.exists(full_image_path):
        image_exists = True
    else:
        image_exists = False
    
    return JsonResponse (
        {
            "imageExists": image_exists,
            "path": full_image_path
        }
    )

@csrf_exempt
@require_http_methods(["POST"])
def check_model_existence(request):
    model_exists = False
    data = json.loads(request.body)
    brand = data["brand"]
    board = data["board"]

    front_end_base_dir = os.path.join(settings.BASE_DIR.parent, 'frontend/public/images/mens')

    if brand == "Yes":
        full_model_path = os.path.join(front_end_base_dir, f"{brand}/models/{brand.replace(' ', '-') + '.' if data['brand'] else ''}-{board.replace(' ', '-') if data['board'] else ''}/{brand.replace(' ', '-') + '.' if data['brand'] else ''}-{board.replace(' ', '-') if data['board'] else ''}.obj")
    else:
        full_model_path = os.path.join(front_end_base_dir, f"{brand}/models/{brand.replace(' ', '-') if data['brand'] else ''}-{board.replace(' ', '-') if data['board'] else ''}/{brand.replace(' ', '-') if data['brand'] else ''}-{board.replace(' ', '-') if data['board'] else ''}.obj")

    if os.path.exists(full_model_path):
        model_exists = True

    return JsonResponse (
        {
            "modelExists": model_exists,
            "path": full_model_path
        }
    )



# THIS WILL NOT BE A VIEW/URL LATER -> PLAN TO CONVERT TO DJANGOQ FUNCTION
@csrf_exempt
@require_http_methods(["GET"])
def generate_board_models(request):
    front_end_base_dir = os.path.join(settings.BASE_DIR.parent, 'frontend/public/images/mens')
    for brand in os.listdir(front_end_base_dir):
        check_directories(brand)
        split_images(brand)
        for board in os.listdir(f"{front_end_base_dir}/{brand}"):
            if os.path.isdir(os.path.join(front_end_base_dir, brand, board)):
                continue
            crop_images(brand, board)
            generate_masks(brand, board)
            # compare_masks(brand, board)
            generate_board_model(brand, board, invert = False, scale = 0.01)
            # smoothVertices(brand, board)

            # print(brand, board)

    return JsonResponse(
        {
            'success': True
        }
    )


def check_directories(brand):
    front_end_base_dir = os.path.join(settings.BASE_DIR.parent, 'frontend/public/images/mens')
    # print(front_end_base_dir)
    for i in ['splits', 'masks', 'models']:
        if not os.path.exists(os.path.join(front_end_base_dir, brand, i)):
            os.makedirs(os.path.join(front_end_base_dir, brand, i))
    for board in os.listdir(os.path.join(front_end_base_dir, brand)):
        if os.path.isdir(os.path.join(front_end_base_dir, brand, board)):
            continue
        else:
            if not os.path.exists(os.path.join(front_end_base_dir, brand, 'splits', board.replace('.jpg', ''))):
                os.makedirs(os.path.join(front_end_base_dir, brand, 'splits', board.replace('.jpg', '')))
            if not os.path.exists(os.path.join(front_end_base_dir, brand, 'masks', board.replace('.jpg', ''))):
                os.makedirs(os.path.join(front_end_base_dir, brand, 'masks', board.replace('.jpg', '')))
            if not os.path.exists(os.path.join(front_end_base_dir, brand, 'models', board.replace('.jpg', ''))):
                os.makedirs(os.path.join(front_end_base_dir, brand, 'models', board.replace('.jpg', '')))


def split_images(brand):
    front_end_base_dir = os.path.join(settings.BASE_DIR.parent, 'frontend/public/images/mens')
    for board in os.listdir(os.path.join(front_end_base_dir, brand)):
        if os.path.isdir(os.path.join(front_end_base_dir, brand, board)):
            continue
        # Remove alpha channel that shouldn't exist
        im = Image.open(os.path.join(front_end_base_dir, brand, board))
        rgb_im = im.convert('RGB')
        rgb_im.save(os.path.join(front_end_base_dir, brand, board))
        # Split the images down the middle
        split_image(os.path.join(front_end_base_dir, brand, board), 1, 2, output_dir = os.path.join(front_end_base_dir, brand, 'splits', board.replace('.jpg', '')), should_cleanup = False, should_square = False)


def crop_images(brand, board):
    front_end_base_dir = os.path.join(settings.BASE_DIR.parent, 'frontend/public/images/mens')
    for image in os.listdir(os.path.join(front_end_base_dir, brand, 'splits', board.replace('.jpg', ''))):
        # print(os.path.join(front_end_base_dir, brand, 'splits', board.replace('.jpg', ''), image))
        img = cv2.imread(os.path.join(front_end_base_dir, brand, 'splits', board.replace('.jpg', ''), image))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)
        cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        cnt = sorted(cnts, key = cv2.contourArea)[-1]
        x, y, w, h = cv2.boundingRect(cnt)
        dst = img[y:y+h, x:x+w]
        cv2.imwrite(os.path.join(front_end_base_dir, brand, 'splits', board.replace('.jpg', ''), image), dst)


def generate_masks(brand, board):
    # Base Directory for Images stored in front end
    front_end_base_dir = os.path.join(settings.BASE_DIR.parent, 'frontend/public/images/mens')

    for image in os.listdir(os.path.join(front_end_base_dir, brand, 'splits', board.replace('.jpg', ''))):
        # Read each image
        img = cv2.imread(os.path.join(front_end_base_dir, brand, 'splits', board.replace('.jpg', ''), image))
        
        # Preprocessing
        # Convert to Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply Gaussian Blur -> Reduces Noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Thresholding
        mask = cv2.adaptiveThreshold(
            blurred,
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            2
        )

        # _, mask = cv2.threshold(blurred, 240, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)

        # Morphology
        # Define Structuring Element for Opening/Closing
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
        # Opening Removes Small Noise
        mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        # CLosing Fills Small Holes
        mask_cleaned = cv2.morphologyEx(mask_cleaned, cv2.MORPH_CLOSE, kernel)

        # Contour Filtering
        # Find Contours of Cleaned Mask
        contours, _ = cv2.findContours(mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Select Largest Contour by Area
            largest_contour = max(contours, key = cv2.contourArea)

            # Create Blank Image and Draw Filled Contour
            final_mask = np.zeros_like(mask_cleaned)
            cv2.drawContours(final_mask, [largest_contour], -1, color = 255, thickness = -1)

            # Save Mask
            cv2.imwrite(os.path.join(front_end_base_dir, brand, 'masks', board.replace('.jpg', ''), image), final_mask)

def compare_masks(brand, board):
    front_end_base_dir = os.path.join(settings.BASE_DIR.parent, 'frontend/public/images/mens')

    masks = os.path.join(front_end_base_dir, brand, 'masks', board.replace('.jpg', ''))

    top_mask_path = os.path.join(masks, f"{board.replace('.jpg', '')}_0.jpg")
    # print(top_mask)
    bottom_mask_path = os.path.join(masks, f"{board.replace('.jpg', '')}_1.jpg")
    # print(bottom_mask)

    top_mask = cv2.imread(top_mask_path, cv2.IMREAD_GRAYSCALE)
    bottom_mask = cv2.imread(bottom_mask_path, cv2.IMREAD_GRAYSCALE)

    area_top = np.count_nonzero(top_mask)
    area_bottom = np.count_nonzero(bottom_mask)

    if area_top > area_bottom:
        return(top_mask_path)
        # print("Top Area Is Larger")
    elif area_bottom > area_top:
        return(bottom_mask_path)
        # print("Bottom Area Larger")
    # else:
        # print("Masks are the same")

    # print("\n")




# def generate_masks(brand, board):
#     front_end_base_dir = os.path.join(settings.BASE_DIR.parent, 'frontend/public/images/mens')
#     for image in os.listdir(os.path.join(front_end_base_dir, brand, 'splits', board.replace('.jpg', ''))):
#         # Read Image from front end
#         img = cv2.imread(os.path.join(front_end_base_dir, brand, 'splits', board.replace('.jpg', ''), image))
#         # Removing alpha channel from image
#         if img.shape[2] == 4:
#             _, alpha = cv2.threshold(img[:, :, 3], 0, 255, cv2.THRESH_BINARY)
#             mask = cv2.bitwise_not(alpha)
#         # Converting to Grayscale if not alpha
#         else:
#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
        

#         contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         largest_contour = max(contours, key = cv2.contourArea)
#         contour_mask = np.zeros_like(mask)
#         cv2.drawContours(contour_mask, [largest_contour], -1, color = 255, thickness = -1)
#         cv2.imwrite(os.path.join(front_end_base_dir, brand, 'masks', board.replace('.jpg', ''), image), contour_mask)

def generate_board_model(brand, board, invert: bool = False, scale: float = 1.0):
    # Base Directory for Front End
    front_end_base_dir = os.path.join(settings.BASE_DIR.parent, 'frontend/public/images/mens')

    # Load Image in Grayscale
    img_path = compare_masks(brand, board)
    img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img_gray is None:
        raise FileNotFoundError(f"Could not read image at {img_path}")
    
    # Threshold Image to Ensure Binary
    _, mask = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

    # Find Contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("No Contours Found")
    
    main_contour = max(contours, key = cv2.contourArea)

    # Convert Contour Points to a List of (x,y) coordinates
    pts = main_contour.squeeze(axis = 1)

    # Write .OBJ File
    with open(os.path.join(front_end_base_dir, brand, 'models', board.replace('.jpg', ''), board.replace('.jpg', '.obj')), "w") as f:
        f.write(f"{board.replace('.jpg', '')}\n")

        for (x, y) in pts:
            f.write(f"v {x * scale:1f} {-y * scale: 1f} 0.0 \n")

        num_vertices = len(pts)
        face_indices = " ".join(str(i + 1) for i in range(num_vertices))
        f.write(f"f {face_indices}\n")

    # print(f"OBJ Successfuly Saved")
    


# def generate_board_model(brand, board):
#     front_end_base_dir = os.path.join(settings.BASE_DIR.parent, 'frontend/public/images/mens')
#     # side_contour = load_masks_and_find_contours('./sidemask-resized.jpg')
#     # top_contour = load_masks_and_find_contours(f"./mens/{brand}/masks/{board.replace('.jpg', '')}/{board.replace('.jpg', '_0.jpg')}")
#     top_contour = load_masks_and_find_contours(os.path.join(front_end_base_dir, brand, 'masks', board.replace('.jpg', ''), board.replace('.jpg', '_0.jpg')))

#     area = cv2.contourArea(top_contour, oriented = True)
#     if area < 0:
#         print("contours are clockwise, reversing...")
#         top_contour = np.flipud(top_contour)
#         top_contour.reshape((-1, 1, 2))




#     vertices_2d = top_contour.reshape(-1, 2).astype(np.float64)
#     max_y = np.amax(vertices_2d[:, 1])
#     vertices_2d[:, 0] /= max_y
#     vertices_2d[:, 1] /= max_y
#     vertices_bottom = np.hstack((vertices_2d, np.zeros((vertices_2d.shape[0], 1))))

#     # print(vertices_bottom[:3])

#     vertices_top = vertices_bottom.copy()
#     vertices_top[:, 2] += .005 # extrusion height

#     # print(vertices_top[:3])

#     side_faces = []
#     for i in range(len(vertices_bottom)):
#         next_i = (i + 1) % len(vertices_bottom)
#         side_faces.extend([
#             [i, next_i, next_i + len(vertices_bottom)],
#             [i, next_i + len(vertices_bottom), i + len(vertices_bottom)]
#         ])

#     vertices = np.vstack([vertices_bottom, vertices_top])

#     # print(vertices[:3])

#     top_faces = [[len(vertices_bottom), i + len(vertices_bottom), (i + 1) % len(vertices_bottom) + len(vertices_bottom)] for i in range(len(vertices_bottom))]
#     bottom_faces = [[0, (i + 1) % len(vertices_bottom), i] for i in range(len(vertices_bottom))]

#     faces = np.vstack([bottom_faces, top_faces, side_faces])

#     mesh = trimesh.Trimesh(vertices = vertices, faces = faces)
#     if not mesh.is_volume:
#         mesh.fill_holes()

#     # mesh.fix_normals()

#     mesh.apply_scale(.1)



#     mesh.export(os.path.join(front_end_base_dir, brand, 'models', board.replace('.jpg', ''), board.replace('.jpg', '.obj')))






#     # top_contour = np.squeeze(top_contour)

#     # flat_vertices = []
#     # for point in top_contour:
#     #     flat_vertices.append([point[0], point[1], 0])

#     # flat_vertices = np.array(flat_vertices).astype(np.float64)

#     # max_y_mesh = np.max(flat_vertices[:, 1])
#     # flat_vertices[:, 0] /= max_y_mesh
#     # flat_vertices[:, 1] /= max_y_mesh

#     # flat_faces = []
#     # for i in range(1, len(flat_vertices) - 1):
#     #     flat_faces.append([0, i, i + 1])

#     # mesh = trimesh.Trimesh(vertices = flat_vertices, faces = flat_faces)

#     #     # Duplicate and translate the vertices to create the top surface
#     # top_vertices = flat_vertices.copy()
#     # top_vertices[:, 2] += .0050  # Adjust the 10 to change the thickness

#     # # Combine the vertices and faces for the top and bottom surfaces
#     # all_vertices = np.vstack((flat_vertices, top_vertices))
#     # top_faces = [[vertex_index + len(flat_vertices) for vertex_index in face] for face in flat_faces]
#     # # top_faces = flat_faces.copy() + len(flat_vertices)
#     # all_faces = np.vstack((flat_faces, top_faces))

#     # # Create the side faces
#     # for i in range(len(flat_faces)):
#     #     face = flat_faces[i]
#     #     all_faces = np.vstack((all_faces, [face[0], face[1], face[1] + len(flat_vertices)]))
#     #     all_faces = np.vstack((all_faces, [face[0], face[1] + len(flat_vertices), face[0] + len(flat_vertices)]))
#     #     all_faces = np.vstack((all_faces, [face[1], face[2], face[2] + len(flat_vertices)]))
#     #     all_faces = np.vstack((all_faces, [face[1], face[2] + len(flat_vertices), face[1] + len(flat_vertices)]))
#     #     all_faces = np.vstack((all_faces, [face[2], face[0], face[0] + len(flat_vertices)]))
#     #     all_faces = np.vstack((all_faces, [face[2], face[0] + len(flat_vertices), face[2] + len(flat_vertices)]))

#     # # Create the extruded mesh
#     # extruded_mesh = trimesh.Trimesh(vertices=all_vertices, faces=all_faces)
#     # extruded_mesh.export(os.path.join(front_end_base_dir, brand, 'models', board.replace('.jpg', ''), board.replace('.jpg', '.obj')))

# def load_masks_and_find_contours(path):
#     image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
#     _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
#     contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     contour = max(contours, key = cv2.contourArea)
#     return contour


def smoothVertices(brand, board):
    front_end_base_dir = os.path.join(settings.BASE_DIR.parent, 'frontend/public/images/mens')


    # print(os.path.join(front_end_base_dir, brand, 'models', board.replace('.jpg', '')))

    model_dir = os.path.join(front_end_base_dir, brand, 'models', board.replace('.jpg', ''))

    for model in os.listdir(model_dir):
        print(os.path.abspath(model))

        model_path = os.path.join(model_dir, model)
        print(f"\n{model_path}\n")
        
        
        bpy.ops.object.select_all(action = "SELECT")
        bpy.ops.object.delete(use_global = False)

        bpy.ops.wm.obj_import(filepath = f"./{model}")


        imported_objects = bpy.context.selected_objects

        if not imported_objects:
            print("No Object Found")
        
        else:
            for i, obj in enumerate(imported_objects):
                print(f"Imported Object {i} original name: {obj.name}")

                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode = "EDIT")
                bpy.ops.mesh.select_all(action = "SELECT")
                bpy.mesh.vertices_smooth(repeat = 10, factor = 0.5)
                bpy.ops.object.mode_set(mode = "OBJECT")
                print(f"Smoothing Applied to {obj.name}")

        export_path = f"{model.replace('obj', '')}-smooth.obj"
        bpy.ops.wm.obj_export(filepath = export_path, export_materials = False)

        # print(model)