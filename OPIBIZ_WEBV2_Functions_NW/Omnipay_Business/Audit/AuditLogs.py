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
from selenium.common.exceptions import TimeoutException, NoAlertPresentException  # Handle Selenium exceptions

# ---------------------------
# Local / project-specific imports
# ---------------------------
from path_config import SCD_MODULE_PATHS  # Project-specific constants for module paths
from Utility import (                     # Custom helper functions for automation
    log_action,                           # Log successful actions for debugging/auditing
    log_error,                             # Log exceptions/errors for diagnostics
    clear_folder,                          # Clear temporary folders or files
)

def AuditLogs(driver, wait):
   
    # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['PayBills']['log']
    screenshots_folder = SCD_MODULE_PATHS['PayBills']['screenshots']
    
    # Clear old files before test run
    clear_folder(screenshots_folder=screenshots_folder)


    try:

        # Wait until the side options are clickable
        
        audit_logs_menu = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/AuditLogs']")))
        driver.execute_script("arguments[0].click()", audit_logs_menu)
        log_action("Clicked Audit Logs", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(3)
        driver.save_screenshot(os.path.join(screenshots_folder, "Send_Money.png"))

        Present_tbl = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "auditTrailTable_wrapper")))

        log_action("Audit table is present", log_file_path=log_file_path)

        Search_logs = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "searchTable")))
        Search_logs.send_keys("INVCONTROL")
        log_action("Search log", log_file_path=log_file_path)

        try:
            # Wait up to 10 seconds for the alert to appear
            WebDriverWait(driver, 10).until(EC.alert_is_present())

            # Switch to the alert
            alert = driver.switch_to.alert
            print("Alert says:", alert.text)

            # Accept the alert
            alert.accept()

        except TimeoutException:
            print("No alert appeared within the given time.")

        except NoAlertPresentException:
             print("No alert present when attempting to switch.")

        # Wait until search result (example: element with class 'search-result-item') is visible
        results = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "table-container")))
        log_action("Search log results", log_file_path=log_file_path)

        # Export Audit Logs in Excel
        export_logs = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//a[@data-btn-export-excel]')))
        driver.execute_script("arguments[0].click()", export_logs)
        log_action("Clicked Audit Logs", log_file_path=log_file_path)

    except Exception as e:
        error_message = f"Element not found or interaction failed: {traceback.format_exc()}"
        log_error(error_message, log_file_path=log_file_path, driver=driver)
        print(error_message)