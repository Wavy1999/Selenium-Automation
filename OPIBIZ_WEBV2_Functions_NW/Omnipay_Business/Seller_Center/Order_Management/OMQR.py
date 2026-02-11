# ---------------------------
# Standard library imports
# ---------------------------
import os                   # File and directory operations
import time                 # Sleep/delays or timestamp operations

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
from Utility import (                     # Custom utility functions for automation
    log_action,                           # Log successful actions for debugging/auditing
    clear_folder,                          # Clear temporary folders or files
)

def OMQR(driver, wait):
    
    # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['OMQR']['log']
    screenshots_folder = SCD_MODULE_PATHS['OMQR']['screenshots']

    # Clear old files before test run  
    clear_folder(screenshots_folder=screenshots_folder)

    # driver.refresh()
    # log_action("For better running",log_file_path=log_file_path)

    try:
        # Navigate: Order Management → Generate QR View only
         # Uncomment this for solo run this module
        # print("Navigating to Seller Center Dashboard...")

        # Seller_Center = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-bs-title='Seller Center' and .//span[text()='Seller Center']]")))
        # driver.execute_script("arguments[0].click()", Seller_Center)
        # log_action("Clicked Seller Center", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(3)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Seller_Center.png"))

        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # # Order_Management = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[.//span[contains(text(), 'Order Management')]]")))
        # driver.execute_script("arguments[0].click();", Order_Management)
        # log_action("Clicked Order Management", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        breadcrumb = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.ob__breadcrumb-link")))
        driver.execute_script("arguments[0].click();", breadcrumb)
        log_action("Clicked 'Order Management' breadcrumb", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(3)
        driver.save_screenshot(os.path.join(screenshots_folder, "QR.png"))
        
        QR = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/GenerateQR']")))
        driver.execute_script("arguments[0].click();", QR)
        log_action("Clicked Generate QR", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshots_folder, "Generate_QR_Page.png"))
        log_action("Generate QR Page loaded successfully", log_file_path=log_file_path)

       # Custom QR
        custom_qr = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "customQRCheckbox")))
        driver.execute_script("arguments[0].click()", custom_qr)
        log_action("Clicked Custom QR", log_file_path=log_file_path)
        time.sleep(5)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshots_folder, "Custom_QR_Option_Selected.png"))

    except Exception as e:
        log_action(f"An error occurred: {e}", log_file_path=log_file_path)
