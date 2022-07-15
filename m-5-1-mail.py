from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
from pymongo import MongoClient
from pprint import pprint


def parse_url(driver, link_list):
    link_1 = driver.find_element(By.XPATH, "//div[@class='letter-list__react']//div[@aria-label= 'grid']")

    elems = driver.find_elements(By.XPATH, "//div[@class='letter-list__react']//div[@aria-label= 'grid']//a")
    print(len(elems))
    for elem in elems:
        try:
            link_0 = elem.get_attribute('href')
            if 'e.mail.ru' in link_0:
                if link_0 not in link_list:
                    link_list.append(link_0)
                    link_7 = link_0[17:]
                    date_ = driver.find_element(By.XPATH, "//a[contains(@href, '" + link_7 + "')]/div[4]/div/div[5]")
                    from_ = driver.find_element(By.XPATH,
                                                "//a[contains(@href, '" + link_7 + "')]/div[4]/div[1]/div[1]/span")
                    subj_ = driver.find_element(By.XPATH,
                                                "//a[contains(@href, '" + link_7 + "')]/div[4]/div[1]/div[3]/span[1]//span")
                    text_ = driver.find_element(By.XPATH,
                                                "//a[contains(@href, '" + link_7 + "')]/div[4]/div[1]/div[3]/span[2]/div/span")
                    hash_id = hash(link_0)
                    mail_dic = {'_id': hash_id,
                                'From': from_.text,
                                'Data': date_.text,
                                'Subj': subj_.text,
                                'Text': text_.text}
                    pprint(mail_dic)
                    save_to_base(mail_dic)
                # else:
                    # print('DABL')

        except:
            pass
            # print('Ошибка в извлечении URL')

    flag = True
    while flag:
        flag = False
        for y in range(28):
            link_1.send_keys(Keys.ARROW_DOWN)
        elems = driver.find_elements(By.XPATH, "//div[@class='letter-list__react']//div[@aria-label= 'grid']//a")
        print(len(elems))
        for elem in elems:
            try:
                link_0 = elem.get_attribute('href')
                if 'e.mail.ru' in link_0:
                    if link_0 not in link_list:
                        link_list.append(link_0)
                        link_7 = link_0[17:]
                        date_ = driver.find_element(By.XPATH,
                                                    "//a[contains(@href, '" + link_7 + "')]/div[4]/div/div[5]")
                        from_ = driver.find_element(By.XPATH,
                                                    "//a[contains(@href, '" + link_7 + "')]/div[4]/div[1]/div[1]/span")
                        subj_ = driver.find_element(By.XPATH,
                                                    "//a[contains(@href, '" + link_7 + "')]/div[4]/div[1]/div[3]/span[1]//span")
                        text_ = driver.find_element(By.XPATH,
                                                    "//a[contains(@href, '" + link_7 + "')]/div[4]/div[1]/div[3]/span[2]/div/span")
                        hash_id = hash(link_0)
                        mail_dic = {'_id': hash_id,
                                    'From': from_.text,
                                    'Data': date_.text,
                                    'Subj': subj_.text,
                                    'Text': text_.text}
                        pprint(mail_dic)
                        save_to_base(mail_dic)
                        flag = True
            except:
                pass
    print(len(link_list))


def save_to_base(mail_dic):
    try:
        mail.insert_one(mail_dic)
    except:
        pass


if __name__ == '__main__':
    client = MongoClient('127.0.0.1', 27017)
    db = client['base220715']
    mail = db.mailru

    s = Service('./chromedriver')
    driver = webdriver.Chrome(service=s)
    driver.get('https://account.mail.ru/login')
    login = driver.find_element(By.NAME, 'username')
    login.send_keys("study.ai_172@mail.ru")
    login.send_keys(Keys.ENTER)
    time.sleep(1)
    pwd = driver.find_element(By.NAME, 'password')
    pwd.send_keys("NextPassword172#")
    pwd.send_keys(Keys.ENTER)
    time.sleep(4)
    link_list = []

    parse_url(driver, link_list)

    # driver.close()
