from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from pymongo import MongoClient
import time
from selenium.webdriver.chrome.options import Options
from pprint import pprint


def parce_url(driver):
    tag_ = driver.find_elements(By.XPATH,
                                   "//h2[contains(text(), 'Самые просматриваемые')]/..//div[@class='product-mini-card__name ng-star-inserted']//a/div")
    price_ = driver.find_elements(By.XPATH,
                                     "//h2[contains(text(), 'Самые просматриваемые')]/..//div[@class='product-mini-card__price ng-star-inserted']//div/span[@class='price__main-value']")
    rating_ = driver.find_elements(By.XPATH,
                                      "//h2[contains(text(), 'Самые просматриваемые')]/..//span[@class='value ng-star-inserted']")
    link_ = driver.find_elements(By.XPATH,
                                    "//h2[contains(text(), 'Самые просматриваемые')]/..//div[@class='product-mini-card__name ng-star-inserted']//a")

    for index_tag in range(len(list(price_))):
        id_ = link_[index_tag].get_attribute('href')[-8:]
        mvideo_dic = {'_id': id_,
                  'Name': tag_[index_tag].text,
                  'Price': price_[index_tag].text,
                  'Rating': rating_[index_tag].text,
                  'URL': link_[index_tag].get_attribute('href')
                      }
        pprint(mvideo_dic)
        save_to_base(mvideo_dic)


def save_to_base(m_dic):
    try:
        mvideo.insert_one(m_dic)
    except:
        pass


if __name__ == '__main__':
    client = MongoClient('127.0.0.1', 27017)
    db = client['base220715']
    mvideo = db.mvideo

    s = Service('./chromedriver')
    chrom_option = Options()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrom_option.add_experimental_option('prefs', prefs)
    chrom_option.add_argument("start-maximized")
    driver = webdriver.Chrome(service=s, chrome_options=chrom_option)
    driver.get('https://www.mvideo.ru')
    time.sleep(1)

    driver.execute_script("window.scrollTo(0, 1200)")
    time.sleep(3)

    parce_url(driver)

    driver.close()


