import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage


load_dotenv()

cred = credentials.Certificate(os.getenv('FIREBASE_SA_PATH'))
firebase_admin.initialize_app(cred, {
  'storageBucket': os.getenv('FIREBASE_BUCKET_NAME')
})

bucket = storage.bucket()

# Get the models already in FB
existing_blobs = []
for blob in bucket.list_blobs():
  existing_blobs.append(blob.name);

print(existing_blobs);
base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'boards')
for brand in os.listdir(base_path):
  brand_path = os.path.join(base_path, brand)
  for board in os.listdir(brand_path):
    board_path = os.path.join(brand_path, board)
    for model in os.listdir(board_path):
      if '.glb' not in model:
        continue
      
      # Skip over models already in FB
      if model in existing_blobs:
        print(model, "already in existing_blobs")

      else:
        file_path = os.path.join(base_path, brand, board, model).replace("\\", '/')
        blob = bucket.blob(model)
        blob.upload_from_filename(file_path)
        print(f"File {file_path} uploaded to gs://{bucket.name}/{model}")
