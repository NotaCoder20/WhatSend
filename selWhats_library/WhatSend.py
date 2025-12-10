import logging
import time
import timeit

from . import colored_log
from . import Elements
from . import WebDriver
from .WebDriver import WebElement


class _WhatSendImpl:
    LINK = "https://web.whatsapp.com"
    webDriver = None
    log = colored_log.getLogger(__name__, level=logging.INFO)

    def __init__(
            self,
            chrome_path: str,
            chrome_profile_path: str,
            log_level: int | None = None,
            logger=None,
            retries: int = 3
    ) -> None:

        # Use user's logger if provided
        if logger:
            self.log = logger
        else:
            # otherwise create one with desired log level (default INFO)
            level = log_level if log_level is not None else colored_log.logging.INFO
            self.log = colored_log.getLogger(__name__, level=level)

        self.webDriver = WebDriver.getWebDriver(chrome_path, chrome_profile_path, retries=retries)
        self.webDriver.startDriver(self.LINK)
        time.sleep(5)

    def __del__(self):
        if self.webDriver:
            self.webDriver.stopDriver()

    def sendMessageToNewChat(self, number: str, message: str, file: str | None = None) -> bool:

        self.clickElement(Elements.NEW_CHAT_ELEMENT)
        return self.sendMessage(Elements.NUMBER_BOX,
                                Elements.NEW_CHAT,
                                number, message,
                                Elements.HEADER_BACK,
                                file=file)

    def sendMessageToContact(self, name: str, message: str, file: str | None = None) -> bool:

        return self.sendMessage(Elements.CONTACT_BOX, f'//*[@title="{name}"]', name, message, file=file)

    def sendMessage(self,
                    search_box_path: str, chat_path: str,
                    name: str, message: str, press_back=None, file: str | None = None) -> bool:
        self.webDriver.sendText(search_box_path, name)
        time.sleep(0.1)

        if not self.findChat(chat_path, name):
            if press_back:
                self.clickElement(press_back)
            return False

        time.sleep(0.5)
        if file:
            self.webDriver.sendText(Elements.MESSAGE_BOX, message)
            self.clickElement(Elements.ATTACH_BNT)
            self.clickElement(Elements.IMG_BNT)
            self.log.debug(file)
            self.webDriver.attachFile(Elements.ATTACH_MULTI_BNT, file)
            time.sleep(0.5)
            self.clickElement(Elements.SEND_BNT)
            return True

        return self.sendText(message)

    def sendText(self, message: str) -> bool:
        message_box = self.webDriver.wait_for_element(Elements.MESSAGE_BOX, timeout=20)
        self.webDriver.sendText(Elements.MESSAGE_BOX, message)
        self.webDriver.pressEnter(message_box)
        time.sleep(0.1)
        return True

    def clickElement(self, path: str, timeout=10):
        self.webDriver.clickElement(path, timeout=timeout)

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
            pass

        execution_time = timeit.timeit(send_message, number=number)
        print(f"Execution time: {execution_time} seconds")


# -------------------------------------------------
# PUBLIC API WRAPPER (EXACT SAME PUBLIC METHOD NAMES)
# -------------------------------------------------
class WhatSend:
    """Public API — exposes ONLY the constructor and two main methods."""

    def __init__(
            self,
            chrome_path: str,
            chrome_profile_path: str,
            log_level: int | None = None,
            logger=None,
            retries: int = 3
    ) -> None:

        self._impl = _WhatSendImpl(
            chrome_path,
            chrome_profile_path,
            log_level=log_level,
            logger=logger,
            retries=retries,
        )

    # ---- EXPOSE ONLY THESE EXACT TWO METHODS ----
    def sendMessageToNewChat(self, number: str, message: str, file: str | None = None) -> bool:
        return self._impl.sendMessageToNewChat(number, message, file=file)

    def sendMessageToContact(self, name: str, message: str, file: str | None = None) -> bool:
        return self._impl.sendMessageToContact(name, message, file=file)

    def __del__(self):
        try:
            del self._impl
        except Exception:
            pass


__all__ = ["WhatSend"]

if __name__ == '__main__':
    pass
