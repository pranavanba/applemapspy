import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time

def get_place_names(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    driver.get(url)

    wait = WebDriverWait(driver, 10)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    place_name_elements = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "mw-collection-place-name")))

    place_names = [element.get_attribute("innerText") for element in place_name_elements]

    driver.quit()

    return place_names

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL of the webpage to scrape")
    args = parser.parse_args()

    place_names = get_place_names(args.url)

    place_names = list(set(place_names))

    try:
        with open("place_names.txt", "w") as file:
            file.write("\n".join(place_names))
        print("Place names saved to place_names.txt")
    except IOError:
        print("An error occurred while writing to the file.")
