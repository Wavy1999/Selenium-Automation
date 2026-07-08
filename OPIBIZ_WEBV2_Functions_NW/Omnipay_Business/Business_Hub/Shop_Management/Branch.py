# ---------------------------
# Standard library imports
# ---------------------------
import os                   # File and directory operations
import time                 # Sleep/delays or timestamp operations
import traceback            # Capture stack traces for exception handling

# ---------------------------
# Third-party imports (Selenium WebDriver)
# ---------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------------------------
# Local / project-specific imports
# ---------------------------
from path_config import SCD_MODULE_PATHS  # Project-specific constants for module paths
from env_config import BASE_URL           # Centralized base URL (from .env)
from Utility import (                     # Custom helper functions for automation
    log_action,                           # Log successful actions for debugging/auditing
    log_error,                             # Log exceptions/errors for diagnostics
    clear_folder,                          # Clear temporary folders or files
    Main_Dashboard,                        # Access main dashboard functions
)

def Branches(driver, wait):

    wait = WebDriverWait(driver, 30)  # Ensure wait is defined for this function
    
     # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['Branches']['log']
    screenshots_folder = SCD_MODULE_PATHS['Branches']['screenshots']
    
    # Clear old files before test run
    clear_folder(screenshots_folder=screenshots_folder)
    try:
        
        shop_management_url = f"{BASE_URL}/ShopManagement"

        driver.get(shop_management_url)
        log_action(f"Direct navigation to: {shop_management_url}", log_file_path=log_file_path)

        # Wait for page to load fully
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "ShopManagement_Landing.png"))

        # Wait for Branches container
        branches_container = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.shop__management.branches")))
        log_action("Branches container visible", log_file_path=log_file_path)
        driver.save_screenshot(os.path.join(screenshots_folder, "Branches.png"))

    except Exception as e:
        error_message = f"Element not found or interaction failed: {traceback.format_exc()}"
        log_error(error_message, log_file_path=log_file_path, driver=driver)
        print(error_message)