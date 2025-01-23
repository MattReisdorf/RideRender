import os

from PIL import Image
import cv2

def split_images(board_image_path: str, board: str, image: str):
  img = Image.open(os.path.join(board_image_path, image))
  width, height = img.size
  top_graphic = img.crop((width // 2, 0, width, height))
  bottom_graphic = img.crop((0, 0, width // 2, height))
  top_graphic.save(os.path.join(board_image_path, f"{board}-top.png"))
  bottom_graphic.save(os.path.join(board_image_path, f"{board}-bottom.png"))

def crop_image(board_image_path: str, image: str):
  img = cv2.imread(os.path.join(board_image_path, image))
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
  morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)
  cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
  cnt = sorted(cnts, key = cv2.contourArea)[-1]
  x, y, w, h = cv2.boundingRect(cnt)
  dst = img[y: y + h, x: x + w]
  cv2.imwrite(os.path.join(board_image_path, image), dst)

base_path = os.path.dirname(os.path.realpath(__file__))
all_brands_path = os.path.join(base_path, 'boards')

for brand in os.listdir(all_brands_path):
  brand_path = os.path.join(all_brands_path, brand)

  for board in os.listdir(brand_path):
    board_path = os.path.join(brand_path, board)

    for image in os.listdir(board_path):
      board_image_path = os.path.join(board_path)
      if 'top' in image:
        crop_image(board_path, image)
      elif 'bottom' in image:
        crop_image(board_path, image)
      else: continue