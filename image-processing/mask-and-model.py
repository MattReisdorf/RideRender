import os
import cv2
import numpy as np


def generate_mask(board_path: str, board: str, image: str):
  # Read Image
  img = cv2.imread(os.path.join(board_path, image))

  # Convert to Grayscale
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  # Apply Gaussian Blue
  blurred = cv2.GaussianBlur(gray, (5, 5), 0)

  # Thresholding
  # mask = cv2.adaptiveThreshold(
  #   blurred,
  #   255,
  #   cv2.ADAPTIVE_THRESH_MEAN_C,
  #   cv2.THRESH_BINARY_INV,
  #   11,
  #   2
  # )

  _, mask = cv2.threshold(blurred, 240, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)

  # Define Structuring Element for Opening/Closing
  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
  # Opening Removes Small Noise
  mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
  # Closing Fills Small Holes
  mask_cleaned = cv2.morphologyEx(mask_cleaned, cv2.MORPH_CLOSE, kernel)

  # Find Contours of Cleaned Mask
  contours, _ = cv2.findContours(mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  if contours:
    largest_contour = max(contours, key = cv2.contourArea)

    final_mask = np.zeros_like(mask_cleaned)
    cv2.drawContours(final_mask, [largest_contour], -1, color = 255, thickness = -1)

    if 'top' in image:
      cv2.imwrite(os.path.join(board_path, f"{board}-top-mask.png"), final_mask)
    else:
      cv2.imwrite(os.path.join(board_path, f"{board}-bottom-mask.png"), final_mask)

def generate_masks():
  base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'boards')

  for brand in os.listdir(base_path):
    brand_path = os.path.join(base_path, brand)
    # print(brand_path)
    for board in os.listdir(brand_path):
      board_path = os.path.join(brand_path, board)
      # print(board_path)
      for image in os.listdir(board_path):
        if 'top' in image:
          generate_mask(board_path, board, image)
        elif 'bottom' in image:
          generate_mask(board_path, board, image)
        else: continue

def compare_masks(top_mask_path: str, bottom_mask_path: str) -> str:
  top_mask = cv2.imread(top_mask_path, cv2.IMREAD_GRAYSCALE)
  bottom_mask = cv2.imread(bottom_mask_path, cv2.IMREAD_GRAYSCALE)

  top_area = np.count_nonzero(top_mask)
  bottom_area = np.count_nonzero(bottom_mask)

  if top_area > bottom_area:
    return(top_mask_path)
  elif bottom_area > top_area:
    return(bottom_mask_path)
  else: return top_mask_path

def generate_model(scale: float = 1.0):
  base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'boards')

  for brand in os.listdir(base_path):
    brand_path = os.path.join(base_path, brand)
    # print(brand_path)
    for board in os.listdir(brand_path):
      board_path = os.path.join(brand_path, board)
      # print(board_path)
      masks = []
      for image in os.listdir(board_path):
        if 'top-mask' in image:
          masks.append(os.path.join(board_path, image))
        elif 'bottom-mask' in image:
          masks.append(os.path.join(board_path, image))
        else: continue
      
      # print(len(masks), board)
      print(board)
      mask_path = compare_masks(masks[1], masks[0])
      print(mask_path)
      mask_gray = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
      if mask_gray is None:
        print(mask_path)
        raise FileNotFoundError(f"Could Not Read Image at {mask_path}")
      
      _, mask = cv2.threshold(mask_gray, 127, 255, cv2.THRESH_BINARY)

      contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      if not contours:
        raise ValueError("No Contours Found")
      
      main_contour = max(contours, key = cv2.contourArea)

      pts = main_contour.squeeze(axis = 1)

      with open(os.path.join(board_path, f"{board}.obj"), "w") as f:
        f.write(f"{board}\n")

        for (x, y) in pts:
          f.write(f"v {x * scale:1f} {-y * scale: 1f} 0.0 \n")

        num_vertices = len(pts)
        face_indices = " ".join(str(i + 1) for i in range(num_vertices))
        f.write(f"f {face_indices}\n")
      # # print(board_path, board)

generate_model(scale = 0.01)

# generate_masks()