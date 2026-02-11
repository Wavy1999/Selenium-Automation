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
    human_like_typing,                     # Simulate realistic typing in UI automation
    product_data,                           # Data structure/helper for product information
    product_dropdown,                       # Select a product from a dropdown
    upload_image_product,                   # Upload product images in UI forms
    select_data,                            # General selection utility for forms/tables
    wait_and_click_ok,                      # Wait for dialog/button and click safely
)

def CNProduct(driver, wait):
    
    # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['CNProduct']['log']
    screenshots_folder = SCD_MODULE_PATHS['CNProduct']['screenshots']

    # Clear old files before test run  
    clear_folder(screenshots_folder=screenshots_folder)

    try:
        # === NAVIGATE TO SELLER CENTER DASHBOARD ===
        # For Debugging Purposes uncomment the line below per module
        print("Navigating to Seller Center Dashboard...")
        Seller_Center = wait.until(EC.element_to_be_clickable((By.XPATH,  "//a[@data-bs-title='Seller Center' and @data-bs-toggle='tooltip' and .//span[text()='Seller Center']]")))
        driver.execute_script("arguments[0].click()", Seller_Center)
        log_action("Clicked Seller Center", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        Product_Management =  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"//a[@data-bs-title='Product Management' and @data-bs-toggle='tooltip' and .//span[text()='Product Management']]")))
        driver.execute_script("arguments[0].click();", Product_Management)
        log_action("Clicked Product Management", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshots_folder, "Product_Management.png"))

        Create_new_product = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/ProductManagement/NewProduct') and .//span[contains(text(), 'Create New Product')]]")))
        driver.execute_script("arguments[0].click();", Create_new_product)
        log_action("Clicked Create New Product", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshots_folder, "Create_New_Product_Page.png"))

        main_content = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "mainContent")))
        log_action("Create New Product page loaded successfully", log_file_path=log_file_path)
        time.sleep(3)
        driver.save_screenshot(os.path.join(screenshots_folder, "Create_New_Product_Content.png"))

        add_products = product_data()

        # Product name
        product_name = driver.find_element(By.ID, "Product.ProductName")
        product_name.clear()
        human_like_typing(product_name, str(add_products["Product Name"]))
        log_action(f"Entered Product Name: {add_products['Product Name']}", log_file_path=log_file_path)
        time.sleep(2)

        # SKU
        sku = driver.find_element(By.ID, "Product.SalesInfo.SKU")
        sku.clear()
        human_like_typing(sku, str(add_products["SKU"]))
        log_action(f"Entered SKU: {add_products['SKU']}", log_file_path=log_file_path)
        time.sleep(2)

        # UNIT OF MEASURES
        select_data (driver, wait, "Product.InventoryInfo.UnitOfMeasureID", "pc")
        log_action(f"Entered Units of Measure: pc", log_file_path=log_file_path)
        time.sleep(2)

        # Product DESCRIPTION
        product_description = driver.find_element(By.ID, "Product.ProductDescription")
        product_description.clear()
        human_like_typing(product_description, add_products["Product Description"])
        log_action(f"Entered Menu Description: {add_products['Product Description']}", log_file_path=log_file_path)
        time.sleep(2)
      
        # Warehouse
        select_data(driver, wait, "Product.InventoryInfo.WarehouseID", "MAIN WAREHOUSE")
        log_action(f"Selected Warehouse: MAIN WAREHOUSE", log_file_path=log_file_path)

        # STOCK QUANTITY
        stock_quantity = driver.find_element(By.NAME, "Product.InventoryInfo.Quantity")
        stock_quantity.clear()
        human_like_typing(stock_quantity, str(add_products["Quantity"]))
        log_action(f"Entered Stock Quantity: {add_products['Quantity']}", log_file_path=log_file_path)
        time.sleep(2)

        # Predefined TAGS
        select_data(driver, wait, "Product.ProductTags.TagKey", "BRAND")
        log_action(f"Selected Predefined Tags: BRAND", log_file_path=log_file_path)
        time.sleep(2)

        # Product Value
        product_value = driver.find_element(By.ID, "Product.ProductTags.TagValue")
        product_value.clear()
        human_like_typing(product_value, str(add_products["Product Value"]))
        log_action(f"Entered Menu Value: {add_products['Product Value']}", log_file_path=log_file_path)
        time.sleep(2)

        # UNIT PRICE
        unit_price = driver.find_element(By.ID, "Product.SalesInfo.CostPerUnit")
        unit_price.clear()
        human_like_typing(unit_price, str(add_products["Unit Price"]))
        log_action(f"Entered Unit Price: {add_products['Unit Price']}", log_file_path=log_file_path)
        time.sleep(2)

        # Product CATEGORY
        select_data(driver, wait, "Product.CategoryDescription", "Electronics and Accessories")
        log_action(f"Selected Product Category: Electronics and Accessories", log_file_path=log_file_path)
        time.sleep(2)

     
        # Product CATEGORY 
        select_data(driver, wait, "Product.CategoryDescription", "Electronics and Accessories")
        log_action(f"Selected Product Category: Electronics and Accessories", log_file_path=log_file_path)
        time.sleep(2)

        # Product SUB CATEGORY 
        select_data(driver, wait, "Product.SubCategoryDescription", "Audio and Video Equipment")
        log_action(f"Selected Product SUB CATEGORY: Audio and Video Equipment", log_file_path=log_file_path)
        time.sleep(2)

        # Image Upload
        uploaded_img_path = upload_image_product(driver)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);",uploaded_img_path)
        log_action(f"Uploaded image: {uploaded_img_path}", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)                                       
                                                  
        # Submit
        save_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'saveProduct')))
        time.sleep(0.5)
        driver.execute_script("arguments[0].click()", save_btn)
        log_action("Clicked Save Button", log_file_path=log_file_path)
        driver.save_screenshot(os.path.join(screenshots_folder, ' save_btn.png'))
        log_action("Added New Product ", log_file_path=log_file_path)
        time.sleep(5)

        # Confirmation 
        confirm_btn =  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'swal2-confirm') and contains(text(), 'OK')]")))
        driver.execute_script("arguments[0].click();", confirm_btn)
        log_action("Clicked Confirm OK", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # Success
        driver.save_screenshot(os.path.join(screenshots_folder, ' success.png'))
        log_action("Clicked Confirm Success", log_file_path=log_file_path)
        time.sleep(5)

    except Exception as e:
        error_message = f"Critical error in Seller Dashboard: {traceback.format_exc()}"
        log_error(error_message, log_file_path=log_file_path, driver=driver)
        driver.save_screenshot(os.path.join(screenshots_folder, 'Critical_Error.png'))
        raise