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
    human_like_typing,                     # Simulate realistic typing in UI automation
    random_warehouse,                      # Select a random warehouse for testing
    upload_image_warehouse,                # Upload warehouse images in UI forms
    select_dropdown,                        # Select an option in dropdown menus
    clear_folder,                           # Clear temporary folders or files
    wait_and_click_ok,                      # Wait for dialog/button and click safely
    navigate_flyout,                        # Navigate through flyout menus in UI
)

def WHouse(driver, wait):
   
   # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['WHouse']['log']
    screenshots_folder = SCD_MODULE_PATHS['WHouse']['screenshots']
    
    # Clear old files before test run
    clear_folder(screenshots_folder=screenshots_folder)
    driver.refresh()
    try:
        
        # Business Hub
        # Uncomment this per module
        # Business_Hub = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-bs-title='Business Hub' and .//span[text()='Business Hub']]")))
        # driver.execute_script("arguments[0].click();", Business_Hub)
        # log_action("Clicked Business Hub menu", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(3)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Business_Hub_Menu.png"))

        # Shop Management
        # Shop_Management = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-bs-title='Shop Management' and .//span[text()='Shop Management']]")))
        # Shop_Management = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[3]/div[1]/div[1]/div/ul/li[2]")))
        # driver.execute_script("arguments[0].click();", Shop_Management)
        # log_action("Clicked Shop Management menu", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(3)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Shop_Management_Menu.png"))

        # # Select Warehouses
        # Warehouses_Submenu = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/header/div/div/div[2]/ul/li[2]/a/div/img")))
        # driver.execute_script("arguments[0].click();", Warehouses_Submenu)
        # log_action("Clicked Warehouses submenu", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(3)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Warehouses_Submenu.png"))

        base_url = "http://beta-opibizscd.paybps.ovpn/ShopManagement/Warehouse "  # Use your actual base URL
        driver.get(base_url)
        log_action("Navigated directly to Warehouse", log_file_path=log_file_path)

        # Add Warehouses
        Add_Warehouse = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/ShopManagement/AddWarehouse') and contains(@class, 'btn-primary')]")))
        driver.execute_script("arguments[0].click();", Add_Warehouse)
        log_action("Clicked Add New Warehouse button", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Add_New_Warehouse.png"))
      
        # Populate Fields
        warehouse_data = random_warehouse()  # dictionary

        # Warehouse Name
        w_name = driver.find_element(By.NAME, "Description")
        w_name.clear()
        human_like_typing(w_name, warehouse_data["Warehouse Name"])
        log_action(f"Entered Warehouse Name: {warehouse_data['Warehouse Name']}", log_file_path=log_file_path)

        # Contact Person
        contact = driver.find_element(By.NAME, "ContactPerson")
        contact.clear()
        human_like_typing(contact, warehouse_data["Contact Person"])
        log_action(f"Entered Contact Person: {warehouse_data['Contact Person']}", log_file_path=log_file_path)

        # Contact Number
        contact_no = driver.find_element(By.NAME, "ContactNo")
        contact_no.clear()
        human_like_typing(contact_no, str(warehouse_data["Contact No."]))
        log_action(f"Entered Contact No.: {warehouse_data['Contact No.']}", log_file_path=log_file_path)

        # Location Name
        location = driver.find_element(By.NAME, "LocationName")
        location.clear()
        human_like_typing(location, warehouse_data["Location Name"])
        log_action(f"Entered Location Name: {warehouse_data['Location Name']}", log_file_path=log_file_path)

        # House/Floor/Unit No.
        house_no = driver.find_element(By.NAME, "houseNumber")
        house_no.clear()
        human_like_typing(house_no, str(warehouse_data["House/Floor/Unit No."]))
        log_action(f"Entered House/Floor/Unit No.: {warehouse_data['House/Floor/Unit No.']}", log_file_path=log_file_path)

        # Block/Building/Street
        street = driver.find_element(By.NAME, "street")
        street.clear()
        human_like_typing(street, warehouse_data["Block/Building/Street"])
        log_action(f"Entered Street: {warehouse_data['Block/Building/Street']}", log_file_path=log_file_path)

        # Country dropdown
        select_dropdown(driver, wait, "select2-countryCode-container", warehouse_data["Country"])
        log_action(f"Selected Country: {warehouse_data['Country']}", log_file_path=log_file_path)
        time.sleep(2)

        # Province dropdown
        select_dropdown(driver, wait, "select2-province-container", warehouse_data["Province"])
        log_action(f"Selected Province: {warehouse_data['Province']}", log_file_path=log_file_path)
        time.sleep(2)

        # City/Municipality dropdown
        select_dropdown(driver, wait, "select2-city-container", warehouse_data["City/Municipality"])
        log_action(f"Selected City/Municipality: {warehouse_data['City/Municipality']}", log_file_path=log_file_path)
        time.sleep(2)

        # Barangay dropdown
        select_dropdown(driver, wait, "select2-barangay-container", warehouse_data["Barangay"])
        log_action(f"Selected Barangay: {warehouse_data['Barangay']}", log_file_path=log_file_path)
        time.sleep(2)

        # Postal Code
        postal = driver.find_element(By.NAME, "postCode")
        postal.clear()
        human_like_typing(postal, str(warehouse_data["Postal Code"]))
        log_action(f"Entered Postal Code: {warehouse_data['Postal Code']}", log_file_path=log_file_path)

        # Image Upload
        uploaded_img_path = upload_image_warehouse(driver)
        log_action(f"Uploaded image: {uploaded_img_path}", log_file_path=log_file_path)
        
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Fill_Warehouse.png"))

        # Add New Warehouse Button
        Add_New_Warehouse_Button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-add-new-warehouse and contains(normalize-space(text()), 'Add New Warehouse')]")))
        driver.execute_script("arguments[0].scrollIntoView({ block: 'center', inline: 'center' });", Add_New_Warehouse_Button)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", Add_New_Warehouse_Button)
        log_action("Clicked Add New Warehouse button", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Add_New_Warehouse_Button.png"))

        Confirm_Button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'swal2-confirm') and normalize-space(text())='Confirm']")))
        driver.execute_script("arguments[0].click();", Confirm_Button)
        log_action("Clicked SweetAlert Confirm button", log_file_path=log_file_path)
        time.sleep(1)
        driver.save_screenshot(os.path.join(screenshots_folder, "Confirm.png"))

        wait_and_click_ok(driver,timeout=20)
        log_action("Warehouse has been createed sucessfully",log_file_path=log_file_path)
        time.sleep(1)
        driver.save_screenshot(os.path.join(screenshots_folder, "Success.png"))

        # Coming soon Bulk Warehouse




    except Exception as e:
        error_message = f"Element not found or interaction failed: {traceback.format_exc()}"
        log_error(error_message, log_file_path=log_file_path, driver=driver)
        print(error_message)
