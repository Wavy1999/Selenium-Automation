Run it to the powershell
.venv\Scripts\activate

Then install the following virtual venv

1. pip install selenium
2. pip install openpyxl
3. pip install webdriver-manager
4. pip install pyautogui
5. pip install seleniumbase
6. pip install prettytable
7. pip install Pillow
8. pip install openpyxl pillow

Framework plugins
 1. pip install behave
 2. pip install pytest
 3. pip install allure
 4. pip install allure-combine --break-system-packages


cd OPIBIZ_WEBV2_Functions_NW\admin

# List files to confirm
dir *.py
allure serve allure-results
pytest test_resto.py -v -s --html=Automation_Test_report.html --self-contained-html

Here’s what exit statuses 0, 1, and 2 typically mean on Unix / Linux systems:

Exit status 0 → Success (no error). 
Exit status 1 → General error or “something went wrong” (often used when there’s no more specific code). 
Exit status 2 → Misuse of shell built-in commands or more specific error (depending on the program).

1. pip install screeninfo
2. pip install isort