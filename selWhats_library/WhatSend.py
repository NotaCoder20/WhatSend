import logging
import time
import timeit

from selWhats_library import Elements, colored_log, WebDriver
from selWhats_library.WebDriver import WebDriver, WebElement


class WhatSend:
    LINK = "https://web.whatsapp.com"
    webDriver = None
    log = colored_log.getLogger(__name__, level=logging.DEBUG)

    def __init__(self, chrome_path, chrome_profile_path):
        self.webDriver = WebDriver(chrome_path, chrome_profile_path)
        self.webDriver.startDriver(self.LINK)
        time.sleep(5)

    def __del__(self):
        if self.webDriver:
            self.webDriver.stopDriver()

    def sendMessageToNewChat(self, number: str, message: str) -> bool:

        new_chat_button = self.getWebElement(Elements.NEW_CHAT_ELEMENT)
        new_chat_button.click()
        time.sleep(0.5)

        number_box = self.getWebElement(Elements.NUMBER_BOX)
        number_box.click()
        self.webDriver.sendText(number_box, number)
        self.webDriver.pressEnter(number_box)
        time.sleep(0.7)

        try:
            self.getWebElement(Elements.NO_CHAT_FOUND, 1)
            self.log.warning(f"No Chat Found for: {number}")
            self.getWebElement(Elements.HEADER_BACK).click()
            return False
        except TimeoutError as _:
            self.log.debug(f"Chat Found for: {number}")
            pass

        message_box = self.getWebElement(Elements.MESSAGE_BOX)
        self.webDriver.sendText(message_box, message)
        self.webDriver.pressEnter(message_box)
        time.sleep(0.5)

        return True

    def getWebElement(self, path: str, timeout=20) -> WebElement:
        return self.webDriver.wait_for_element(path, timeout=timeout)

    def testTime(self, number=1):
        # Create a wrapper function for the method to be timed
        def send_message():
            self.sendMessageToNewChat("9082974811", "Hey")

        execution_time = timeit.timeit(send_message, number=number)
        print(f"Execution time: {execution_time} seconds")


if __name__ == '__main__':
    chrome_path1 = r'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    chrome_profile_path1 = r'C:\\Users\\kevin\\AppData\\Local\\Google\\Chrome\\User Data\\'
    whatsapp = WhatSend(chrome_path1, chrome_profile_path1)
    time.sleep(5)
    # whatsapp.sendMessageToNewChat("9082974811", "Hii")
    # whatsapp.sendMessageToNewChat("9082974812", "Hii")
    # whatsapp.sendMessageToNewChat("9082974811", "Hii")
    # whatsapp.sendMessageToNewChat("9082974812", "Hii")
    # whatsapp.sendMessageToNewChat("9082974811", "Hii")
    # whatsapp.sendMessageToNewChat("9082974812", "Hii")
    whatsapp.testTime(10)
