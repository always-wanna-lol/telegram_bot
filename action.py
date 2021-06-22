from selenium import webdriver
import googletrans
from selenium.webdriver.common.keys import Keys
import requests
from googletrans import Translator

import time

import auth




class Parsing_Post_Bot():

    def __init__(self, username, password):
        self.username = auth.username
        self.password = auth.password
        self.browser = webdriver.Chrome()

    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def login(self):
        browser = self.browser

        browser.get("https://www.instagram.com")
        time.sleep(1)

        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(self.username)

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(self.password)

        password_input.send_keys(Keys.ENTER)

        time.sleep(3)

    def download(self, url):
        browser = self.browser
        browser.get(url)

        time.sleep(2)
        try:
            button = browser.find_element_by_class_name('_6CZji   ')
        except Exception:
            print("Кнопки нет!")

        i=0
        downloaded = []
        while True:
            i += 1
            try:
                img_src_url = browser.find_element_by_class_name('FFVAD').get_attribute("src")
                if img_src_url not in downloaded:
                    get_img = requests.get(img_src_url)
                    #with open(f"files/{i}_img.jpg", 'wb') as img_file:
                    #    img_file.write(get_img.content)
                    #    print(f"Фото {i} успешо скачано")
                    downloaded.append(img_src_url)
                    time.sleep(1)
            except Exception:
                print("Это не фото!")
            try:
                video_src_url = browser.find_element_by_class_name('tWeCl').get_attribute("src")
                if video_src_url not in downloaded:
                    get_video = requests.get(video_src_url, stream = True)
                    #with open(f"files/{i}_video.mp4", "wb") as video_file:
                    #    for chunk in get_video.iter_content(chunk_size=1024*1024):
                    #        if chunk:
                    #            video_file.write(chunk)
                    #    print("Видео успешно скачано!")
                    downloaded.append(video_src_url)
                    time.sleep(1)
            except Exception:
                print("Это не видео!")
            try:
                button.click()
                time.sleep(2)
            except Exception:
                break

        time.sleep(2)
        self.close_browser()

        return downloaded

    def descriotion(self, url):
        browser = self.browser
        browser.get(url)

        descriotion_xpath = '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span'
        description_text = browser.find_element_by_xpath(descriotion_xpath).get_attribute('textContent')

        translator = Translator()
        result = translator.translate(description_text, dest='ru')
        
        self.close_browser()

        return result.text


#my_bot = Parsing_Post_Bot(auth.username, auth.password)
#my_bot.login()
#my_bot.download('https://www.instagram.com/p/CQWLBOzH_HU/?utm_source=ig_web_copy_link')
#my_bot.descriotion('https://www.instagram.com/p/COijjfpHXfd/?utm_source=ig_web_copy_link')