# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from selWhats_library.WhatSend import WhatSend

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    chrome_path = r'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    chrome_profile_path = r'C:\\Users\\kevin\\AppData\\Local\\Google\\Chrome\\User Data\\'
    whatsapp = WhatSend(chrome_path, chrome_profile_path)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
