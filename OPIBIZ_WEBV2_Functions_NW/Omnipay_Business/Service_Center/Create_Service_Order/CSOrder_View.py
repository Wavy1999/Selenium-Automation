# Standard library imports
import os
import time

# Third‑party imports (Selenium)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local / project‑specific imports
from Utility import log_action, clear_folder
from path_config import SCD_MODULE_PATHS

def CSOrder_View(driver, wait):
    log_file_path = SCD_MODULE_PATHS['CSOrder_View']['log']
    screenshots_folder = SCD_MODULE_PATHS['CSOrder_View']['screenshots']

    clear_folder(screenshots_folder=screenshots_folder)
    
    try:
        # Wait and expand Service Center menu
        # Service_Center = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-bs-title='Service Center' and @data-bs-toggle='tooltip' and .//span[text()='Service Center']]")))
        # driver.execute_script("arguments[0].click()", Service_Center)
        # log_action("Clicked Service Center", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        
        # create_service_order  = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,"//a[@href='/OrderCreation?type=service#' ""and @data-bs-title='Create Acknowledgement Receipt' ""and @data-bs-toggle='tooltip' ""and .//span[text()='Create Service Order']]")))
        # driver.execute_script("arguments[0].click();", create_service_order)
        url  = "http://beta-opibizscd.paybps.ovpn/OrderCreation?type=service#"
        driver.get(url)
        log_action("Clicked Create Service Center", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        driver.save_screenshot(os.path.join(screenshots_folder, "Create Service Center.png"))

        # Wait for page load and take screenshot
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        driver.save_screenshot(os.path.join(screenshots_folder, "Create_Service_Order_View.png"))

    except Exception as e:
        log_action(f"An error occurred: {e}", log_file_path=log_file_path)
