# Standard library imports
import os
import time
import traceback
from datetime import datetime

# Third-party imports (Selenium)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local / project‑specific imports
from Utility import (
    log_action,
    log_error,
    clear_folder,
    wait_and_click_ok,
)
from path_config import SCD_MODULE_PATHS

def PayBills(driver,wait):

     # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['PayBills']['log']
    screenshots_folder = SCD_MODULE_PATHS['PayBills']['screenshots']
    
    # Clear old files before test run
    clear_folder(screenshots_folder=screenshots_folder)

    try:

        driver.refresh()

        # --- SEND MONEY --- #
        Send_Money = driver.find_element(By.CSS_SELECTOR, '[data-bs-title="Send Money"]')
        driver.execute_script("arguments[0].click();", Send_Money)
        log_action("Clicked Send Money menu", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(3)
        driver.save_screenshot(os.path.join(screenshots_folder, "Send_Money.png"))

        # --- PAY BILLS --- #
        pay_bills_menu  = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-bs-title='Pay Bills' and .//span[text()='Pay Bills']]")))
        driver.execute_script("arguments[0].click();", pay_bills_menu)
        log_action("Clicked 'To Another Bank' menu", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(3)
        driver.save_screenshot(os.path.join(screenshots_folder, "pay_bills_menu.png"))

        wait_and_click_ok(driver)
        log_action("Watch This Space! This feature will be available soon!",log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        driver.save_screenshot(os.path.join(screenshots_folder, "OK.png"))


    except Exception as e:
        log_error(f" Send Money function encountered an error: {traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
        driver.save_screenshot(os.path.join(screenshots_folder, "Critical_Error.png"))
        raise
