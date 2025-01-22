import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
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

  if not os.path.join(os.path.join(base_path, 'boards')):
    os.makedirs(os.path.join(base_path, 'boards'))

  for brand, boards in data.items():
    for board_dict in boards:
      for board_name, board_info in board_dict.items():

        board_link = board_info['link']
        driver.get(board_link)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        board_image = soup.find('img', class_ = 'active')['src']

        response = requests.get(board_image)

        file_name = f"{board_name}.png"
        folder_name = brand

        if not os.path.isdir(os.path.join(base_path, 'boards', brand)):
          os.makedirs(os.path.join(base_path, 'boards', brand))

        folder_name = board_name

        if not os.path.exists(os.path.join(base_path, 'boards', brand, folder_name)):
          os.makedirs(os.path.join(base_path, 'boards', brand, folder_name))

        with open(os.path.join(base_path, 'boards', brand, folder_name, file_name), 'wb') as f:
          f.write(response.content)

driver.quit()