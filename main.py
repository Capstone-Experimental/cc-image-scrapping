import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def scrape_images(query, num_images):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(f"https://www.google.com/search?tbm=isch&q={query.replace(' ', '+')}")

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    image_urls = driver.execute_script("""
        const images = document.querySelectorAll('.rg_i.Q4LuWd');
        let urls = [];
        images.forEach(img => {
            if (img.hasAttribute('data-src') && img.getAttribute('data-src').startsWith('http')) {
                urls.push(img.getAttribute('data-src'));
            } else if (img.hasAttribute('src') && img.getAttribute('src').startsWith('http')) {
                urls.push(img.getAttribute('src'));
            }
        });
        return urls;
    """)

    os.makedirs("downloaded_images", exist_ok=True)
    for idx, url in enumerate(image_urls[:num_images]):
        response = requests.get(url)
        with open(f"downloaded_images/{query}_{idx}.jpg", "wb") as f:
            f.write(response.content)

    driver.quit()

scrape_images("burung gagak", 3)
