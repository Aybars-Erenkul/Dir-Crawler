# DirCrawler
![Made With Python](http://ForTheBadge.com/images/badges/made-with-python.svg) ![Made with love](http://ForTheBadge.com/images/badges/built-with-love.svg)

A GUI Web directory and file scanner written in Python 3.10


<img src="https://user-images.githubusercontent.com/90629653/218284134-782ba2e7-8b31-462e-8574-a2f70d2a4e93.png" width="396" height="439">

<img src="https://user-images.githubusercontent.com/90629653/218284149-e0c88e44-1252-487c-b7e8-c8e45f4be809.png" width="396" height="439">

Requirements:

  1)PyQt6
  
  2)Requests

*Note: If you want to convert this script into a standalone executable using PyInstaller, you'd need to change the* **uic.loadUi("window.ui", self)** *to the absolute path of the window.ui such as* **uic.loadUi("r'C:\Development\Python\window.ui", self)**. *The r prefix makes sure the backslashes are interpreted literally. *
