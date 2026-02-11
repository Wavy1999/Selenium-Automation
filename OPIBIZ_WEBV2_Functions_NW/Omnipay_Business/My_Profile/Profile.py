# Standard library imports
import os
import time
import traceback

# Third‑party imports (Selenium WebDriver)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local / project‑specific imports
from Utility import (
    log_action,
    log_error,
    clear_folder,
)
from path_config import SCD_MODULE_PATHS

def Profile(driver, wait, timeout=10):
    
    # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['Profile']['log']
    screenshots_folder = SCD_MODULE_PATHS['Profile']['screenshots']
    
    # Clear old files before test run
    clear_folder(screenshots_folder=screenshots_folder)

    try:
       
        my_profile_menu = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Profile']")))
        driver.execute_script("arguments[0].click();", my_profile_menu)
        log_action("Clicked 'My Profile' menu", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(3)
        driver.save_screenshot(os.path.join(screenshots_folder, "My_Profile.png"))

        Settings = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "nav-settings-tab")))
        driver.execute_script("arguments[0].click();", Settings)
        log_action("Clicked Settings", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(3)
        driver.save_screenshot(os.path.join(screenshots_folder, "Settings.png"))

    except Exception as e:
        error_message = f"Failed to click 'My Profile': {repr(e)}"
        log_error(error_message, log_file_path=log_file_path)
        log_error(traceback.format_exc(), log_file_path=log_file_path)
        print(error_message)
        print(traceback.format_exc())
