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
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------------------------
# Local / project-specific imports
# ---------------------------
from path_config import SCD_MODULE_PATHS  # Project-specific constants for module paths
from Utility import (                     # Custom utility functions for automation
    log_action,                           # Log successful actions for debugging/auditing
    log_error,                             # Log exceptions/errors for diagnostics
    clear_folder,                          # Clear temporary folders or files
    select_warehouse,                       # Select a warehouse in UI forms or tables
)

def Bulk(driver, wait):
    
    # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['CNProducts_Bulk']['log']
    screenshots_folder = SCD_MODULE_PATHS['CNProducts_Bulk']['screenshots']

    # Clear old files before test run  
    clear_folder(screenshots_folder=screenshots_folder)

    try:
            
            # === NAVIGATE TO SELLER CENTER DASHBOARD ===
            # For Debugging Purposes uncomment the line below per module
            # print("Navigating to Seller Center Dashboard...")
            # Seller_Center = wait.until(EC.element_to_be_clickable((By.XPATH,  "//a[@data-bs-title='Seller Center' and @data-bs-toggle='tooltip' and .//span[text()='Seller Center']]")))
            # driver.execute_script("arguments[0].click()", Seller_Center)
            # log_action("Clicked Seller Center", log_file_path=log_file_path)
            # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

            # Product_Management =  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"//a[@data-bs-title='Product Management' and @data-bs-toggle='tooltip' and .//span[text()='Product Management']]")))
            # driver.execute_script("arguments[0].click();", Product_Management)
            # log_action("Clicked Product Management", log_file_path=log_file_path)
            # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            # time.sleep(5)
            
            # Create_Bulk = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/ProductManagement/BatchProduct') and .//span[contains(text(), 'Create New Products (Bulk)')]]")))
            # driver.execute_script("arguments[0].click();", Create_Bulk)
            # log_action("Clicked Create New Product(Bulk)", log_file_path=log_file_path)

            driver.get("http://beta-opibizscd.paybps.ovpn/ProductManagement/BatchProduct")
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            time.sleep(5)
            driver.save_screenshot(os.path.join(screenshots_folder, "Create Bulk Product.png"))

            warehouse_dropdown = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "warehouseID")))
            log_action("Create New Product(Bulk) page loaded successfully", log_file_path=log_file_path)
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

            # Select Warehouse
            wait.until_not(EC.presence_of_element_located((By.CSS_SELECTOR, ".loading, .spinner, .overlay, .modal-backdrop.show")))
            select_warehouse (driver, wait, "warehouseID", "MAIN WAREHOUSE")
            log_action("Selected Warehouse: Main Warehouse", log_file_path=log_file_path)
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

            # File path
            excel_path = r"d:\Bastion\SQA_QualityEnterprise\SoftwareTesting\Projects\Common\Automation\OPI\Files\Testdata\Product_Batch_Upload.xlsx"
            log_action(f"Excel File Path: {excel_path}", log_file_path=log_file_path)

            file_input = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.filepond--browser")))
            file_input.send_keys(excel_path)
            log_action("Uploaded Excel file for Bulk Product Upload", log_file_path=log_file_path)
            time.sleep(5)
            driver.save_screenshot(os.path.join(screenshots_folder, "Bulk Product Upload.png"))

            upload_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-upload-batch]")))
            driver.execute_script("arguments[0].click();", upload_button)
            log_action("Clicked Upload button for Bulk Product Upload", log_file_path=log_file_path)
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
           
            success_section = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='success']//h1[contains(text(), 'Batch Product Successfully Processed!')]")))
            log_action("Bulk Product Upload processed successfully", log_file_path=log_file_path)

            driver.save_screenshot(os.path.join(screenshots_folder, "Bulk Product Upload Success.png"))

    except Exception as e:
            error_message = f"Critical error in Create New Product Bulk: {traceback.format_exc()}"
            log_error(error_message, log_file_path=log_file_path, driver=driver)
            driver.save_screenshot(os.path.join(screenshots_folder, 'Critical_Error.png'))
            raise