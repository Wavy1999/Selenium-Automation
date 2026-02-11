# Standard library imports
import os           # for file system / path operations
import time         # for sleep or time-based operations
import traceback    # for exception tracebacks / debugging stack traces

# Third-party imports (Selenium WebDriver)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Local application / project imports
from Utility import (
    log_action,              # custom action logging
    log_error,               # custom error logging
    clear_folder,            # utility to clear folders
    upload_file_bulk_employee  # utility to bulk upload employee files
)
from path_config import SCD_MODULE_PATHS  # project-specific config for module paths

def Bulk_Employee(driver, wait):
   
    # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['Bulk_Employee']['log']
    screenshots_folder = SCD_MODULE_PATHS['Bulk_Employee']['screenshots']
    
    # Clear old files before test run
    clear_folder(screenshots_folder=screenshots_folder)

    try:
        # Wait until the side options are clickable
        Business_Hub = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-bs-title='Business Hub' and .//span[text()='Business Hub']]")))
        driver.execute_script("arguments[0].click();", Business_Hub)
        log_action("Clicked Business Hub menu", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Business_Hub_Menu.png"))

        # Employee Management
        Employee_Management = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-bs-title='Employee Management' and .//span[text()='Employee Management']]")))
        driver.execute_script("arguments[0].click();", Employee_Management)
        log_action("Clicked Employee Management menu", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Employee_Management_Menu.png"))
       
        # Employee List
        add_new_client_bulk = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[.//span[normalize-space(text())='Add New Client (Bulk)']]")))
        driver.execute_script("arguments[0].click();", add_new_client_bulk)
        log_action("Clicked Add New Client (Bulk) fly‑out", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(3)
        driver.save_screenshot(os.path.join(screenshots_folder, "Add_New_Client_Bulk_Page.png"))

        # Batch Upload of Bulk Features
        try:
            uploaded_file_path = upload_file_bulk_employee(driver, log_file_path)
            log_action(f"Uploaded file: {uploaded_file_path}", log_file_path=log_file_path)
        except Exception as e:
            log_error(f"Could not upload file: {traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
            # Return or raise here to prevent continuing with failed upload
            return

        # Wait for the photo / upload preview element to become visible
        upload_preview_xpath = '//*[@id="filepond--item-qdn7re9vv"]/fieldset/div/div[6]'

        # Wait a bit for processing
        time.sleep(3)

        # Upload
        upload_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="batchOrderForm"]/div[2]/button')))
        driver.execute_script("arguments[0].click()", upload_btn)
        log_action("Clicked Upload button", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(3)
        driver.save_screenshot(os.path.join(screenshots_folder, "Bulk_Services.png"))

    except Exception as e:
        error_message = f"Element not found or interaction failed: {traceback.format_exc()}"
        log_error(error_message, log_file_path=log_file_path, driver=driver)
        print(error_message)
        raise  