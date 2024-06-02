from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import time


class ChatGPT:
    def __init__(self, initial_prompt=None):
        url = "https://chatgpt.com/"

        self.driver = self.open_browser(url)
        self.send_message(initial_prompt)

    def send_message(self, message):
        if message is None:
            return

        text_area = self.get_text_area()
        time.sleep(0.1)
        if len(message) > 1000:
            for i in range(0, len(message), 500):
                text_area.send_keys(message[i : i + 500])
        else:
            text_area.send_keys(message)
        time.sleep(0.1)
        button = self.get_button()
        time.sleep(0.1)
        button.click()
        time.sleep(0.1)

    def get_response(self):
        WebDriverWait(self.driver, 30).until_not(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[aria-label="Stop generating"]')
            )
        )
        time.sleep(0.1)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="send-button"]')
            )
        )

        responseDiv = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    '[data-testid^="conversation-turn-"][data-scroll-anchor="true"]',
                )
            )
        )

        responseText = responseDiv.find_element(By.CSS_SELECTOR, ".markdown")
        return responseText.text

    def get_text_area(self):
        return WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "prompt-textarea"))
        )

    def get_button(self):
        return WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="send-button"]'))
        )

    def get_initial_prompt(self, file):
        with open(file, "r") as file:
            return file.read()

    def set_page_title(self, name):
        self.driver.execute_script(f'document.title = "{name}"')

    def quit(self):
        self.driver.quit()

    def open_browser(self, url):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        geckodriver_path = "/snap/bin/geckodriver"
        driver_service = Service(executable_path=geckodriver_path)

        driver = webdriver.Firefox(options=options, service=driver_service)
        driver.get(url)

        return driver
