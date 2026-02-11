# ---------------------------
# Standard library imports
# ---------------------------
import os                   # File and directory operations
import time                 # Sleep/delays or timestamp operations
import re                   # Regular expressions for string matching/manipulation

# ---------------------------
# Third-party imports (Selenium WebDriver)
# ---------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException  # Handle Selenium timeouts

# ---------------------------
# Local / project-specific imports
# ---------------------------
from path_config import SCD_MODULE_PATHS  # Project-specific constants for module paths
from Utility import (                     # Custom helper functions for automation
    log_action,                           # Log successful actions for debugging/auditing
    update_profile_data,                  # Update profile data in the UI
    clear_folder,                          # Clear temporary folders or files
    wait_and_click_ok,                     # Wait for dialog/button and click safely
    search_select_order,                   # Search and select an order in UI tables/forms
    get_latest_name_from_log,              # Retrieve latest name from log for chaining
)
def MSOrder(driver, wait):
    
    # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['MSOrder']['log']
    screenshots_folder = SCD_MODULE_PATHS['MSOrder']['screenshots']
    
    # Clear old files before test run
    clear_folder(screenshots_folder=screenshots_folder)

    try:
        # Navigate: Service Order Management → Manage Service Order
        # Uncomment this per solo module run
        # Service_Center = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-bs-title='Service Center' and @data-bs-toggle='tooltip' and .//span[text()='Service Center']]")))
        # driver.execute_script("arguments[0].click()", Service_Center)
        # log_action("Clicked Service Center", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

#         # Service Order Management
#         Service_Order_Management = WebDriverWait(driver, 30).until(
#     EC.presence_of_element_located(
#         (By.XPATH, "//li[@class='ob__breadcrumb-link' and normalize-space()='Service Order Management']")
#     )
# )

#         # Force click with JavaScript
#         try:
#             driver.execute_script("arguments[0].click();", Service_Order_Management)
#             log_action("Clicked Service Order Management", log_file_path=log_file_path)
#         except Exception as e:
#             print(f"⚠️ Force click failed: {e}")
#             # Optional: retry after short wait
#             time.sleep(1)
#             driver.execute_script("arguments[0].click();", Service_Order_Management)
#             log_action("Clicked Service Order Management on retry", log_file_path=log_file_path)

#         # Give the page some time to process click
#         time.sleep(3)

#         # Take screenshot
#         driver.save_screenshot(os.path.join(screenshots_folder, "Manage_Service_Order_Flyout.png"))

#         # Wait until page is fully loaded
#         WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        Manage_Service_Orders = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/ManageOrder?type=service']")))
        driver.execute_script("arguments[0].click();", Manage_Service_Orders)
        log_action("Clicked Manage Service Order", log_file_path=log_file_path)
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshots_folder, "Manage_Service_Order_Page.png"))
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # yes_leave_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'swal2-confirm') and contains(text(),'Yes, leave page')]")))
        # driver.execute_script("arguments[0].click();", yes_leave_btn)
        # log_action("Clicked 'Yes, leave page'", log_file_path=log_file_path)
        # time.sleep(10)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        time.sleep(10)

        manage_order = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, "manage-order")))
        log_action("Manage Order page visible", log_file_path=log_file_path)

         # Get latest service name from Create_New_Service log
        logs_reuse_path = SCD_MODULE_PATHS['CSOrder']['log']
        service_name = get_latest_name_from_log(logs_reuse_path)
        if not service_name:
            print("No service name found in CSOrder log.")
            return
        log_action(f"Searching for service: {service_name}", log_file_path=log_file_path)

       # =========================
        # Search and Filter Section
        # =========================
        search_select_order(driver,wait,log_file_path)
        log_action("Checked first order row", log_file_path=log_file_path)
        driver.save_screenshot(os.path.join(screenshots_folder, "First_Order_Row_Checked.png"))

        order_profile_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="manageOrderTable"]/tbody/tr[1]//a[text()="Order Profile"]')))
        driver.execute_script("arguments[0].click();", order_profile_btn)
        log_action("Viewed Order Profile", log_file_path=log_file_path)
        
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshots_folder, "Order_Profile_Page.png"))

        # =========================
        # Update Contact & Shipping
        # =========================
        
        update_profile_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'updateContacts')))
        driver.execute_script("arguments[0].click();", update_profile_btn)
        log_action("Opened Update Contact & Shipping", log_file_path=log_file_path)

        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshots_folder, "Update_Contact_and_Shipping_Modal.png"))

        Modal = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'updateContactsModal')))
        log_action("Modal loaded", log_file_path=log_file_path)

        # Get random profile data from Excel
        profile = update_profile_data()

        # Fill form fields
        fields = {
            "mobileNumber": profile["Mobile No."],
            "HouseNumber": profile["House/Floor/Unit No."],
            "Street": profile["Block/Building/Street"],
            "PostCode": profile["Postal Code"]
        }

        for field, value in fields.items():
            element = driver.find_element(By.NAME if field != "mobileNumber" else By.ID, field)
            element.clear()
            element.send_keys(value)
            log_action(f"Updated {field}: {value}", log_file_path=log_file_path)
            time.sleep(2)

        # Country / Province / City / Barangay dropdowns
        dropdowns = {
            "CountryCode": profile["Country"],
            "Province": profile["Province"],
            "City": profile["City/Municipality"],
            "Barangay": profile["Barangay"]
        }

        for name, value in dropdowns.items():
            dropdown = wait.until(EC.element_to_be_clickable((By.NAME, name)))
            dropdown.click()
            try:
                Select(dropdown).select_by_visible_text(value)
            except Exception:
                opt = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[text()='{value}']")))
                opt.click()
            log_action(f"Selected {name}: {value}", log_file_path=log_file_path)
            time.sleep(2)

        driver.save_screenshot(os.path.join(screenshots_folder, "Updated_Contact_and_Shipping_Info.png"))

        # Save and confirm
        save_changes = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'saveChanges')))
        driver.execute_script("arguments[0].click();", save_changes)
        log_action("Clicked Save Changes", log_file_path=log_file_path)

        confirm_changes = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[6]/button[1]')))
        driver.execute_script("arguments[0].click();", confirm_changes)
        log_action("Confirmed Changes", log_file_path=log_file_path)

        wait_and_click_ok(driver,timeout=20)
        log_action("Clicked OK", log_file_path=log_file_path)

        # =========================
        # Manage Orders and Receive Payment
        # =========================
        manage_orders_url = "http://beta-opibizscd.paybps.ovpn/ManageOrder?type=service"
        driver.get(manage_orders_url)
        log_action("Navigated to Manage Service Order page", log_file_path=log_file_path)
        time.sleep(10)

        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'manageOrderTable')))
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="manageOrderTable"]/tbody/tr[1]')))

        search_select_order(driver,wait,log_file_path)
        log_action("Checked first order row", log_file_path=log_file_path)

        table = driver.find_element(By.ID, 'manageOrderTable')
        driver.execute_script("arguments[0].scrollIntoView({block: 'start'});", table)
        time.sleep(2)

        receive_payment = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="manageOrderTable"]/tbody/tr[1]//a[contains(@href, "/ReceivePayment")]')))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", receive_payment)
        driver.execute_script("arguments[0].click();", receive_payment)
        log_action("Clicked Receive Payment", log_file_path=log_file_path)

        time.sleep(3)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        driver.save_screenshot(os.path.join(screenshots_folder, "Receive_Payment_Page_Loaded.png"))

        # =========================
        # Payment Handling
        # =========================
        try:
            payment_table = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//table[.//thead//th[contains(text(), 'Order Number')]]")))
            log_action("Payment table found", log_file_path=log_file_path)
        except TimeoutException:
            log_action("Payment table not found", log_file_path=log_file_path)
            driver.save_screenshot(os.path.join(screenshots_folder, "Error_No_Payment_Table.png"))

        # Find Remaining Balance
        remaining_balance_element = None
        for attempt in range(3):
            try:
                remaining_balance_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(), 'Remaining Balance')]/ancestor::td/following-sibling::td//strong")))
                break
            except TimeoutException:
                time.sleep(3)

        if not remaining_balance_element:
            log_action("ERROR: Could not find Remaining Balance element", log_file_path=log_file_path)
            driver.save_screenshot(os.path.join(screenshots_folder, "Error_No_Remaining_Balance.png"))
            raise ValueError("Remaining Balance element not found")

        full_price_text = remaining_balance_element.text.strip()
        price_matches = re.findall(r'[\d.]+', full_price_text)
        if not price_matches:
            raise ValueError(f"No numeric value in: '{full_price_text}'")

        price_value = price_matches[0]
        log_action(f"Extracted price: ₱{price_value}", log_file_path=log_file_path)

        # Enter payment amount
        payment_input = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, 'amount')))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", payment_input)
        payment_input.clear()
        payment_input.send_keys(price_value)
        log_action(f"Entered payment amount: {price_value}", log_file_path=log_file_path)

        # Submit Payment
        submit_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Submit Payment')]]")))
        driver.execute_script("arguments[0].click();", submit_btn)
        log_action("Clicked Submit Payment", log_file_path=log_file_path)

        driver.save_screenshot(os.path.join(screenshots_folder, "Payment_Submitted.png"))
        log_action("Payment completed successfully", log_file_path=log_file_path)


        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        modal = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "swal2-popup")))
        log_action("Payment confirmation modal appeared", log_file_path=log_file_path)
        time.sleep(3)   
        driver.save_screenshot(os.path.join(screenshots_folder, "Payment_Confirmation_Modal.png"))

        confirmation_text = driver.find_element(By.ID, "swal2-html-container").text
        log_action(f"Payment Confirmation Text: {confirmation_text}", log_file_path=log_file_path)

        yes_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Yes')]")))
        driver.execute_script("arguments[0].click();", yes_btn)
        log_action("Clicked Yes on confirmation modal", log_file_path=log_file_path)
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshots_folder, "Payment_Confirmed.png"))

        # =========================
        # Create New Order
        # =========================
        manage_orders_url = "http://beta-opibizscd.paybps.ovpn/ManageOrder?type=service"
        driver.get(manage_orders_url)
        log_action("Navigated to Manage Service Order", log_file_path=log_file_path)
        time.sleep(10)

        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        create_new_service_order_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(@class, 'ob-button--create-order') and contains(text(),'Create New Service Order')]")))
        driver.execute_script("arguments[0].click();", create_new_service_order_btn)
        log_action("Clicked Create New Service Order", log_file_path=log_file_path)
        time.sleep(10)
        driver.save_screenshot(os.path.join(screenshots_folder, "Create_New_Order_Page.png"))

        manage_orders_url = "http://beta-opibizscd.paybps.ovpn/ManageOrder?type=service"
        driver.get(manage_orders_url)
        log_action("Navigated to Manage Service Order", log_file_path=log_file_path)
        time.sleep(10)

    except TimeoutException as e:
        log_action(f"Timeout error: {str(e)}", log_file_path=log_file_path)
        driver.save_screenshot(os.path.join(screenshots_folder, "Timeout_Error.png"))
        raise

    except Exception as e:
        log_action(f"An error occurred: {e}", log_file_path=log_file_path)
        driver.save_screenshot(os.path.join(screenshots_folder, "General_Error.png"))
        raise
