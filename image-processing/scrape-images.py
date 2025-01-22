import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re
import json
import os

options = Options()
options.add_argument('--headless')
options.add_argument('--diasble-dev-shm-usage')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options = options)

with open('board-links.json') as json_file:
  data = json.load(json_file)
  base_path = os.path.dirname(os.path.realpath(__file__))

  # board_link = data['arbor'][0]['arbor-a-frame']['link']
  # print(board_link)
  # (board_name, ) = data['arbor'][0]
  # print(board_name)

  for brand, boards in data.items():
    for board_dict in boards:
      for board_name, board_info in board_dict.items():
        board_link = board_info['link']
        # print(board_link)
        driver.get(board_link)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        print(brand + ":", board_name)

        board_image = soup.find('img', class_ = 'active')['src']

        response = requests.get(board_image)

        file_name = f"{board_name}.png"
        folder_name = brand

        if not os.path.isdir(os.path.join(base_path, brand)):
          os.makedirs(os.path.join(base_path, brand))

        folder_name = board_name

        if not os.path.exists(os.path.join(base_path, brand, folder_name)):
          os.makedirs(os.path.join(base_path, brand, folder_name))

        with open(os.path.join(base_path, brand, folder_name, file_name), 'wb') as f:
          f.write(response.content)



  # driver.get(board_link)
  # time.sleep(3)

  # soup = BeautifulSoup(driver.page_source, 'html.parser')

  # # (board_name, ) = data['arbor'][0]
  # board_name = 'arbor-a-frame'
  
  # board_image = soup.find('img', class_ = 'active')['src']

  # response = requests.get(board_image)

  # file_name = f"{board_name}.png"
  # folder_name = board_name
  # if not os.path.exists(os.path.join(base_path, folder_name)):
  #   os.makedirs(os.path.join(base_path, folder_name))
  # with open(os.path.join(base_path, folder_name, file_name), 'wb') as f:
  #   f.write(response.content)
  

  


