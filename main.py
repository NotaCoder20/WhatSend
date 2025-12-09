# This is a sample Python script.
import time

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from selWhats_library.WhatSend import WhatSend
import pandas as pd

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def send_messages_from_excel(excel_file):
    global success_cnt, failure_cnt, total, repeated_cnt
    df = pd.read_excel(excel_file)
    phone_set = set()

    if 'Customer Name' not in df.columns or 'Customer Phone' not in df.columns:
        print("The Excel file must contain 'Name' and 'Phone' columns")
        return

    print_hi('PyCharm')
    chrome_path = r'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    chrome_profile_path = r'C:\\Users\\kevin\\AppData\\Local\\Google\\Chrome\\User Data\\'
    whatsapp = WhatSend(chrome_path, chrome_profile_path)
    fileNames = "C:\\Users\\kevin\\Downloads\\Offer.jpeg C:\\Users\\kevin\\Downloads\\Menu.pdf"

    for index, row in df.iterrows():
        name = row['Customer Name'].strip().split()[0].capitalize()
        phone_number = str(row['Customer Phone']).strip()

        if phone_number not in phone_set:

            try:
                whatsapp.sendMessageToNewChat(phone_number, "", file=fileNames)
                name = ('{: <12}'.format(name))
                print(f"Message to {name}:\t{phone_number}\tSUCCESS")
                success_cnt += 1
                phone_set.add(phone_number)
                time.sleep(1)
            except Exception as e:
                print(f"Message to {name}:\t{phone_number}\tFAILED \t{str(e)}")
                failure_cnt += 1

        else:
            print(f"Message to {name}:\t{phone_number}\tRepeated")
            repeated_cnt += 1
        total += 1


    print(f"\n\nTotal \t: {total}\nSuccess \t: {success_cnt}\nFailure \t: {failure_cnt}\nRepeat \t: {repeated_cnt}")


if __name__ == '__main__':
    print_hi('PyCharm')
    send_messages_from_excel()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
