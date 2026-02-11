# Standard library imports
import os
import time
import traceback
from datetime import datetime

# Third‑party imports (Selenium WebDriver)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Local / project‑specific imports
from path_config import SCD_MODULE_PATHS
from Utility import (
    clear_folder,
    log_action,
    log_error,
    random_service,
    select_warehouse,
    upload_image_service,
    wait_and_click_ok,
    select_location,
    Main_Dashboard,
)

def CNService(driver, wait):

    log_file_path = SCD_MODULE_PATHS['CNService']['log']
    screenshots_folder = SCD_MODULE_PATHS['CNService']['screenshots']
    
    clear_folder(screenshots_folder=screenshots_folder)
  
    try:
      
        url = "http://beta-opibizscd.paybps.ovpn/ProductManagement/NewService?type=add"
        driver.get(url)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        driver.save_screenshot(os.path.join(screenshots_folder, "Create New Service Page.png"))

        # ============================================
        # STEP 4: Fill in Service Information
        # ============================================
        service = random_service()

        # Service Name
        service_name = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "Product.ProductName")))
        service_name.clear()
        service_name.send_keys(service["Service Name"])
        log_action(f"Entered Service Name: {service['Service Name']}", log_file_path=log_file_path)
        time.sleep(1)

        # SKU
        sku = driver.find_element(By.NAME, "Product.SalesInfo.SKU")
        sku.clear()
        sku.send_keys(service["SKU"])
        log_action(f"Entered SKU: {service['SKU']}", log_file_path=log_file_path)
        time.sleep(1)

        # Units of Measure
        uom = driver.find_element(By.NAME, "Product.InventoryInfo.UnitOfMeasure")
        uom.clear()
        uom.send_keys(service["Units of Measure"])
        log_action(f"Entered Units of Measure: {service['Units of Measure']}", log_file_path=log_file_path)
        time.sleep(1)

        # Service Description
        desc = driver.find_element(By.NAME, "Product.ProductDescription")
        desc.clear()
        desc.send_keys(service["Service Description"])
        log_action(f"Entered Service Description: {service['Service Description']}", log_file_path=log_file_path)
        time.sleep(1)
        
        select_location(driver, "Location", "MAIN WAREHOUSE", log_file_path)
        log_action("Selected Warehouse: MAIN WAREHOUSE", log_file_path=log_file_path)

        # Unit Price
        price = driver.find_element(By.NAME, "Product.SalesInfo.CostPerUnit")
        price.clear()
        price.send_keys(service["Unit Price"])
        log_action(f"Entered Unit Price: {service['Unit Price']}", log_file_path=log_file_path)
        time.sleep(1)

        # Service Tags
        tags_key = driver.find_element(By.NAME, "Product.ProductTags.TagKey")
        tags_key.clear()
        tags_val = service["Service Tags"]
        if not isinstance(tags_val, tuple):
            tags_val = (tags_val,)
        tags_key.send_keys(tags_val)
        log_action(f"Entered Service Tags: {tags_val}", log_file_path=log_file_path)
        time.sleep(1)

        # Service Value
        tags_value = driver.find_element(By.NAME, "Product.ProductTags.TagValue")
        tags_value.clear()
        tags_val2 = service["Service Value"]
        if not isinstance(tags_val2, tuple):
            tags_val2 = (tags_val2,)
        tags_value.send_keys(tags_val2)
        log_action(f"Entered Service Value: {tags_val2}", log_file_path=log_file_path)
        time.sleep(1)

        # Service Sub-Category
        subcat = driver.find_element(By.NAME, "Product.SubCategoryDescription")
        subcat.clear()
        subcat.send_keys(service["Service Sub-Category"])
        log_action(f"Entered Service Sub-Category: {service['Service Sub-Category']}", log_file_path=log_file_path)
        time.sleep(1)

        # Service Media
        try:
            uploaded_img_path = upload_image_service(driver, log_file_path, input_locator=(By.CSS_SELECTOR, "input[type='file']"))
            log_action(f"Uploaded image: {uploaded_img_path}", log_file_path=log_file_path)
        except Exception as e:
            log_error(f"Could not upload image: {traceback.format_exc()}", log_file_path=log_file_path)

        driver.save_screenshot(os.path.join(screenshots_folder, "after fillup.png"))
  
        # ============================================
        # STEP 5: Save Service
        # ============================================
        save_selectors = [
            (By.XPATH, "//a[contains(text(),'Save')]"),
            (By.XPATH, "//button[contains(text(),'Save')]"),
            (By.CSS_SELECTOR, "#serviceForm a.btn-primary, #serviceForm button.btn-primary"),
            (By.XPATH, '//*[@id="serviceForm"]/div[2]/a[1]'),
        ]
        
        for selector in save_selectors:
            try:
                save_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(selector))
                driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", save_btn)
                log_action("Clicked Save Service", log_file_path=log_file_path)
                break
            except:
                continue
        
        time.sleep(2)

        # ============================================
        # STEP 6: Confirm Dialog
        # ============================================
        confirm_selectors = [
            (By.XPATH, "//button[contains(@class,'swal2-confirm')]"),
            (By.CSS_SELECTOR, ".swal2-confirm"),
            (By.XPATH, "//button[contains(text(),'OK') or contains(text(),'Yes') or contains(text(),'Confirm')]"),
            (By.XPATH, "/html/body/div[3]/div/div[6]/button[1]"),
        ]
        
        for selector in confirm_selectors:
            try:
                confirm_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(selector))
                driver.execute_script("arguments[0].click();", confirm_btn)
                log_action("Confirmed Service Creation", log_file_path=log_file_path)
                break
            except:
                continue

    except Exception as e:
        error_message = f"Element not found or interaction failed: {traceback.format_exc()}"
        log_error(error_message, log_file_path=log_file_path, driver=driver)
        print(error_message)
        raise  # ✅ Re-raise so TestRunner knows it failed