# ---------------------------
# Standard library imports
# ---------------------------
import os                   # File and directory operations
import time                 # Sleep/delays or timestamp operations
import traceback            # Capture stack traces for exception handling
import random               # Generate random values for testing (e.g., random service/product)

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
from Utility import (                     # Custom helper functions for automation
    log_action,                           # Log successful actions for debugging/auditing
    log_error,                             # Log exceptions/errors for diagnostics
    clear_folder,                          # Clear temporary folders or files
    human_like_typing,                     # Simulate realistic typing in UI automation
    product_data,                           # Data structure/helper for product information
    wait_and_click_ok,                      # Wait for a dialog/button and click safely
    get_latest_product_name_from_log,       # Fetch the latest product name from logs
    upload_image_product,                   # Upload product images in UI forms
    set_start_date,                         # Set start date in UI forms or calendar pickers
    set_end_date,                           # Set end date in UI forms or calendar pickers
    set_post_promo_price,                    # Set post-promo price in product forms
    set_future_date,                         # Set a future date for scheduling or testing
    fill_order_row,                          # Fill order row in UI forms or tables
    search_and_select_client,                # Search and select a client in forms/dropdowns
    search_and_select_address,               # Search and select an address in forms/dropdowns
)

def MProduct(driver, wait):
    
    # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['MProduct']['log']
    screenshots_folder = SCD_MODULE_PATHS['MProduct']['screenshots']

    # Clear old files before test run  
    clear_folder(screenshots_folder=screenshots_folder)

    try:
            
            # === NAVIGATE TO SELLER CENTER DASHBOARD ===
            # For Debugging Purposes uncomment the line below per module
            # print("Navigating to Seller Center Dashboard...")
            # Seller_Center = wait.until(EC.element_to_be_clickable((By.XPATH,  "//a[@data-bs-title='Seller Center' and @data-bs-toggle='tooltip' and .//span[text()='Seller Center']]")))
            # driver.execute_script("arguments[0].click()", Seller_Center)
            # log_action("Clicked Seller Center", log_file_path=log_file_path)
            # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

            # Product_Management =  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"//a[@data-bs-title='Product Management' and @data-bs-toggle='tooltip' and .//span[text()='Product Management']]")))
            # driver.execute_script("arguments[0].click();", Product_Management)
            # log_action("Clicked Product Management", log_file_path=log_file_path)
            # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            # time.sleep(5)
            # driver.save_screenshot(os.path.join(screenshots_folder, "Product_Management.png"))

            Manage_Product = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@onclick, 'navToManageProduct') and contains(., 'Manage Product')]")))
            driver.execute_script("window.scrollTo(0, 0);",Manage_Product)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", Manage_Product)
            log_action("Clicked Create New Product", log_file_path=log_file_path)
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            time.sleep(2)
            driver.save_screenshot(os.path.join(screenshots_folder, "Manage Product.png"))

            # Extract logs from CNProduct for reuse
            logs_reuse_path = SCD_MODULE_PATHS['CNProduct']['log']
            product_name = get_latest_product_name_from_log(logs_reuse_path)

            if not product_name:
                print("  No product name found in CNProduct log.")
                return

            log_action(f"Searching for product: {product_name}", log_file_path=log_file_path)

            # Search box
            search_box = wait.until(EC.visibility_of_element_located((By.ID, "searchTable")))
            search_box.clear()
            human_like_typing(search_box, product_name)
            log_action(f"Searched for product: {product_name}", log_file_path=log_file_path)
            time.sleep(3)
            driver.save_screenshot(os.path.join(screenshots_folder, "Searched_Product.png"))
        
            checkbox = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#manageProductTable tbody tr:first-child td:first-child input[type="checkbox"]')))
            try:
                driver.execute_script("arguments[0].click();", checkbox)
                time.sleep(2)
                log_action("Selected first product checkbox", log_file_path=log_file_path)
            except Exception:
                driver.execute_script("arguments[0].click();", checkbox)
                log_error(f"Failed to click checkbox4: {str(e)}\n{traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
                raise
            
            # Edit Product
            edit_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(@href, '/ProductManagement/NewProduct') and contains(@href, 'type=edit')])[1]")))
            driver.execute_script("arguments[0].click();", edit_button)
            log_action("Clicked first Edit button", log_file_path=log_file_path)
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

            update_data = product_data()

            # Product Value
            product_value = driver.find_element(By.ID, "Product.ProductTags.TagValue")
            product_value.clear()
            human_like_typing(product_value, str(update_data["Product Value"]))
            log_action(f"Entered Menu Value: {update_data['Product Value']}", log_file_path=log_file_path)
            time.sleep(2)
            driver.save_screenshot(os.path.join(screenshots_folder, ' Product_Value_Edited.png'))

            # Submit
            save_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'saveProduct')))
            driver.execute_script("arguments[0].scrollIntoView({block: 'end'});", save_btn)
            time.sleep(2)
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
            
            driver.save_screenshot(os.path.join(screenshots_folder, ' Product_Updated.png'))

            # Success
            back_to_manage_product = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@onclick, 'navToManageProduct')]")))
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", back_to_manage_product)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", back_to_manage_product)
            log_action("Clicked Manage Product button", log_file_path=log_file_path)
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

            # Search box
            search_box_2 = wait.until(EC.visibility_of_element_located((By.ID, "searchTable")))
            search_box_2.clear()
            human_like_typing(search_box_2, product_name)
            log_action(f"Searched for product: {product_name}", log_file_path=log_file_path)
            time.sleep(3)
            driver.save_screenshot(os.path.join(screenshots_folder, "Searched_Product.png"))
        
            checkbox_2 =  checkbox_2 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#manageProductTable tbody tr:nth-child(1) td:nth-child(1) input[type='checkbox']")))
            try:
                driver.execute_script("arguments[0].click();", checkbox_2)
                time.sleep(2)
                log_action("Selected first product checkbox", log_file_path=log_file_path)
            except Exception:
                driver.execute_script("arguments[0].click();", checkbox_2)
                log_error(f"Failed to click checkbox4: {str(e)}\n{traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
                raise

            # View Product
            view_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/ProductManagement/NewProduct') and contains(@href, 'type=view')]")))
            driver.execute_script("arguments[0].click();", view_button)
            log_action("Clicked first View button in Manage Product table", log_file_path=log_file_path)
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            driver.save_screenshot(os.path.join(screenshots_folder, ' Product_View.png'))

            back_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'Back')]")))
            driver.execute_script("arguments[0].click();", back_button)
            log_action("Clicked Back button", log_file_path=log_file_path)
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

            # Upload photo
            image_folder = r"D:\Bastion\SQA_QualityEnterprise\SoftwareTesting\Projects\Common\Automation\OPI\Files\Images\Product"

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

            # Make it interactable
            driver.execute_script("arguments[0].style.display = 'block';", upload_input)

            # Send the random file
            upload_input.send_keys(random_image)

            # Click upload button if needed
            driver.find_element(By.ID, "uploadAllBtn").click()
            log_action("Uploaded photo", log_file_path=log_file_path)

            swal_popup = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.swal2-popup.swal2-show")))
            log_action("Upload Images Successfully appeared", log_file_path=log_file_path)
            driver.save_screenshot(os.path.join(screenshots_folder, ' Image_Uploaded.png'))
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

            # Upload again to close the modal
            upload_again_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class,'btn') and text()='Upload again']")))
            driver.execute_script("arguments[0].click();", upload_again_btn)
            log_action("Clicked Upload Again to close the modal", log_file_path=log_file_path)
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')  

            try:

                # Search box
                search_box_3 = wait.until(EC.visibility_of_element_located((By.ID, "searchTable")))
                search_box_3.clear()
                human_like_typing(search_box_3, product_name)
                log_action(f"Searched for product: {product_name}", log_file_path=log_file_path)
                time.sleep(3)
                driver.save_screenshot(os.path.join(screenshots_folder, "Searched_Product.png"))
            
                checkbox_3 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#manageProductTable tbody tr:first-child td:first-child input[type="checkbox"]')))
                try:
                    driver.execute_script("arguments[0].click();", checkbox_3)
                    log_action("Selected first product checkbox", log_file_path=log_file_path)
                except Exception:
                    driver.execute_script("arguments[0].click();", checkbox_3)
                    log_error(f"Failed to click checkbox4: {str(e)}\n{traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
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
                driver.save_screenshot(os.path.join(screenshots_folder, "AdjustPrice_Modal_Visible.png"))

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
                time.sleep(2)

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
        
                WebDriverWait(driver, 15).until_not(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled")))
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

                wait_and_click_ok(driver,timeout=20)
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
                search_box_4 = wait.until(EC.visibility_of_element_located((By.ID, "searchTable")))
                search_box_4.clear()
                human_like_typing(search_box_4, product_name)
                log_action(f"Searched for product: {product_name}", log_file_path=log_file_path)
                time.sleep(3)
                driver.save_screenshot(os.path.join(screenshots_folder, "Searched_Product.png"))
            
                checkbox_4 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#manageProductTable tbody tr:first-child td:first-child input[type="checkbox"]')))
                try:
                    driver.execute_script("arguments[0].click();", checkbox_4)
                    time.sleep(2)
                    log_action("Selected first product checkbox", log_file_path=log_file_path)
                except Exception:
                    driver.execute_script("arguments[0].click();", checkbox_4)
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
                WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#orderAdjustmentTable tbody tr")))
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

                service_table = wait.until(EC.visibility_of_element_located((By.ID, "priceManagementModal")))
                log_action("Table is diplay",log_file_path=log_file_path)

                # Export
                export_button = wait.until(EC.element_to_be_clickable((By.ID, "exportButton")))
                driver.execute_script("arguments[0].click()", export_button)
                log_action("Clicked Export Button", log_file_path=log_file_path)
                time.sleep(2)

                # Get the current window handle
                original_window = driver.current_window_handle
                log_action("Stored original window handle", log_file_path=log_file_path)

                # Click the Payment Link Button   
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
            error_message = f"Critical error in Seller Dashboard: {traceback.format_exc()}"
            log_error(error_message, log_file_path=log_file_path, driver=driver)
            driver.save_screenshot(os.path.join(screenshots_folder, 'Critical_Error.png'))
            raise