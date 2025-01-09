import logging
import time
import timeit

import colored_log
import Elements
import WebDriver
from selWhats_library.WebDriver import WebElement


class WhatSend:
    LINK = "https://web.whatsapp.com"
    webDriver = None
    log = colored_log.getLogger(__name__, level=logging.DEBUG)

    def __init__(self, chrome_path: str, chrome_profile_path: str):
        self.webDriver = WebDriver.getWebDriver(chrome_path, chrome_profile_path)
        self.webDriver.startDriver(self.LINK)
        time.sleep(5)

    def __del__(self):
        if self.webDriver:
            self.webDriver.stopDriver()

    def sendMessageToNewChat(self, number: str, message: str) -> bool:

        self.clickElement(Elements.NEW_CHAT_ELEMENT)
        return self.sendMessage(Elements.NUMBER_BOX, Elements.NEW_CHAT, number, message, Elements.HEADER_BACK)

    def sendMessageToContact(self, name: str, message: str) -> bool:

        return self.sendMessage(Elements.CONTACT_BOX, f'//*[@title="{name}"]', name, message)

    def sendMessage(self, search_box_path: str, chat_path: str, name: str, message: str, press_back=None) -> bool:
        self.typeText(search_box_path, name)
        time.sleep(0.1)

        if not self.findChat(chat_path, name):
            if press_back:
                self.clickElement(press_back)
            return False

        return self.sendText(message)

    def sendText(self, message: str) -> bool:
        message_box = self.getWebElement(Elements.MESSAGE_BOX)
        self.typeText(Elements.MESSAGE_BOX, message)
        self.webDriver.pressEnter(message_box)
        time.sleep(0.1)
        return True

    def typeText(self, path: str, text: str):
        self.webDriver.sendText(path, text)

    def clickElement(self, path: str, timeout=10):
        self.webDriver.clickElement(path, timeout=timeout)

    def getWebElement(self, path: str, timeout=20) -> WebElement:
        return self.webDriver.wait_for_element(path, timeout=timeout)

    def findChat(self, path: str, name: str) -> bool:
        self.log.debug(path)
        try:
            self.clickElement(path, timeout=2)
            self.log.debug(f'Chat Found for {name}')
            return True
        except TimeoutError as _:
            self.log.warning(f"Chat Not Found for: {name}")
            return False

    def testTime(self, number=1):
        def send_message():
            self.sendMessageToNewChat("9082974811", "Test new Chat")
            # self.sendMessageToContact("Kevin Dedhia", "Test Contact")

        execution_time = timeit.timeit(send_message, number=number)
        print(f"Execution time: {execution_time} seconds")


if __name__ == '__main__':
    chrome_path1 = r'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    chrome_profile_path1 = r'C:\\Users\\kevin\\AppData\\Local\\Google\\Chrome\\User Data\\'
    whatsapp = WhatSend(chrome_path1, chrome_profile_path1)
    time.sleep(5)
    whatsapp.testTime(10)
