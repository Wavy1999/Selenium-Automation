# ---------------------------
# Standard library imports
# ---------------------------
import os                 # For file and directory operations
import time               # For delays/sleep or timestamp-based logic
import traceback          # For capturing stack traces in exception handling

# ---------------------------
# Third-party imports (Selenium WebDriver)
# ---------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------------------------
# Local / project-specific imports
# ---------------------------
from path_config import SCD_MODULE_PATHS     # Project-specific path constants
from Utility import (                        # Custom helper functions for automation
    log_action,                              # Log successful actions for auditing/debugging
    log_error,                               # Log errors/exceptions for diagnostics
    clear_folder,                            # Clear temporary folders or files
    select_data_by_text,                      # Select an option in dropdowns by visible text
    handle_inventory_modal,                   # Handle pop-up modals related to inventory
    wait_and_click_ok,                        # Wait for a dialog/button and click safely
    get_latest_product_name_from_log,         # Fetch latest product name from logs for chaining
)

def Inventory_Management(driver,wait):
    
    # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['IManagement']['log']
    screenshots_folder = SCD_MODULE_PATHS['IManagement']['screenshots']

    # Clear old files before test run  
    clear_folder(screenshots_folder=screenshots_folder)
    driver.refresh()

    try:

        # === NAVIGATE TO SELLER CENTER DASHBOARD ===
        # For Debugging Purposes uncomment the line below per module
        print("Navigating to Seller Center Dashboard...")
        Seller_Center = wait.until(EC.element_to_be_clickable((By.XPATH,  "//a[@data-bs-title='Seller Center' and @data-bs-toggle='tooltip' and .//span[text()='Seller Center']]")))
        driver.execute_script("arguments[0].click()", Seller_Center)
        log_action("Clicked Seller Center", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        Inventory_Management = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"//a[contains(@href, '/SellerCenter/InventoryManagement') and .//span[contains(text(), 'Inventory Management')]]")))
        driver.execute_script("arguments[0].click();", Inventory_Management)
        log_action("Clicked Inventory Management", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        driver.save_screenshot(os.path.join(screenshots_folder, "Inventory_Management_Page.png"))

         # === Inventory Control === #

        # Add Inventory
        add_inventory = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-action-update='add' and contains(@class, 'add-inventory-btn')]")))
        driver.execute_script("arguments[0].click();", add_inventory)
        log_action("Clicked Add Inventory button", log_file_path=log_file_path)

        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        inventory_modal = WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'swal2-popup') and contains(@class, 'swal2-modal')]")))
        log_action("Add Inventory modal displayed", log_file_path=log_file_path)

        driver.save_screenshot(os.path.join(screenshots_folder, "Add_Inventory_Modal.png"))

        # Extract logs from CNProduct for reuse
        logs_reuse_path = SCD_MODULE_PATHS['CNProduct']['log']
        product_name = get_latest_product_name_from_log(logs_reuse_path)

        if not product_name:
            print("  No product name found in CNProduct log.")
            return

        log_action(f"Searching for product: {product_name}", log_file_path=log_file_path)

        # Select Product
        product = select_data_by_text(log_file_path, wait, "product-select", product_name, by="text")
        log_action(f"Selected Product: {product.text}", log_file_path=log_file_path)

        # Enter Quantity
        quantity_input = driver.find_element(By.ID, "add-quantity-input")
        quantity_input.clear()
        quantity_input.send_keys("50")
        log_action("Entered Quantity: 50", log_file_path=log_file_path)
        time.sleep(2)
        
        # Reference Number
        reference_input = driver.find_element(By.ID, "transmittalID-input")
        reference_input.clear()
        reference_input.send_keys("REF12345")
        log_action("Entered Reference Number: REF12345", log_file_path=log_file_path)
        time.sleep(2)

        # Branch/Warehouse
        branch = select_data_by_text(driver, wait, "warehouse-select", "1", by="value")
        log_action(f"Selected Warehouse: {branch.text}", log_file_path=log_file_path)
        time.sleep(2)

        # Remarks
        remarks_input = driver.find_element(By.ID, "movementNote-textarea")
        remarks_input.clear()
        remarks_input.send_keys("Adding inventory for testing purposes.")
        log_action(f"Entered Remarks{remarks_input.text}", log_file_path=log_file_path)
        time.sleep(2)

        # Submit Add Inventory
        add_btn = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'swal2-confirm') and normalize-space(text())='Add']")))
        driver.execute_script("arguments[0].click();", add_btn)
        log_action("Clicked Add button to submit inventory addition", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(10)
        driver.save_screenshot(os.path.join(screenshots_folder, "Inventory_Added.png"))
        
        handle_inventory_modal(driver, wait, action="update_quantity", log_file_path=log_file_path)
        log_action("Clicked Update Quantity", log_file_path=log_file_path)
        time.sleep(5)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        inventory_modal_2 = WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".swal2-popup.swal2-show")))
        time.sleep(2)

        # Reason 
        reason = select_data_by_text(log_file_path, wait, "movementReason-select", "Retrieved Item(s)",by="text")
        log_action(f"Entered Reason: {reason.text}", log_file_path=log_file_path)
        time.sleep(2)

        # Remarks
        remarks_input = driver.find_element(By.ID, "movementNote-textarea")
        remarks_input.clear()
        remarks_input.send_keys("Adding inventory for testing purposes.")
        log_action(f"Entered Remarks{remarks_input.text}", log_file_path=log_file_path)
        time.sleep(2)

        driver.save_screenshot(os.path.join(screenshots_folder, "Add_Quantity.png"))

        # Confirmation
        yes_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'swal2-confirm') and normalize-space(text())='Yes']")))
        driver.execute_script("arguments[0].click();", yes_button)
        log_action("Clicked Confirmation",log_file_path=log_file_path)
        time.sleep(2)

        wait_and_click_ok(driver)
        log_action("Clicked Ok",log_file_path=log_file_path)

         # === Inventory Movement === #
        inventory_movement = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "nav-inventory-movement-tab")))
        driver.execute_script("arguments[0].click();", inventory_movement)
        driver.execute_script("arguments[0].scrollIntoView({block: 'end'});", inventory_movement)
        log_action("Clicked Inventory button", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        driver.save_screenshot(os.path.join(screenshots_folder, "Inventory Movemen.png"))


       

    except Exception as e:
        log_error(f"An error occurred: {str(e)}", log_file_path=log_file_path)
        log_error(traceback.format_exc(), log_file_path=log_file_path)