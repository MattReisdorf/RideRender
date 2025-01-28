from django.shortcuts import render

import os
from django.conf import settings
from django.http import JsonResponse, HttpResponse, Http404

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from django.core.exceptions import BadRequest

from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

load_dotenv()

base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))

cred = credentials.Certificate(os.getenv('FIREBASE_SA_PATH'))
firebase_admin.initialize_app(cred, {
  'storageBucket': os.getenv('FIREBASE_BUCKET_NAME')
})

bucket = storage.bucket()

@csrf_exempt
@require_http_methods(["GET"])
def get_glb_model(request, model_name):

  try:
    glb = bucket.blob(f"{model_name}.glb").download_as_bytes()

    response = HttpResponse(glb, content_type = 'model/gltf-binary')
    response['Cache-Control'] = 'max-age=3600'

    return response
  except Exception as exception:
    raise Http404(f"Error retrieving GLB file: {str(exception)}")

@csrf_exempt
@require_http_methods(["POST"])
def model_existence(request, model_name):
  print(model_name)

  try:
    blobs = bucket.list_blobs()
    for blob in blobs:
      if model_name in blob.name:
        return JsonResponse({
          "Success": True,
          "modelExists": True
        })
      else:
        return JsonResponse({
          "Success": True,
          "modelExists": False
        })
  except:
    return JsonResponse({
      "Success": False,
      "Exception": BadRequest
    })