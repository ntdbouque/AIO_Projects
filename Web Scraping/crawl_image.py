from io import BytesIO
import os
from PIL import Image
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('start-maximumed')
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(
    service = Service(ChromeDriverManager().install()),
    options = chrome_options
)

root_dir = './thumbnailimg_corpus'
os.makedirs(root_dir, exist_ok = True)
n_pages = 1
img_id = 0
news_page_urls = []

for page_idx in range(n_pages):
    main_url = f'https://vietnamnet.vn/thoi-su-page{page_idx}'
    driver.get(main_url)

    imgs_lst_xpath = '//div[@class="topStory-15nd"]/div/div[1]/a/img'
    imgs_tags = driver.find_elements(
        By.XPATH, 
        imgs_lst_xpath
    )

    img_urls = [
        imgs_tag.get_attribute('src') \
            for imgs_tag in imgs_tags
    ]

    for img_url in img_urls:
        img_url_resp = requests.get(img_url)
        
        try:
            img = Image.open(
                BytesIO(img_url_resp.content)
            )
        except:
             continue
        
        if img.mode == 'P':
             img = img.convert('RGB')
            
        img_name = f'IMG_{img_id:05}.png'
        img_save_path = os.path.join(
            root_dir,
            img_name
        )

        img.save(img_save_path)
        img_id +=1
        
    
        

    

