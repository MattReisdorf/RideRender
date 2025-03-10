from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import re
import json

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options = options)

# Regex Function Replacement -> Clean URLs for Board Names
pattern = re.compile(r'^.*/(?P<base>.+)-snowboard(?:-(?P<year>\d+))?$')
def clean_url(url: str) -> str:
  match = pattern.match(url)
  if match:
    base = match.group('base')
    year = match.group('year')

    if year:
      return f"{base}-{year}"
    else:
      return base
    
  else:
    return url

# Scrape Step 1:
# Get All Brand Names Sold From SideBar Selection Menu
def get_brand_names(url: str):
  driver.get(url)
  time.sleep(3)

  soup = BeautifulSoup(driver.page_source, 'html.parser')

  fieldset = soup.find('fieldset', id = 'sidebar_facets_2__facet-brand')
  ul = fieldset.findChild('ul', class_ = 'facet-list')
  li = ul.findChildren('li', class_ = 'facet-value-li')

  # Initialize Empty Dict for Brands and Brand-Filtered Results Page
  brand_links = {}

  for i in li:
    a = i.find('a', class_ = 'results-link')
    brand = a.get('aria-label')
    # Clean Brand Names with Regex
    step1 = re.sub(r"\.", "", brand)
    step2 = re.sub(r"\s+", "-", step1)
    # Add Brand: URL to Dict
    brand_links[step2.lower()] = f"https://www.evo.com/shop/snowboard/snowboards/{step2.lower()}/mens/condition_new/s_name/rpp_400"

  # Call Step 2
  get_board_links(brand_links)


# Scrape Step 2:
# Get All Boards From Each Brand and the Page URLs
def get_board_links(brand_links: dict):
  # Initialize Empty Dict for Boards

  # Iterate through Brand: URL Dict -> Add Child Dicts with Board Names and Product URLs
  for key, value in brand_links.items():
    driver.get(value)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    links = soup.find_all('a', class_ = 'js-product-thumb-details-link')

    link_array = []
    for link in links:
      if 'snowboards' not in link.get('href'):
        continue
      elif 'blem' in link.get('href'):
        continue

      full_link = "https://evo.com" + link.get('href')
      # Use Clean URL Regex Function to Get Cleaned Board Names
      board_name = clean_url(full_link)
      link_array.append(
        {
          board_name: {
            "name": board_name,
            "link": full_link
          }
        }
      )

    # Add SubDicts to Main Dict
    board_links[key] = link_array

  

# Scrape Step 3:
# Get Info On Each Board: X Sizes, Camber/Rocker/?, Flex, Binding Compat, X Price
def get_board_info(board_links: dict):
  for brand, boards in board_links.items():
    for board_dict in boards:
      print(board_dict)
      for board_name, board_info in board_dict.items():
        driver.get(board_info["link"])

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        lengths = soup.find_all('li', class_ = 'js-selection-matrix-option-container')

        board_lengths = []

        for length in lengths:
          lengthChild = length.findChild('input', class_ = 'js-selection-matrix-option')
          aaa = lengthChild.get('value')
          board_lengths.append(aaa)
        board_info['sizes'] = board_lengths

        price = soup.find('span', class_ = 'pdp-price-regular') or soup.find('span', class_ = 'pdp-price-discount')
        board_info['price'] = price.getText()


        specs_parent = soup.find('section', class_ = 'pdp-specs')
        specs = specs_parent.find('ul', class_ = 'pdp-spec-list')
        specs_list = specs.findChildren('li', class_ = 'pdp-spec-list-item')
        wanted_specs = ["Terrain:", "Ability Level:", "Rocker Type:", "Shape:", "Flex Rating:", "Binding Mount Pattern:"]
        for spec in specs_list:
          key = spec.find('span', class_ = 'pdp-spec-list-title')
          value = spec.find('span', class_ = 'pdp-spec-list-description')

          if key.getText() not in wanted_specs:
            continue

          board_info[key.getText()] = value.getText()
      
  # Writes out Final as JSON
  with open('board-info.json', 'w') as f:
    json.dump(board_links, f, indent = 2)


board_links = {}

get_brand_names("https://www.evo.com/shop/snowboard/snowboards/mens/condition_new/s_name/rpp_400")
get_board_info(board_links)



driver.quit()