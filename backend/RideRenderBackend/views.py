from django.shortcuts import render

import os
from django.conf import settings
from django.http import JsonResponse

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

import json

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