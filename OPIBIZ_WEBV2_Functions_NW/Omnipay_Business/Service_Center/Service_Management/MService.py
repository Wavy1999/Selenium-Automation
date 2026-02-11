# Standard library imports
import os              # For file and path operations
import traceback       # For retrieving stack traces when catching exceptions
import time            # For sleep/delay or timestamp-based operations
import random          # For generating random values (e.g. selecting a random service)

# Selenium (third‑party) imports — for browser automation
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local / project‑specific imports — utilities and config for your project
from Utility import (        # Custom utility functions for logging, cleanup, typing, etc.
    log_action,             # Log significant actions during automation (for debugging / audit)
    log_error,              # Log errors / exceptions for diagnosis
    clear_folder,           # Clean up temporary folders/files (cleanup between runs)
    human_like_typing,      # Simulate realistic typing behavior in automated UI tests
    set_start_date,         # Utility to set start date in UI form / calendar picker
    get_latest_name_from_log_service,  # Get last logged service name — helpful for chaining tests
    find_service_row,       # Locate a service row in UI tables/grids
    random_service,         # Helper to pick a random service (test data)
    wait_and_click_ok,      # Wait for dialog/modal OK button, then click — stable for waits
    set_end_date,           # Utility to set end date in UI form / calendar picker
    set_post_promo_price,   # Utility to set promotional/pricing fields in UI forms
    set_future_date,        # Utility for selecting a future date (for scheduling, tests)
    product_data,           # Data structure / helper for product‑related test data
    fill_order_row,         # Helper to fill order rows in UI forms or tables
    search_and_select_client,   # UI helper: search and select a client in a form/dropdown
    search_and_select_address   # UI helper: search and select an address in a form/dropdown
)

from path_config import SCD_MODULE_PATHS  # Configuration constants / paths used across modules

def MService(driver, wait):
    # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['MService']['log']
    screenshots_folder = SCD_MODULE_PATHS['MService']['screenshots']

    # Clear old files before test run  
    clear_folder(screenshots_folder=screenshots_folder)

    try:
        # === NAVIGATE TO SELLER CENTER DASHBOARD === #
        # Uncomment this if debugging per module
        # print("Navigating to Service Center Dashboard...")
        # service_center = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,"//a[@data-bs-title='Service Center' and @data-bs-toggle='tooltip' and .//span[text()='Service Center']]")))
        # driver.execute_script("arguments[0].click()", service_center)
        # log_action("Clicked Service Center", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # # Service Management
        # service_management = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,"//a[@data-bs-title='Service Management' and @data-bs-toggle='tooltip' and .//span[text()='Service Management']]")))
        # driver.execute_script("arguments[0].click()", service_management)
        # log_action("Clicked Service Management", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # driver.save_screenshot(os.path.join(screenshots_folder, "Service_Management.png"))

        # Manage Services
        manage_services = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[onclick='navToManageService()'].btn.btn-secondary.ob-button")))
        driver.execute_script("arguments[0].scrollIntoView();", manage_services)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", manage_services)
        log_action("Clicked Manage Services", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(3)
        driver.save_screenshot(os.path.join(screenshots_folder, "Manage_Services.png"))

        # Get latest service name from Create_New_Service log
        logs_reuse_path = SCD_MODULE_PATHS['CNService']['log']
        service_name = get_latest_name_from_log_service(logs_reuse_path)
        if not service_name:
            print("No service name found in CNService log.")
            return
        log_action(f"Searching for service: {service_name}", log_file_path=log_file_path)

        # --- SEARCH FOR SERVICE --- #
        search_box = wait.until(EC.presence_of_element_located((By.ID, "managementSearch")))
        search_box.clear()
        human_like_typing(search_box, service_name)
        time.sleep(2)  # allow table to filter
        driver.save_screenshot(os.path.join(screenshots_folder, "Searched_Service.png"))
        log_action(f"Searched for service: {service_name}", log_file_path=log_file_path)

        target_row = find_service_row(driver, service_name)
        if not target_row:
            raise Exception(f"Service '{service_name}' not found in table.")

        # --- CLICK CHECKBOX ---
        try:
            checkbox = target_row.find_element(By.CSS_SELECTOR, "td:first-child input[type='checkbox']")
            driver.execute_script("arguments[0].click();", checkbox)
            log_action("Selected service checkbox", log_file_path=log_file_path)
        except Exception as e:
            log_error(f"Failed to click checkbox: {str(e)}\n{traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
            raise

        # --- VIEW SERVICE ---
        try:
            view_btn = target_row.find_element(By.XPATH, ".//button[contains(text(),'View Service')]")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_btn)
            driver.execute_script("arguments[0].click();", view_btn)
            log_action("Clicked View Service", log_file_path=log_file_path)
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            time.sleep(5)
            driver.save_screenshot(os.path.join(screenshots_folder, "Service_View.png"))
        except Exception as e:
            log_error(f"Failed to click View Service: {str(e)}\n{traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
            raise

        # --- BACK TO MANAGE PRODUCTS ---
        try:
            back_btn = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.bck-btn")))
            driver.execute_script("arguments[0].click();", back_btn)
            log_action("Clicked Manage Product button", log_file_path=log_file_path)
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        except Exception as e:
            log_error(f"Failed to navigate back to Manage Products: {str(e)}\n{traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
            raise

        # --- Click Update Service ---
        try:
            update_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, f"//table[@id='servicemanagemenTable']//tr[td[contains(text(), '{service_name}')]]//button[contains(text(), 'Update Service')]")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", update_btn)
            driver.execute_script("arguments[0].click();", update_btn)
            log_action("Clicked Update Service", log_file_path=log_file_path)
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            driver.save_screenshot(os.path.join(screenshots_folder, "Service_Update_Page.png"))
        except Exception as e:
            log_error(f"Failed to click Update Service: {str(e)}\n{traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
            raise

        # --- Update fields (example: warehouse, price, etc.) ---
        
        service = random_service()
        try:
            # SELECT WAREHOUSE via the search‐input dropdown style
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.swal2-container.loading-spinner-container")))
            
            dropdown_search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="serviceForm"]/div[1]/div/section[1]/div[2]/div[3]/div/span/span[1]/span/ul/li/input')))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown_search)
            time.sleep(0.3)

            driver.execute_script("arguments[0].click();", dropdown_search)
            dropdown_search.clear()
            dropdown_search.send_keys(service["Location"])
            dropdown_search.send_keys(Keys.ENTER)
            dropdown_search.send_keys(Keys.TAB)
            
            time.sleep(1)
            log_action(f"Selected Location by typing & Enter: {service['Location']}", log_file_path=log_file_path)
            time.sleep(2)
            log_action("Selected Warehouse: MAIN WAREHOUSE", log_file_path=log_file_path)

        except Exception as e:
            log_error(f"Failed to update service fields: {str(e)}\n{traceback.format_exc()}",log_file_path=log_file_path, driver=driver)
            raise

        # --- CLICK SAVE ---
        try:
            save_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-service-save].btn.btn-primary.save-btn")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", save_btn)
            log_action("Clicked Save Button", log_file_path=log_file_path)
            driver.save_screenshot(os.path.join(screenshots_folder, 'Service_Saved.png'))
        except Exception as e:
            log_error(f"Failed to click Save button: {str(e)}\n{traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
            raise

        # --- CONFIRM OK ---
        try:
            confirm_btn = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'swal2-confirm') and contains(text(), 'OK')]")))
            driver.execute_script("arguments[0].click();", confirm_btn)
            log_action("Clicked Confirm OK", log_file_path=log_file_path)
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            driver.save_screenshot(os.path.join(screenshots_folder, 'Services_Updated.png'))
        except Exception as e:
            log_error(f"Failed to click Confirm OK: {str(e)}\n{traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
            raise
        
        time.sleep(10)

        try:
            # --- BACK TO MANAGE SERVICE ---
            manage_btn = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'ob-button') and text()='Manage Service']")))
            driver.execute_script("arguments[0].scrollIntoView({block:'start'});", manage_btn)
            driver.execute_script("arguments[0].click();", manage_btn)
            log_action("Clicked Manage Service button", log_file_path=log_file_path)

        except Exception as e:
            log_error(f"Failed to click Manage Services: {str(e)}\n{traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
            raise

        # Upload photo
        try:

            search_box_2 = wait.until(EC.presence_of_element_located((By.ID, "managementSearch")))
            search_box_2.clear()
            human_like_typing(search_box_2, service_name)
            log_action(f"Searched for product: {service_name}", log_file_path=log_file_path)
            time.sleep(3)
            driver.save_screenshot(os.path.join(screenshots_folder, "Searched_Product.png"))
            
            target_row_2 = find_service_row(driver, service_name)
            if not target_row:
                raise Exception(f"Service '{service_name}' not found in table.")

            # --- CLICK CHECKBOX ---
            try:
                checkbox2 = target_row_2.find_element(By.CSS_SELECTOR, "td:first-child input[type='checkbox']")
                driver.execute_script("arguments[0].click();", checkbox2)
                log_action("Selected service checkbox2", log_file_path=log_file_path)
            except Exception as e:
                log_error(f"Failed to click checkbox2: {str(e)}\n{traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
                raise

            image_folder = r"D:\Bastion\SQA_QualityEnterprise\SoftwareTesting\Projects\Common\Automation\OPI\Files\Images\Service Media"

            # Check folder exists
            if not os.path.exists(image_folder):
                raise FileNotFoundError(f"Folder not found: {image_folder}")

            # Get all images
            images = [os.path.join(image_folder, f) for f in os.listdir(image_folder)
                    if f.lower().endswith((".png", ".jpg", ".jpeg"))]

            # Pick random image
            random_image = random.choice(images)
            log_action(f"Selected random image for upload: {random_image}", log_file_path=log_file_path)

            # Find the hidden file input (example: usually has type='file')
            upload_input = driver.find_element(By.XPATH, "//input[@type='file']")  # change XPath if needed

            driver.execute_script("arguments[0].style.display = 'block';", upload_input)

            # Send the random file
            upload_input.send_keys(random_image)

            # Click upload button if needed
            driver.find_element(By.ID, "uploadAllBtn").click()
            log_action("Uploaded photo", log_file_path=log_file_path)

            swal_popup = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.swal2-popup.swal2-show")))
            log_action("Upload Images Successfully appeared", log_file_path=log_file_path)
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            time.sleep(5)
            driver.save_screenshot(os.path.join(screenshots_folder, ' Image_Uploaded.png'))
            

            # Upload again to close the modal
            upload_again_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class,'btn') and text()='Upload again']")))
            driver.execute_script("arguments[0].click();", upload_again_btn)
            log_action("Clicked Upload Again to close the modal", log_file_path=log_file_path)
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            time.sleep(5)
            driver.save_screenshot(os.path.join(screenshots_folder, ' Image_Uploadeds.png'))
         
        
        except Exception as e:
            log_error(f"Failed to upload photo: {str(e)}\n{traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
            raise

        try:
                # Search box
                search_box_3 = wait.until(EC.presence_of_element_located((By.ID, "managementSearch")))
                search_box_3.clear()
                human_like_typing(search_box_3, service_name)
                log_action(f"Searched for product: {service_name}", log_file_path=log_file_path)
                time.sleep(3)
                driver.save_screenshot(os.path.join(screenshots_folder, "Searched_Product.png"))
            
                target_row_3 = find_service_row(driver, service_name)
                if not target_row:
                    raise Exception(f"Service '{service_name}' not found in table.")

                # --- CLICK CHECKBOX ---
                try:
                    checkbox3 = target_row_3.find_element(By.CSS_SELECTOR, "td:first-child input[type='checkbox']")
                    driver.execute_script("arguments[0].click();", checkbox3)
                    log_action("Selected service checkbox3", log_file_path=log_file_path)
                except Exception as e:
                    log_error(f"Failed to click checkbox3: {str(e)}\n{traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
                    raise

                # Price Adjustment
                price_icon = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img.img-price-icon[alt='adjust price icon']")))
                driver.execute_script("arguments[0].click();", price_icon)
                log_action("Clicked first Adjust Price icon", log_file_path=log_file_path)

                # Wait until the radio input is clickable
                promo_option_1 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label.radio-card[for='temporaryPromoRadio'], label.radio-card")))
                driver.execute_script("arguments[0].click();", promo_option_1)
                log_action("Selected Option 1: Run a Special Promotion", log_file_path=log_file_path)
                WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

                modal_body = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.modal-body.pb-4")))
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//p[@data-modal-productid and contains(text(), 'BNW-PRD-')]")))
                log_action(" Adjust Price modal displayed successfully.", log_file_path=log_file_path)
                time.sleep(5)
                driver.save_screenshot(os.path.join(screenshots_folder, "AdjustPrice_Modal_Visible.png"))

                update_data = product_data()

                # Promo price
                promo_price = driver.find_element(By.NAME, "PriceAdjustments[0].UnitPrice")
                promo_price.clear()
                human_like_typing(promo_price, str(update_data["Unit Price"]))
                log_action(f"Entered Promo Price: {update_data['Unit Price']}", log_file_path=log_file_path)  

                # Start Date and End Date
                set_start_date(driver, wait, log_file_path)
                log_action("Set Start Date for Promotion", log_file_path=log_file_path)

                set_end_date(driver, wait, log_file_path)
                log_action("Set End Date for Promotion", log_file_path=log_file_path)

                # Set post promo price
                set_post_promo_price(driver, wait, 2299.00, log_file_path)
                log_action("Set Post Promo Price", log_file_path=log_file_path)
                driver.save_screenshot(os.path.join(screenshots_folder, "Option1_PromoDetails.png"))

                # Save Price Adjustment
                save_btn = wait.until(EC.element_to_be_clickable((By.ID, "savePriceAdjustmentBtn")))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", save_btn)
                log_action(" Clicked 'Save Price Adjustment' button", log_file_path=log_file_path)

                yes_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled")))
                driver.execute_script("arguments[0].click();", yes_button)
                log_action(" Clicked 'Yes' on confirmation ", log_file_path=log_file_path)
                time.sleep(2)

                wait_and_click_ok(driver,timeout=20)
                log_action(" Clicked 'OK' on success message ", log_file_path=log_file_path)
                WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
                time.sleep(5)
                
                WebDriverWait(driver, 15).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled")))
                log_action(" Confirmation  closed successfully", log_file_path=log_file_path)

                driver.save_screenshot(os.path.join(screenshots_folder, "Option1_PromoSaved.png"))

                back_button = wait.until(EC.element_to_be_clickable((By.ID, "goBackToOptionsBtn")))
                driver.execute_script("arguments[0].click();", back_button)
                log_action("Clicked Back to Options button", log_file_path=log_file_path)

                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-component='promoOptions']")))
                log_action(" Promo options are now visible again", log_file_path=log_file_path)
                time.sleep(2)
             
                promo_option_2 =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//h6[text()='Option 2: Adjust Unit Price']/ancestor::label")))
                driver.execute_script("arguments[0].click();", promo_option_2)
                log_action("Selected Option 2: Adjust Unit Price", log_file_path=log_file_path)
                WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
                time.sleep(5)

                modal_body = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-body.pb-4")))
                price_management_section = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-component='priceManagement'].active")))
                driver.save_screenshot(os.path.join(screenshots_folder, "AdjustPrice_Option2_Selected.png"))

                # Enter New Price
                new_price = driver.find_element(By.NAME, "PriceAdjustments[0].UnitPrice")
                new_price.clear()
                human_like_typing(new_price, str(update_data["Unit Price"]))
                log_action(f"Entered New Unit Price: {update_data['Unit Price']}", log_file_path=log_file_path)

                # Start Date & Time
                set_future_date(driver, wait, "PriceAdjustments[0].EffectiveFr", days_ahead=1)
                log_action("Set Future Start Date for Price Adjustment", log_file_path=log_file_path)
                driver.save_screenshot(os.path.join(screenshots_folder, "Option2_PriceDetails.png"))

                # Save Price Adjustment
                save_btn = wait.until(EC.element_to_be_clickable((By.ID, "savePriceAdjustmentBtn")))
                driver.execute_script("arguments[0].click();", save_btn)
                log_action(" Clicked 'Save Price Adjustment' button for Option 2", log_file_path=log_file_path)

                yes_button_2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled")))
                driver.execute_script("arguments[0].click();", yes_button_2)
                log_action(" Clicked 'Yes' on confirmation ", log_file_path=log_file_path)
                time.sleep(2) 

                wait_and_click_ok(driver,timeout=30)
                log_action(" Clicked 'OK' on success message ", log_file_path=log_file_path)
                driver.save_screenshot(os.path.join(screenshots_folder, "Option2_PriceSaved.png"))
                time.sleep(2)

                close_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-close")))
                driver.execute_script("arguments[0].click();", close_btn)
                log_action("Closed Price Management modal", log_file_path=log_file_path)

        except Exception as e:
                log_action(f" Failed to select 'Run a Special Promotion' option: {str(e)}", log_file_path=log_file_path)

        time.sleep(10)

         # Bulk Feature
        try:

                # Search box
                search_box_4 = wait.until(EC.presence_of_element_located((By.ID, "managementSearch")))
                search_box_4.clear()
                human_like_typing(search_box_4, service_name)
                log_action(f"Searched for service: {service_name}", log_file_path=log_file_path)
                time.sleep(3)
                driver.save_screenshot(os.path.join(screenshots_folder, "Searched_Product.png"))
            
                target_row_4 = find_service_row(driver, service_name)
                if not target_row:
                    raise Exception(f"Service '{service_name}' not found in table.")

                # --- CLICK CHECKBOX ---
                try:
                    checkbox4 = target_row_4.find_element(By.CSS_SELECTOR, "td:first-child input[type='checkbox']")
                    driver.execute_script("arguments[0].click();", checkbox4)
                    log_action("Selected service checkbox4", log_file_path=log_file_path)
                except Exception as e:
                    log_error(f"Failed to click checkbox4: {str(e)}\n{traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
                    raise
            
                # Create BUlk Feature
                bulk_feature_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "createBulkOrderButton")))
                driver.execute_script("arguments[0].click();", bulk_feature_button)
                log_action("Clicked Create Bulk Feature button", log_file_path=log_file_path)
                wait = WebDriverWait(driver, 10)

                # Search Client List

                if search_and_select_client(driver, "Christian", "CHRISTIAN  TESTER"):
                    log_action("Client selection successful",log_file_path=log_file_path)
                else:
                    log_action("Client selection failed",log_file_path=log_file_path)
                    
                # Select address
                if search_and_select_address(driver, "MALIGAYA", "MALIGAYA"):
                    log_action("Address selection successful",log_file_path=log_file_path)
                else:
                    log_action("Address selection failed",log_file_path=log_file_path)
    

                # Submit Bulk Feature
                submit_bulk_feature = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "submit-bulk-order-button")))
                driver.execute_script("arguments[0].click();", submit_bulk_feature)
               
                WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
                time.sleep(5)
                driver.save_screenshot(os.path.join(screenshots_folder, "Bulk Product.png"))

                table = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "orderAdjustmentTable")))
                WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#orderAdjustmentTable tbody tr")))
                log_action("Order Adjustment loaded successfully", log_file_path=log_file_path)

                shipping_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.shipping-input[data-client-id='0']")))
                shipping_input.clear()
                shipping_input.send_keys("150") 
                log_action("Entered Shipping Amount: 150", log_file_path=log_file_path)
                time.sleep(2)

                fill_order_row(driver, wait, client_id=0, adjustment=2299, shipping=150, tax="VAT")
                log_action("Filled order row with adjustment, shipping, and tax details", log_file_path=log_file_path)
                driver.save_screenshot(os.path.join(screenshots_folder, ' Bulk_Feature_Filled.png'))
                time.sleep(2)

                finalize_bulk_order = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "finalize-bulk-order-button")))
                driver.execute_script("arguments[0].click();", finalize_bulk_order)
                log_action("Clicked Finalize Bulk Feature button", log_file_path=log_file_path)
                time.sleep(10)
                WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
                time.sleep(2)

                service_table = wait.until(EC.presence_of_element_located((By.ID, "servicemanagemenTable")))
                log_action("Table is diplay",log_file_path=log_file_path)

                # Export
                export_button = wait.until(EC.element_to_be_clickable((By.ID, "exportButton")))
                driver.execute_script("arguments[0].click()", export_button)
                log_action("Clicked Export Button", log_file_path=log_file_path)
                time.sleep(2)

              # store original window
                original_window = driver.current_window_handle
                log_action("Stored original window handle", log_file_path=log_file_path)

                # click the payment link (using JS click is fine if needed)
                payment_link = wait.until(EC.element_to_be_clickable((By.ID, "payment-button-0")))
                driver.execute_script("arguments[0].click()", payment_link)
                log_action("Clicked Payment Link Button", log_file_path=log_file_path)
                WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
                time.sleep(5)
                driver.save_screenshot(os.path.join(screenshots_folder, 'Payment_Windows.png'))

                # Wait for the new window/tab to appear
                WebDriverWait(driver, 30).until(lambda d: len(d.window_handles) > 1)
                log_action("New window opened for payment link", log_file_path=log_file_path)
               
                # Switch to the new window
                new_window = [window for window in driver.window_handles if window != original_window][0]
                driver.switch_to.window(new_window)
                log_action("Switched to new payment window", log_file_path=log_file_path)

                # Wait 5 seconds before closing
                time.sleep(5)

                # Close the new window
                driver.close()
                log_action("Closed new payment window after 5 seconds", log_file_path=log_file_path)

                # Switch back to the original window
                driver.switch_to.window(original_window)
                log_action("Switched back to original window", log_file_path=log_file_path)

        except Exception as e:
                log_action(f" Failed to select 'Bulk Feature: {str(e)}", log_file_path=log_file_path)

    except Exception as e:
        error_message = f"Critical error in Service Dashboard: {traceback.format_exc()}"
        log_error(error_message, log_file_path=log_file_path, driver=driver)
        driver.save_screenshot(os.path.join(screenshots_folder, 'Critical_Error.png'))
        raise Exception(error_message)
