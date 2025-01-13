import logging
import os
import time
import pyperclip
import requests
import subprocess

from selWhats_library import colored_log

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.file_detector import LocalFileDetector
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebDriverError(Exception):
    """Custom exception for WebDriver-related errors."""
    pass


class WebDriver:
    log = colored_log.getLogger(__name__, level=logging.INFO)
    chrome_path = None
    chrome_profile_path = None
    web_driver = None

    def __init__(self, chrome_path=chrome_path, chrome_profile_path=chrome_profile_path):

        if not os.path.exists(chrome_profile_path):
            self.log.error(f"Chrome profile path not found: {chrome_profile_path}. Enter Path For Chrome Profile")
            raise WebDriverError(f"Chrome profile path not found: {chrome_profile_path}. Enter Path For Chrome Profile")

        if not os.path.exists(chrome_path):
            self.log.error(f"Chrome.exe path not found: {chrome_path}. Enter Path For Chrome.exe Profile")
            raise WebDriverError(f"Chrome.exe path not found: {chrome_path}. Enter Path For Chrome.exe Profile")

        self.chrome_path = chrome_path
        self.chrome_profile_path = chrome_profile_path

        self.log.info(f"Starting Chrome with Profile : {chrome_profile_path.split('\\')[-1]}")

    def startDriver(self, link: str) -> webdriver:
        self.log.info("Starting Driver")
        self.checkConnection()
        options = self.getChromeOptions()
        self.web_driver = webdriver.Chrome(options=options)
        self.web_driver.get(link)
        return self.web_driver

    def getChromeOptions(self):
        options = webdriver.ChromeOptions()
        options.add_argument(f'--user-data-dir={self.chrome_profile_path}')
        options.add_argument(f'--remote-debugging-port=9222')
        options.add_experimental_option("debuggerAddress", "localhost:9222")
        options.add_argument(f'--profile-directory=Default')
        return options

    def clickElement(self, path, timeout=10):
        for _ in range(3):
            try:
                self.wait_for_element(path, timeout=timeout).click()
                return
            except Exception as e:
                self.log.warning(e)
                time.sleep(0.5)
        self.log.error(f"Cannot Click {path}")

    def stopDriver(self):
        if self.web_driver:
            self.log.info("Stopping Driver")
            self.web_driver.quit()
            self.web_driver = self.web_driver.quit()

    def wait_for_element(self, xpath: str, timeout=20) -> WebElement:
        waitTime = 0
        backoff_time = 0.05  # Initial wait time in seconds
        attempt = 0
        while attempt < 1:
            try:
                return WebDriverWait(self.web_driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            except Exception as _:
                time.sleep(backoff_time)
                waitTime += backoff_time + timeout
                backoff_time *= 2  # Exponential backoff
                attempt += 1
        waitTime = timeout * 3 + 3.5
        self.log.debug(f"Element with xpath '{xpath}' not clickable after {waitTime} seconds.")
        raise TimeoutError(f"Element with xpath '{xpath}' not clickable after {waitTime} seconds.")

    def checkConnection(self):
        try:
            requests.get("http://localhost:9222")
            self.log.debug("Chrome is Active")
            return
        except requests.exceptions.ConnectionError as ec:

            self.log.warning("No Active Session Found. Starting new Session")

            subprocess.call(["taskkill", "/F", "/IM", "chrome.exe"])
            subprocess.Popen([self.chrome_path,
                              f'--remote-debugging-port=9222',
                              f'--user-data-dir={self.chrome_profile_path}'])
            time.sleep(1)
            attempt = 0
            while attempt < 3:
                try:
                    requests.get("http://localhost:9222")
                    self.log.debug("New Session Started Successfully")
                    return
                except Exception as e:
                    time.sleep(0.5)
                    self.log.error(e)

            raise WebDriverError(f"Failed to establish connection with Chrome. {ec.__cause__}")

        except Exception as e:
            self.log.error(e.__cause__)
            raise WebDriverError(f"Failed to establish connection with Chrome. {e.__cause__}")

    def sendText(self, path: str, text: str):
        try:
            web_element = self.wait_for_element(path)
            pyperclip.copy(text)
            web_element.click()
            act = ActionChains(self.web_driver)
            act.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
            act.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
        except Exception as e:
            self.log.error(f"Failed to send text: {e}")
            raise WebDriverError(f"Failed to send text: {e}")

    def attachFile(self, elementPath: str, filePath: str):
        self.web_driver.file_detector = LocalFileDetector()
        files = filePath.split(" ")
        fileInput = self.web_driver.find_element(By.XPATH, elementPath)
        for file in files:
            self.log.DEBUG(file)
            fileInput.send_keys(file)
            time.sleep(0.5)
            fileInput = self.web_driver.find_element(By.XPATH, '//input[@accept="*"]')
            time.sleep(0.5)

    def pressEnter(self, web_element: WebElement):
        web_element.send_keys(Keys.ENTER)

    def __del__(self):
        if self.web_driver:
            self.stopDriver()


def getWebDriver(chrome_path: str, chrome_profile_path: str) -> WebDriver:
    return WebDriver(chrome_path, chrome_profile_path)
