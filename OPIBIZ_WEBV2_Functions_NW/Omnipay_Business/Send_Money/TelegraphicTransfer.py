# Standard library imports
import os
import time
import traceback
from datetime import datetime

# Third‑party imports (Selenium)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local / project‑specific imports
from Utility import (
    log_action,
    log_error,
    clear_folder,
)
from path_config import SCD_MODULE_PATHS

def TelegraphicTransfer(driver,wait):

     # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['TelegraphicTransfer']['log']
    screenshots_folder = SCD_MODULE_PATHS['TelegraphicTransfer']['screenshots']
    
    # Clear old files before test run
    clear_folder(screenshots_folder=screenshots_folder)

    try:

        # driver.refresh()

        # # --- SEND MONEY --- #
        # Send_Money = driver.find_element(By.CSS_SELECTOR, '[data-bs-title="Send Money"]')
        # driver.execute_script("arguments[0].click();", Send_Money)
        # log_action("Clicked Send Money menu", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(3)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Send_Money.png"))

        url = "http://vm-app-dev01:9001/EcoPay/RequestTelegraphicTransfer"
        driver.get(url)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(3)
        driver.save_screenshot(os.path.join(screenshots_folder, "Request Telegraphic Transfer.png"))
        
        # # --- Request Telegraphic Transfer --- #
        # request_tt_menu = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/EcoPay/RequestTelegraphicTransfer']")))
        # log_action("Clicked 'Request Telegraphic Transfer' menu", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(3)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Request Telegraphic Transfer.png"))

    except Exception as e:
        log_error(f" Send Money function encountered an error: {traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
        driver.save_screenshot(os.path.join(screenshots_folder, "Critical_Error.png"))
        raise
