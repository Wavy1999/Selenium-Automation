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
from Utility import (                     # Custom helper functions for automation
    log_action,                           # Log successful actions for debugging/auditing
    log_error,                             # Log exceptions/errors for diagnostics
    clear_folder,                          # Clear temporary folders or files
)

def COrderview(driver, wait):

    log_file_path = SCD_MODULE_PATHS['COrder_View']['log']
    screenshots_folder = SCD_MODULE_PATHS['COrder_View']['screenshots']

    clear_folder(screenshots_folder=screenshots_folder)

    try:
        # -----------------
        # Seller Center
        # -----------------
        seller_center = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[contains(text(),'Seller Center')]/ancestor::a")
            )
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", seller_center)
        driver.execute_script("arguments[0].click();", seller_center)

        log_action("Clicked Seller Center", log_file_path=log_file_path)

        # -----------------
        # Create Order (safer locator)
        # -----------------
        create_order = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//a[contains(@href,'/OrderCreation')]")
            )
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", create_order)
        driver.execute_script("arguments[0].click();", create_order)

        log_action("Clicked Create Order", log_file_path=log_file_path)

        # -----------------
        # Wait for page ready
        # -----------------
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "card-body"))
        )

        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        log_action("Create Order page loaded", log_file_path=log_file_path)

        driver.save_screenshot(os.path.join(screenshots_folder, "Create_Order_Page.png"))

        print("Create Order page loaded successfully.")

    except Exception:
        error_message = f"Element not found or interaction failed:\n{traceback.format_exc()}"
        log_error(error_message, log_file_path=log_file_path, driver=driver)
        print(error_message)
