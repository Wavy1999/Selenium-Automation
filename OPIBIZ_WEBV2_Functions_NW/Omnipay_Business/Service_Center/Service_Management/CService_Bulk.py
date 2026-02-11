# Standard library imports
import os
import time
import traceback

# Third‑party imports (Selenium)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)

# Local / project‑specific imports
from path_config import SCD_MODULE_PATHS
from Utility import (
    clear_folder,
    log_action,
    log_error,
    click_service_management,
)

def CService_Bulk(driver, wait):
    log_file_path = SCD_MODULE_PATHS['CService_Bulk']['log']
    screenshots_folder = SCD_MODULE_PATHS['CService_Bulk']['screenshots']

    clear_folder(screenshots_folder=screenshots_folder)

    try:
        # === NAVIGATE TO SERVICE CENTER DASHBOARD === #
        # Click the main Service Center link

        # print("Navigating to Service Center Dashboard...")
        # Service_Center = wait.until(EC.element_to_be_clickable((By.XPATH,  "//a[@data-bs-title='Service Center' and @data-bs-toggle='tooltip' and .//span[text()='Service Center']]")))
        # driver.execute_script("arguments[0].click()", Service_Center)
        # log_action("Clicked Seller Center", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # Service_Management =  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"//a[@data-bs-title='Service Management' and @data-bs-toggle='tooltip' and .//span[text()='Service Management']]")))
        # driver.execute_script("arguments[0].click();", Service_Management)
        # log_action("Clicked Service Management", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(5)

        # Create_Bulk = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/ServiceCenter/BatchService') and .//span[contains(text(), 'Create Service (Bulk)')]]")))
        # driver.execute_script("arguments[0].click();", Create_Bulk)
        # log_action("Clicked Create New Product(Bulk)", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(5)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Create Bulk Product.png"))
    
        url = "http://beta-opibizscd.paybps.ovpn/ServiceCenter/BatchService"
        driver.get(url)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Create Service (Bulk)e.png"))

        # File path
        excel_path = r"d:\Bastion\SQA_QualityEnterprise\SoftwareTesting\Projects\Common\Automation\OPI\Files\Testdata\Service_Batch_Upload.xlsx"
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
           

    except Exception as e:
        error_message = f"Critical error in Create New Service Bulk: {traceback.format_exc()}"
        log_error(error_message, log_file_path=log_file_path, driver=driver)
        driver.save_screenshot(os.path.join(screenshots_folder, "Critical_Error.png"))
        raise
