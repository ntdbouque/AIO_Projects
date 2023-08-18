import os
import time

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

root_dir = './vn_news_corpus'
os.makedirs(root_dir, exist_ok = True)
n_pages = 2
article_id = 0
news_page_urls = []


for page_idx in range(n_pages):
    main_url = f'https://vietnamnet.vn/thoi-su-page{page_idx}'
    driver.get(main_url)

    news_lst_xpath = '//div[@class="topStory-15nd"]/div/div[1]/a'
    news_tags = driver.find_elements(
        By.XPATH, 
        news_lst_xpath
    )

    news_page_urls = [
        news_tag.get_attribute('href') \
            for news_tag in news_tags
    ]

    for news_page_url in news_page_urls:
        driver.get(news_page_url)
        time.sleep(1)

        main_content_xpath = '//div[@class = "content-detail content-mobile-change"]'
        try:
            main_content_tag = driver.find_element(By.XPATH, main_content_xpath)

        except:
            continue
    
        video_content_xpath = '//div[@class="video-detail"]'
        try:
            video_content_tag = main_content_tag.find_element(
                By.XPATH,
                video_content_xpath
            )
            continue
        except:
            pass
    
        title = main_content_tag.find_element(
            By.TAG_NAME,
            'h1'
        ).text.strip()

        abstract = main_content_tag.find_element(
            By.TAG_NAME,
            'h2'
        ).text.strip()
    
        try:
            author_xpath = '//span[@class="name"]'
            author = main_content_tag.find_element(
                By.XPATH,
                author_xpath
            ).text.strip()
        except:
            author = ''

        paragraphs_xpath = '//div[@class="maincontent main-content"]/p'
        paragraphs_tags = main_content_tag.find_elements(
            By.XPATH,
            paragraphs_xpath
        )
        
        paragraphs_lst = [
            paragraphs_tag.text.strip() \
                for paragraphs_tag in paragraphs_tags
        ]
        paragraphs = ' '.join(paragraphs_lst)


        final_content_lst = [title, abstract, paragraphs, author]
        final_content = '\n\n'.join(final_content_lst)

        article_filename = f'article_{article_id:05d}.txt'
        article_savepath = os.path.join(
            root_dir,
            article_filename
        )

        article_id += 1
        with open(article_savepath, 'w') as f:
            f.write(final_content)

        driver.back()
    

