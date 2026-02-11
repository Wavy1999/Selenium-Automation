import os
import traceback
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from path_config import SCD_MODULE_PATHS

from Utility import (
    log_action,
    log_error,
    clear_folder,
    wait_and_click_ok,
)


def Bulk_Employee(driver, wait):
 
    # -------------------
    # Setup paths
    # -------------------
    log_file_path = SCD_MODULE_PATHS["Employee_Bulk"]["log"]
    screenshots_folder = SCD_MODULE_PATHS["Employee_Bulk"]["screenshots"]
    clear_folder(screenshots_folder=screenshots_folder)

    try:
        # Use consistent wait timeout
        wait = WebDriverWait(driver, 30)

        # -------------------
        # Navigate menus
        # -------------------
        if not _navigate_to_bulk_employee(driver, wait, log_file_path, screenshots_folder):
            return False

        # -------------------
        # Upload Excel file
        # -------------------
        excel_path = r"d:\Bastion\SQA_QualityEnterprise\SoftwareTesting\Projects\Common\Automation\OPI\Files\Testdata\SCD_BULK_EMPLOYEE-250908.xlsx"
        
        # Validate file exists before attempting upload
        if not os.path.exists(excel_path):
            log_error(f"Excel file not found: {excel_path}", log_file_path)
            driver.save_screenshot(os.path.join(screenshots_folder, "File_Not_Found.png"))
            return False
            
        log_action(f"Excel File Path: {excel_path}", log_file_path)

        # Upload file
        file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
        file_input.send_keys(excel_path)
        log_action("File added to FilePond", log_file_path)
        
        # Small wait to ensure file is registered
        time.sleep(1)

        # Click upload button
        upload_btn = wait.until(EC.element_to_be_clickable((By.ID, "uploadButton")))
        driver.execute_script("arguments[0].click();", upload_btn)
        log_action("Clicked Upload button for Bulk Employee Upload", log_file_path)
        driver.save_screenshot(os.path.join(screenshots_folder, "After_Click_Upload.png"))

        # -------------------
        # Wait for file upload confirmation and click OK
        # -------------------
        try:
            wait_and_click_ok(driver, timeout=15)
            log_action("Confirmed file upload dialog", log_file_path)
        except Exception as e:
            log_action(f"No upload dialog appeared or error clicking OK: {str(e)}", log_file_path)

        # -------------------
        # Wait for success message
        # -------------------
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(),'Bulk Upload Employee Successfully Processed')]")))
            driver.save_screenshot(os.path.join(screenshots_folder, "Bulk_Employee_Success.png"))
            log_action("Bulk Employee Upload successful", log_file_path)
            return True
            
        except TimeoutException:
            log_error("Success confirmation message not found", log_file_path)
            driver.save_screenshot(os.path.join(screenshots_folder, "Success_Message_Timeout.png"))
            return False

    except TimeoutException as e:
        print(f"Timeout error: {str(e)}")
        print(traceback.format_exc())
        driver.save_screenshot(os.path.join(screenshots_folder, "Timeout_Error.png"))
        log_error(f"Timeout in Bulk_Employee: {str(e)}\n{traceback.format_exc()}", log_file_path)
        return False
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        print(traceback.format_exc())
        driver.save_screenshot(os.path.join(screenshots_folder, "Unexpected_Error.png"))
        log_error(f"Unexpected error in Bulk_Employee: {str(e)}\n{traceback.format_exc()}", log_file_path)
        return False


def _navigate_to_bulk_employee(driver, wait, log_file_path, screenshots_folder):
 
    try:
        # Click Business Hub
        # business_hub = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-bs-title="Business Hub"]')))
        # driver.execute_script("arguments[0].click();", business_hub)
        # log_action("Clicked Business Hub menu", log_file_path)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Business_Hub_Menu.png"))
        # time.sleep(0.5)  # Brief pause for menu to expand

        # # Click Employee Management
        # employee_management = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-bs-title='Employee Management' or contains(., 'Employee Management')]")))
        # driver.execute_script("arguments[0].click();", employee_management)
        # log_action("Clicked Employee Management", log_file_path)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Employee_Management_Menu.png"))
        # time.sleep(0.5)  # Brief pause for submenu to expand

        # # Click Add New Employee (Bulk)
        # add_new_employee_bulk = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[.//span[normalize-space(text())='Add New Employee (Bulk)']]")))
        # driver.execute_script("arguments[0].click();", add_new_employee_bulk)
        # log_action("Clicked Add New Employee (Bulk)", log_file_path)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Add_New_Employee_Bulk_Page.png"))

        # URL
        # url = "http://vm-app-dev01:9001/EmployeeManagement/BatchEmployee"
        url = "http://beta-opibizscd.paybps.ovpn/EmployeeManagement/BatchEmployee"
        driver.get(url)
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        driver.save_screenshot(os.path.join(screenshots_folder, "Navigate_Bulk_Employee_Page.png"))
        log_action("Navigated to Bulk Employee Upload page", log_file_path)
        
        # Wait for page to fully load
        time.sleep(1)
        
        return True
        
    except TimeoutException as e:
        log_error(f"Navigation timeout: {str(e)}", log_file_path)
        driver.save_screenshot(os.path.join(screenshots_folder, "Navigation_Error.png"))
        return False
    except Exception as e:
        log_error(f"Navigation error: {str(e)}", log_file_path)
        driver.save_screenshot(os.path.join(screenshots_folder, "Navigation_Exception.png"))
        return False