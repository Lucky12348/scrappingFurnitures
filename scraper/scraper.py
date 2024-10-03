import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

extension_path = os.path.join(os.getcwd(), 'utils/imagebatcher.crx')

def setup_category_directory(category_name):
    base_path = os.path.join(os.getcwd(), 'categories', category_name)
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    return base_path

def handle_cookies(driver):
    try:
        wait = WebDriverWait(driver, 10)
        accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Tout accepter']")))
        accept_button.click()
        print("Cookies acceptés")
    except Exception as e:
        print(f"Erreur lors de l'acceptation des cookies : {str(e)}")

def scrape_images_for_category(category_name):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_extension(extension_path)
    
    download_folder = setup_category_directory(category_name)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    search_url = f"https://www.google.com/imghp?hl=fr"
    driver.get(search_url)

    handle_cookies(driver)

    try:
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(EC.element_to_be_clickable((By.NAME, "q")))
    except Exception as e:
        print(f"Erreur : {str(e)}")
        driver.quit()
        return

    search_box.send_keys(category_name)
    search_box.send_keys(Keys.RETURN)

    time.sleep(2)

    for _ in range(3):
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        time.sleep(2)

    print("Téléchargement des images via l'extension...")
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('chrome://extensions')
    
    driver.quit()

if __name__ == "__main__":
    categories = ["Chaise", "Table", "Canapé"]
    
    for category in categories:
        print(f"Scraping pour la catégorie : {category}")
        scrape_images_for_category(category)
        print(f"Terminé pour la catégorie : {category}")
