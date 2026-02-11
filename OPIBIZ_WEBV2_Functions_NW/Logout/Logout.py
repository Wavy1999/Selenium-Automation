# Standard library imports
import os
import time
import traceback

# Third-party imports (Selenium WebDriver)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local / project-specific imports
from Utility import (
    log_error,
    log_action,
    clear_folder,
)
from path_config import LOGIN_PATHS

def Logout(driver, wait):
   # Get paths from configuration
    log_file_path = LOGIN_PATHS['Logout']['log']
    screenshots_folder = LOGIN_PATHS['Logout']['screenshots']

    # Clear old files before test run  
    clear_folder(screenshots_folder=screenshots_folder)

    driver.refresh()
    
    try:

        # Logout navbar
        Logout_btn = driver.find_element(By.CSS_SELECTOR, '[data-bs-title="Logout"]')
        driver.execute_script("arguments[0].click()", Logout_btn)
        WebDriverWait(driver,10).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        log_action("Clicked Logout on navbar", log_file_path=log_file_path)
        driver.save_screenshot(os.path.join(screenshots_folder, 'Logout_Clicked.png'))

        # try:
        #     # Confirm Logout                                           
        #     confirm_logout = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'swal2-confirm')]")))
        #     log_action("Confirm Logout", log_file_path=log_file_path)
        #     WebDriverWait(driver,30).until(lambda d: d.execute_script('return document.readyState') == 'complete') 
        #     driver.save_screenshot(os.path.join(screenshots_folder, 'Logout.png'))

        # except Exception:
        #     error_message = f"Logout confirmation button not found or interaction failed: {traceback.format_exc()}"
        #     log_error(error_message, log_file_path=log_file_path)
        #     print(error_message)
            
    except Exception:
        error_message = f"Element not found or interaction failed: {traceback.format_exc()}"
        log_error(error_message, log_file_path=log_file_path)
        print(error_message)
