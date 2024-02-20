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

    print(data)

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
            generate_board_model(brand, board)

            # print(brand, board)

    return JsonResponse(
        {
            'success': True
        }
    )


def check_directories(brand):
    front_end_base_dir = os.path.join(settings.BASE_DIR.parent, 'frontend/public/images/mens')
    print(front_end_base_dir)
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
    front_end_base_dir = os.path.join(settings.BASE_DIR.parent, 'frontend/public/images/mens')
    for image in os.listdir(os.path.join(front_end_base_dir, brand, 'splits', board.replace('.jpg', ''))):
        img = cv2.imread(os.path.join(front_end_base_dir, brand, 'splits', board.replace('.jpg', ''), image))
        if img.shape[2] == 4:
            _, alpha = cv2.threshold(img[:, :, 3], 0, 255, cv2.THRESH_BINARY)
            mask = cv2.bitwise_not(alpha)
        else:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        largest_contour = max(contours, key = cv2.contourArea)
        contour_mask = np.zeros_like(mask)
        cv2.drawContours(contour_mask, [largest_contour], -1, color = 255, thickness = -1)
        cv2.imwrite(os.path.join(front_end_base_dir, brand, 'masks', board.replace('.jpg', ''), image), contour_mask)

def generate_board_model(brand, board):
    front_end_base_dir = os.path.join(settings.BASE_DIR.parent, 'frontend/public/images/mens')
    # side_contour = load_masks_and_find_contours('./sidemask-resized.jpg')
    # top_contour = load_masks_and_find_contours(f"./mens/{brand}/masks/{board.replace('.jpg', '')}/{board.replace('.jpg', '_0.jpg')}")
    top_contour = load_masks_and_find_contours(os.path.join(front_end_base_dir, brand, 'masks', board.replace('.jpg', ''), board.replace('.jpg', '_0.jpg')))

    top_contour = np.squeeze(top_contour)

    flat_vertices = []
    for point in top_contour:
        flat_vertices.append([point[0], point[1], 0])

    flat_vertices = np.array(flat_vertices).astype(np.float64)

    max_y_mesh = np.max(flat_vertices[:, 1])
    flat_vertices[:, 0] /= max_y_mesh
    flat_vertices[:, 1] /= max_y_mesh

    flat_faces = []
    for i in range(1, len(flat_vertices) - 1):
        flat_faces.append([0, i, i + 1])

    mesh = trimesh.Trimesh(vertices = flat_vertices, faces = flat_faces)
    mesh.export(os.path.join(front_end_base_dir, brand, 'models', board.replace('.jpg', ''), board.replace('.jpg', '.obj')))

def load_masks_and_find_contours(path):
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour = max(contours, key = cv2.contourArea)
    return contour