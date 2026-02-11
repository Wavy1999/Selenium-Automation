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
    Main_Dashboard,                        # Access main dashboard functions
)

def Branches(driver, wait):
    
     # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['Branches']['log']
    screenshots_folder = SCD_MODULE_PATHS['Branches']['screenshots']
    
    # Clear old files before test run
    clear_folder(screenshots_folder=screenshots_folder)
    try:
        
        # Main_Dashboard(driver,log_file_path,screenshots_folder)
        # time.sleep(20)

        # # Business_Hub = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-bs-title='Business Hub' and .//span[text()='Business Hub']]")))
        # Business_Hub = driver.find_element(By.CSS_SELECTOR, '[data-bs-title="Business Hub"]')
        # driver.execute_script("arguments[0].click();", Business_Hub)
        # log_action("Clicked Business Hub menu", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(3)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Business_Hub_Menu.png"))

        # # # Shop Management
        # Shop_Management = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-bs-title='Shop Management' and .//span[text()='Shop Management']]")))
        # driver.execute_script("arguments[0].click();", Shop_Management)
        # log_action("Clicked Shop Management menu", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(3)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Shop_Management_Menu.png"))

        # Get current URL to construct the booking URL
        current_url = driver.current_url
        base_url = "/".join(current_url.split("/", 3)[:3])  # e.g. https://domain.com
        shop_management_url = base_url + "/ShopManagement"

        driver.get(shop_management_url)
        log_action(f"Direct navigation to: {shop_management_url}", log_file_path=log_file_path)

        # # Wait until page load complete
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")
        # time.sleep(3)

        # Branch = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,  "//a[@href='/ShopManagement' and .//span[text()='Branches']]")))
        # driver.execute_script("arguments[0].click();", Branch)
        # log_action("Clicked Branches menu", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # driver.save_screenshot(os.path.join(screenshots_folder, "Branches.png"))

        # base_url = "http://vm-app-dev01:9001"  # Use your actual base URL
        # driver.get(base_url + "/ShopManagement")
        # log_action("Navigated directly to Shop Management", log_file_path=log_file_path)

        # Wait for page to load fully
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "ShopManagement_Landing.png"))

        # # Wait for flyout panel or direct Branches link
        # flyout_panel = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.flyout-panel")))
        # log_action("Flyout panel visible", log_file_path=log_file_path)

        # # Click Branches
        # branches_link = WebDriverWait(flyout_panel, 20).until(EC.element_to_be_clickable((By.XPATH, ".//a[@href='/ShopManagement']")))
        # driver.execute_script("arguments[0].click();", branches_link)
        # log_action("Clicked Branches link in flyout", log_file_path=log_file_path)

        # Wait for Branches container
        branches_container = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.shop__management.branches")))
        log_action("Branches container visible", log_file_path=log_file_path)
        driver.save_screenshot(os.path.join(screenshots_folder, "Branches.png"))

    except Exception as e:
        error_message = f"Element not found or interaction failed: {traceback.format_exc()}"
        log_error(error_message, log_file_path=log_file_path, driver=driver)
        print(error_message)