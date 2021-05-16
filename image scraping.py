import os
import selenium
from selenium import webdriver
import time
from PIL import Image  #python Imaging Library is a free and open-source additional
# library for the Python programming language that adds support for opening, manipulating,
# and saving many different image file formats
import io
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException

driver = webdriver.Chrome(ChromeDriverManager().install())

#Specify Search URL
search_url="https://www.google.com/search?q={q}&tbm=isch&tbs=sur%3Afc&hl=en&ved=0CAIQpwVqFwoTCKCa1c6s4-oCFQAAAAAdAAAAABAC&biw=1251&bih=568"

driver.get(search_url.format(q='Car'))

#Scroll to the end of the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)#sleep_between_interactions, to avoid problem because we are reading a page which is not loaded
imgResults = driver.find_elements_by_xpath("//img[contains(@class,'rg_i Q4LuWd')]")  ### gets all images from that page
totalResults=len(imgResults)
# print(totalResults)

#Click on each Image to extract its corresponding link to download

img_urls = set()
for i in  range(0,len(imgResults)):
    img=imgResults[i]
    try:
        img.click()
        time.sleep(2)
        actual_images = driver.find_elements_by_css_selector('img.n3VNCb')
        for actual_image in actual_images:
            if actual_image.get_attribute('src') and 'https' in actual_image.get_attribute('src'):
                img_urls.add(actual_image.get_attribute('src'))
    except ElementClickInterceptedException or ElementNotInteractableException as err:
        print(err)

os.chdir('C:/Users/imsom/PycharmProjects/webscrap/virat')
baseDir=os.getcwd()

for i, url in enumerate(img_urls):
    file_name = f"{i:150}.jpg"
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - COULD NOT DOWNLOAD {url} - {e}")

try:
    image_file = io.BytesIO(image_content)
    image = Image.open(image_file).convert('RGB')

    file_path = os.path.join(baseDir, file_name)

    with open(file_path, 'wb') as f:
        image.save(f, "JPEG", quality=85)
    print(f"SAVED - {url} - AT: {file_path}")
except Exception as e:
    print(f"ERROR - COULD NOT SAVE {url} - {e}")