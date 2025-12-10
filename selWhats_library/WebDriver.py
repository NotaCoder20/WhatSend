import logging
import os
import time
import pyperclip
import requests
import subprocess

from . import colored_log

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.file_detector import LocalFileDetector
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import win32gui
import win32con


class WebDriverError(Exception):
    """Custom exception for WebDriver-related errors."""
    pass


class WebDriver:
    log = colored_log.getLogger(__name__, level=logging.INFO)
    chrome_path = None
    chrome_profile_path = None
    web_driver = None
    retries = 1

    def __init__(self, chrome_path=chrome_path, chrome_profile_path=chrome_profile_path, retries: int = 1):

        if not os.path.exists(chrome_profile_path):
            self.log.error(f"Chrome profile path not found: {chrome_profile_path}. Enter Path For Chrome Profile")
            raise WebDriverError(f"Chrome profile path not found: {chrome_profile_path}. Enter Path For Chrome Profile")

        if not os.path.exists(chrome_path):
            self.log.error(f"Chrome.exe path not found: {chrome_path}. Enter Path For Chrome.exe Profile")
            raise WebDriverError(f"Chrome.exe path not found: {chrome_path}. Enter Path For Chrome.exe Profile")

        self.retries = retries
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
        try:
            print("Time Start")
            element = self.wait_for_element(path, timeout=timeout, attempts=max(self.retries, 3))
            time.sleep(0.2)
            element.click()
            return
        except Exception as e:
            self.log.error(f"Cannot Click {path} for error {e}")
            time.sleep(0.5)

    def stopDriver(self):
        if self.web_driver:
            try:
                self.web_driver.quit()
            except Exception:
                self.log.exception("Error when quitting web driver")
            finally:
                self.web_driver = None

    def wait_for_element(self, xpath: str, timeout=20, attempts: int | None = None) -> WebElement:
        if not getattr(self, "web_driver", None):
            raise WebDriverError("WebDriver not started — call startDriver() or ensure Chrome session is running.")

        waitTime = 0
        backoff_time = 0.05  # Initial wait time in seconds
        attempt = 0
        if attempts is None:
            attempts = getattr(self, "retries", 1)

        while attempt < attempts:
            try:
                return WebDriverWait(self.web_driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            except Exception as _:
                waitTime += timeout
                self.log.warning(f"Element with xpath '{xpath}' not clickable after {waitTime} seconds Attempt : {attempt + 1}.")
                if not (attempts > 1 and attempts == attempt):
                    time.sleep(backoff_time)
                    waitTime += backoff_time
                    backoff_time *= 2  # Exponential backoff
                    attempt += 1

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
        first = True
        i = 0
        for file in files:
            if not first:
                self.clickElement(elementPath)
                print("Attatch button clicked")
            first = False
            time.sleep(0.5)
            self.log.info(f"Attatching files {i}")
            self.attachFileUI(file)
            i += 1
            time.sleep(0.5)


    def attachFileUI(self, filePath: str):
        hdlg = 0
        while hdlg == 0:
            hdlg = win32gui.FindWindow(None, "Open")

        time.sleep(1)
        hwnd = win32gui.FindWindowEx(hdlg, 0, 'ComboBoxEx32', None)
        hwnd = win32gui.FindWindowEx(hwnd, 0, 'ComboBox', None)
        hwnd = win32gui.FindWindowEx(hwnd, 0, 'Edit', None)
        win32gui.SendMessage(hwnd, win32con.WM_SETTEXT, None, filePath)

        hwnd = win32gui.FindWindowEx(hdlg, 0, 'Button', '&Open')

        win32gui.SendMessage(hwnd, win32con.BM_CLICK, None, None)


    def pressEnter(self, web_element: WebElement):
        web_element.send_keys(Keys.ENTER)

    def __del__(self):
        if self.web_driver:
            self.stopDriver()


def getWebDriver(chrome_path: str, chrome_profile_path: str, retries: int = 1) -> WebDriver:
    return WebDriver(chrome_path, chrome_profile_path, retries=retries)
