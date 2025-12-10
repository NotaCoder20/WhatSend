# 📦 **selWhats_library**
### _Automated WhatsApp Web Messaging using Selenium + Chrome Remote Debugging_

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Selenium-Automation-green?style=flat-square" />
  <img src="https://img.shields.io/badge/WhatsApp-Web-00E676?style=flat-square" />
</p>

`selWhats_library` is a lightweight Python library for automating WhatsApp Web messaging using a real Chrome instance with Selenium + remote debugging.  
It is designed to be **simple**, **stable**, and **developer-friendly**.

---

# ⚡️ Features

- 📩 Send messages to **new numbers**
- 👤 Send messages to **existing contacts**
- 📎 Single or multiple file attachments  
- 🔁 Configurable retry logic  
- 📝 Custom logger support  
- 💨 Fast & stable Chrome debugging mode  
- 🧱 Clean XPath separation via `Elements.py`

---

# 📥 Installation

Install in editable mode:

```bash
pip install -e .
```

---

# 🚀 Quick Start

```python
from selWhats_library import WhatSend

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
profile_path = r"C:\Users\kevin\AppData\Local\Google\Chrome\User Data\Default"

ws = WhatSend(chrome_path, profile_path)

ws.sendMessageToNewChat("9082974811", "Hello! This is an automated message.")
ws.sendMessageToContact("Mom", "Reached safely 😊")
```

---

# 📎 Sending Files

### Single file:
```python
ws.sendMessageToNewChat(
    "9082974811",
    "Here is your file:",
    file=r"C:\Users\kevin\Downloads\image.jpg"
)
```

### Multiple files (space-separated string):
```python
files = r"C:\img1.jpg C:\img2.jpg"
ws.sendMessageToContact("John", "Today's photos!", file=files)
```

---

# 🔁 Retry Configuration

```python
ws = WhatSend(
    chrome_path,
    profile_path,
    retries=5
)
```

Retries apply to clicks & element waits for improved stability.

---

# 📝 Logging

### Verbose logs:
```python
import logging
ws = WhatSend(chrome_path, profile_path, log_level=logging.DEBUG)
```

### Custom logger:
```python
import logging
logger = logging.getLogger("whatsbot")
logger.setLevel(logging.INFO)

ws = WhatSend(chrome_path, profile_path, logger=logger)
```

---

# ❗ Troubleshooting

### 🔹 Chrome profile path not found
Ensure the folder exists:

```
C:\Users\<you>\AppData\Local\Google\Chrome\User Data\Default
```

---

### 🔹 WhatsApp Web asks for QR Code every time
Open Chrome manually:

```
chrome.exe --user-data-dir=<your profile>
```

Go to https://web.whatsapp.com and scan once.  
The library will reuse this session.

---

# 🏗 Development Notes

```
selWhats_library/
    __init__.py
    WhatSend.py
    WebDriver.py
    Elements.py
    colored_log.py
pyproject.toml
README.md
```

Editable installation:
```bash
pip install -e .
```

---

# 📜 License

MIT License (recommended)
