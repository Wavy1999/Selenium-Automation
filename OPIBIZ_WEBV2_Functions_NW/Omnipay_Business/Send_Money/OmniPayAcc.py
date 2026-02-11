# Standard library imports
import os
import time
import traceback
from datetime import datetime

# Third‑party imports (Selenium)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local/project imports
from Utility import (
    log_action,
    log_error,
    clear_folder,
)
from path_config import SCD_MODULE_PATHS

def OmniPayAcc(driver,wait):

     # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['OmniPayAcc']['log']
    screenshots_folder = SCD_MODULE_PATHS['OmniPayAcc']['screenshots']
    
    # Clear old files before test run
    clear_folder(screenshots_folder=screenshots_folder)

    try:

        # --- SEND MONEY --- #
        # Send_Money = driver.find_element(By.CSS_SELECTOR, '[data-bs-title="Send Money"]')
        # driver.execute_script("arguments[0].click();", Send_Money)
        # log_action("Clicked Send Money menu", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(3)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Send_Money.png"))

        # --- TO OMNIPAY --- #
        # to_omnipay = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "//a[@data-bs-title='To Another OmniPay Account']]")))
        # driver.execute_script("arguments[0].click();", to_omnipay)
        # log_action("Clicked 'To Another OmniPay Account' menu", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(3)
        # driver.save_screenshot(os.path.join(screenshots_folder, "To_Omnipay.png"))
        
        url = "http://vm-app-dev01:9001/EcoPay/TransferToOmnipay"
        driver.get(url)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(3)
        driver.save_screenshot(os.path.join(screenshots_folder, "To_Omnipay Account.png"))

        # --- TO ANOTHER BANK --- #
        to_another_bank = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.transfer-tab[data-transfer-type='bank']")))
        driver.execute_script("arguments[0].click();", to_another_bank)
        log_action("Clicked 'To Another Bank' button", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(3)
        driver.save_screenshot(os.path.join(screenshots_folder, "to_Another_bank.png"))

    except Exception as e:
        log_error(f" Send Money function encountered an error: {traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
        driver.save_screenshot(os.path.join(screenshots_folder, "Critical_Error.png"))
        raise
