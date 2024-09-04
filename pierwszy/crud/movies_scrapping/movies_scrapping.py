from selenium.webdriver.chrome.options import ChromiumOptions as ChromeOptions
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
import time
import json
from .classes import *

options = ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)


def scrap_movies(urls):
    try:

        meta = MetaClass()

        movies_container = MoviesContainer()

        for url in urls:
            driver.get(url)
            if "helios.pl" in url:
                days = driver.find_elements(By.CSS_SELECTOR, '._0s_cSI div')
                for index, day in enumerate(days):
                    driver.execute_script("document.querySelectorAll('._0s_cSI div')[" + str(index) + "].click();")
                    time.sleep(2)
                    elements = driver.find_elements(By.CSS_SELECTOR, '.I1_7g6')
                    for element in elements:
                        header = element.find_element(By.CSS_SELECTOR, '._56_e4l a')
                        title = header.text
                        link = header.get_attribute('href')

                        category = element.find_element(By.CSS_SELECTOR, '.sU_287')
                        category = category.text.replace(",","")
                        categories = category.lower().split(" ")

                        img = element.find_element(By.CSS_SELECTOR, '._8K_RYd source').get_attribute('srcset')

                        datetimes = element.find_elements(By.CSS_SELECTOR, '.tf_DZ7 time')
                        date = datetime.fromisoformat(datetimes[0].get_attribute('datetime')).strftime("%d.%m")

                        hours = []
                        for x in datetimes:
                            hours.append(datetime.fromisoformat(x.get_attribute('datetime')).strftime("%H:%M"))

                        addingMovieHandler(movies_container, meta, title.capitalize(), date, hours, categories, link, img)
            if "kinokameralnecafe.pl" in url:
                time.sleep(2)
                iframe = driver.find_element(By.TAG_NAME, 'iframe')
                driver.switch_to.frame(iframe)

                days = driver.find_elements(By.CSS_SELECTOR, '.btns a')
                for day in range(len(days)):
                    time.sleep(2)
                    elements = driver.find_elements(By.CSS_SELECTOR, '.iframe_all')

                    for element in elements:
                        date = element.find_element(By.CSS_SELECTOR, '.event_icon').text.replace("\n", "")
                        header = element.find_element(By.CSS_SELECTOR, '.event_data a')
                        title = header.text
                        link = header.get_attribute('href')

                        hour = element.find_elements(By.CSS_SELECTOR, '.B-flex--direction-row p')
                        hours = [hour[2].text.replace(" ", "")]

                        img = element.find_element(By.CSS_SELECTOR, '.B-event__poster img').get_attribute('src')

                        addingMovieHandler(movies_container, meta, title.capitalize(), date, hours, ["kinokameralne"], link, img)
                    if day != len(days) - 1:
                        driver.execute_script("document.querySelector('.btns a:last-child').click()")
                driver.switch_to.default_content()
            # if "multikino.pl" in url:
                # print("multikino")
                # for day in range(10):
                #     time.sleep(4)
                #     elements = driver.find_elements(By.CLASS_NAME, "filmlist__item")
                #     for element in elements:
                #         header = element.find_element(By.CSS_SELECTOR, '.filmlist__title')
                #         title = header.text
                #         link = header.get_attribute('href')
                #
                #         categoryDiv = element.find_elements(By.CSS_SELECTOR, '.film-details a')
                #         categories = []
                #         for category in categoryDiv:
                #             categories.append(category.text.lower())
                #
                #         date = element.find_element(By.CLASS_NAME, 'filmlist__dayExpander').text.split(" ")[1]
                #         hoursDiv = element.find_elements(By.CSS_SELECTOR, '.small time')
                #         hours = []
                #         for hour in hoursDiv:
                #             hours.append(hour.text.replace(" ", ""))
                #
                #         addingMovieHandler(movies_container, meta, title.capitalize(), date, hours, categories, link, False)
                #     driver.execute_script("document.querySelector('.timePicker_forw').click();")
        movies_json = json.dumps(movies_container.movies, cls=MoviesContainerEncoder, ensure_ascii=False)
        meta_json = json.dumps(meta, cls=MetaEncoder, ensure_ascii=False)

        driver.quit()
        return json.dumps({"movies": json.loads(movies_json), "meta": json.loads(meta_json)}, ensure_ascii=False)

    except Exception:
        return False

