import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_place_names(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    driver.get(url)

    wait = WebDriverWait(driver, 10)
    place_names = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "mw-collection-place-name")))

    place_names = [name.text for name in place_names]

    driver.quit()

    return place_names

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL of the webpage to scrape")
    args = parser.parse_args()

    place_names = get_place_names(args.url)

    with open("place_names.txt", "w") as file:
        file.write("\n".join(place_names))
