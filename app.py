from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
import time

app = Flask(__name__)

@app.route("/launch", methods=["POST"])
def launch():
    data = request.json
    pin = data.get("pin")
    name = data.get("name")
    count = int(data.get("count", 1))

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.binary_location = "/usr/bin/google-chrome"

    def bot(index):
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(f"https://kahoot.it/?pin={pin}")
        wait = WebDriverWait(driver, 5)
        try:
            nickname_field = wait.until(EC.presence_of_element_located((By.ID, "nickname")))
            nickname_field.send_keys(f"{name}{index+1}")
            nickname_field.send_keys(Keys.RETURN)
        except Exception as e:
            print(f"Bot {index+1} failed: {e}")
        time.sleep(2)
        driver.quit()

    with ThreadPoolExecutor(max_workers=count) as executor:
        executor.map(bot, range(count))

    return jsonify({"message": f"{count} bots launched!"})
