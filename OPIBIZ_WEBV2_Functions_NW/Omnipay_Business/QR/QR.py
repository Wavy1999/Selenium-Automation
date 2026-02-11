# Standard library imports
import os
import sys
import time
import traceback

# Third‑party imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local / project‑specific imports
from Utility import (
    click_element,
    log_action,
    log_error,
    select_item,
    select_item_qr,
    clear_folder
)
from path_config import SCD_MODULE_PATHS

def QR(driver, wait):
    # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['QR']['log']
    screenshots_folder = SCD_MODULE_PATHS['QR']['screenshots']
    
    # Clear old files before test run
    clear_folder(screenshots_folder=screenshots_folder)

    try:

        # Check Seller Dashboard
        generate_qr_menu = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/GenerateQR']")))
        driver.execute_script("arguments[0].click();", generate_qr_menu)
        log_action("Clicked 'Generate QR' menu", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(3)
        driver.save_screenshot(os.path.join(screenshots_folder, "Generate_QR.png"))

        notes = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="orderNotes"]')))
        notes.send_keys("Test")
        log_action("Input Order Notes", log_file_path=log_file_path)
        time.sleep(5)

        amount = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="amount"]')))
        amount.send_keys("5")
        log_action("Input Amount", log_file_path=log_file_path)
        time.sleep(5)

        GenerateQR_btn = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="generateQRForm"]/div/div/div[6]/button')))
        driver.execute_script("arguments[0].click()", GenerateQR_btn)
        log_action("Clicked Generate QR Button", log_file_path=log_file_path)
        time.sleep(10)

        qr_element  =  WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME,'generate-qr')))
        log_action("QR code is now visible", log_file_path=log_file_path)
            
        # Click Generate QR
        GenerateQR_new = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[3]/div[1]/div/div[2]/a[1]")))
        driver.execute_script("arguments[0].click()", GenerateQR_new)
        log_action("Clicked Generate new QR code", log_file_path=log_file_path)
        time.sleep(5)

        # Custom QR
        custom_qr = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "customQRCheckbox")))
        driver.execute_script("arguments[0].click()", custom_qr)
        log_action("Clicked Custom QR", log_file_path=log_file_path)
        time.sleep(5)

        # Client name
        client_name = wait.until(EC.presence_of_element_located((By.NAME, "clientName")))
        client_name.send_keys("Test")
        log_action("Input Client Name", log_file_path=log_file_path)
        time.sleep(5)

        # Select Products
        Select_products = wait.until(EC.element_to_be_clickable((By.ID, "selectProducts")))
        driver.execute_script("arguments[0].click()", Select_products)
        log_action("Clicked Select Product", log_file_path=log_file_path)
        time.sleep(5)

        # Select Item
        select_item_qr(wait, driver, "searchProducts", "bag", log_file_path=log_file_path)
        log_action("Select item to order", log_file_path=log_file_path)
        time.sleep(15)

        # Quantity
        Quantity = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="quantity"]')))
        Quantity.send_keys("1")
        log_action("Input Quantity", log_file_path=log_file_path)
        time.sleep(5)
        
        # Confirm
        confirm = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="quantity"]')))
        driver.execute_script("arguments[0].click()", confirm)
        log_action("Clicked Confirm", log_file_path=log_file_path)

        element = wait.until(EC.element_to_be_clickable((By.ID, "selectProducts")))
        select_item_qr(wait, driver, "searchProducts", "watch", log_file_path=log_file_path)
        log_action("Select item to order", log_file_path=log_file_path)
        time.sleep(15)
        
        element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div[3]/div[2]/div/div/div[2]/form/div[3]/div[1]/input")))
        element.send_keys(1)
        log_action("Input Quantity", log_file_path=log_file_path)
        time.sleep(5)

        click_element(wait, driver, By.XPATH, "//*[@id=\"productForm\"]/div[3]/div[2]/button", log_file_path=log_file_path)
        log_action("Clicked confirm", log_file_path=log_file_path)
        time.sleep(5)

        click_element(wait, driver, By.XPATH, "//*[@id=\"selectedProductsTable\"]/tbody/tr/td[5]/a", log_file_path=log_file_path)
        log_action("Clicked Remove", log_file_path=log_file_path)
        time.sleep(5)

        click_element(wait, driver, By.ID, "clearSelection", log_file_path=log_file_path)
        log_action("Clicked Clear Selection", log_file_path=log_file_path)
        time.sleep(5)

        element = wait.until(EC.element_to_be_clickable((By.ID, "selectProducts")))
        driver.execute_script("arguments[0].click()", element)
        log_action("Clicked Select Product", log_file_path=log_file_path)
        time.sleep(5)

        select_item_qr(wait, driver, "searchProducts", "BP Glasses", log_file_path=log_file_path)
        log_action("Select item to order", log_file_path=log_file_path)
        time.sleep(15)
        
        element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div[3]/div[2]/div/div/div[2]/form/div[3]/div[1]/input")))
        element.send_keys("1")
        log_action("Input Quantity", log_file_path=log_file_path)
        time.sleep(5)

        click_element(wait, driver, By.XPATH, "//*[@id=\"productForm\"]/div[3]/div[2]/button", log_file_path=log_file_path)
        log_action("Clicked confirm", log_file_path=log_file_path)
        time.sleep(5)

        element = wait.until(EC.presence_of_element_located((By.ID, "orderNotes")))
        element.send_keys("Test")
        log_action("Input Order Notes", log_file_path=log_file_path)
        time.sleep(5)

        click_element(wait, driver, By.XPATH, "//*[@id=\"generateQRForm\"]/div/div/div[6]/button", log_file_path=log_file_path)
        log_action("Clicked Generate QR", log_file_path=log_file_path)
        time.sleep(10)

        element = wait.until(EC.element_to_be_clickable((By.ID, "QRCodeGenerated")))
        log_action("Check if QR Code Exists", log_file_path=log_file_path)
        time.sleep(5)
                
    except Exception as e:
        error_message = f"Element not found or interaction failed: {repr(e)}"
        log_error(error_message, log_file_path=log_file_path, driver=driver)
        error_message = f"Element not found or interaction failed: {traceback.format_exc()}"
        print(error_message)