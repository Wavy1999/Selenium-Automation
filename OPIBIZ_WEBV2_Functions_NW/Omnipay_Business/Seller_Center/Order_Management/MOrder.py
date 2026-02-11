# ---------------------------
# Standard library imports
# ---------------------------
import os                   # File and directory operations
import time                 # Sleep/delays or timestamp operations
import re                   # Regular expressions for string matching/manipulation
from datetime import datetime  # Date and time manipulations

# ---------------------------
# Third-party imports (Selenium WebDriver)
# ---------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

# ---------------------------
# Local / project-specific imports
# ---------------------------
from path_config import SCD_MODULE_PATHS  # Project-specific constants for module paths
from Utility import (                     # Custom utility functions for automation
    log_action,                           # Log successful actions for debugging/auditing
    update_profile_data,                  # Update profile-related data in the UI
    clear_folder,                          # Clear temporary folders/files
    wait_and_click_ok,                     # Wait for a dialog/button and click safely
    get_latest_order_from_log,            # Retrieve latest order from log for chaining
    human_like_typing,                     # Simulate realistic typing in UI automation
)


def MOrder(driver, wait):
    # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['MOrder']['log']
    screenshots_folder = SCD_MODULE_PATHS['MOrder']['screenshots']

    # Clear old files before test run
    clear_folder(screenshots_folder=screenshots_folder)

    # driver.refresh()
    # log_action("For better running",log_file_path=log_file_path)

    try:
        # =========================
        # Navigate to Manage Orders
        # =========================
        # Uncomment this for solo run this module
        # print("Navigating to Seller Center Dashboard...")

        # Seller_Center = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-bs-title='Seller Center' and .//span[text()='Seller Center']]")))
        # driver.execute_script("arguments[0].click()", Seller_Center)
        # log_action("Clicked Seller Center", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(3)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Seller_Center.png"))

        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # Order_Management = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[.//span[contains(text(), 'Order Management')]]")))
        # driver.execute_script("arguments[0].click();", Order_Management)


        # log_action("Clicked Order Management", log_file_path=log_file_path)

        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(5)

        Manage_Order = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/ManageOrder']")))
        driver.execute_script("arguments[0].click();", Manage_Order)
        log_action("Clicked Manage Order", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshots_folder, "Receipt.png"))

        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        manage_orders_element = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, "manage-order")))
        log_action("'Manage Orders' element is visible", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(20)
        driver.save_screenshot(os.path.join(screenshots_folder, "Manage_Order.png"))

        # Get latest service name from COrder log
        logs_reuse_path = SCD_MODULE_PATHS['COrder']['log']
        order_name = get_latest_order_from_log(logs_reuse_path)
        if not order_name:
            print("No order name found in Create_Order log.")
            return
        log_action(f"Searching for service: {order_name}", log_file_path=log_file_path)

        # =========================
        # Search and Filter Section
        # =========================
        search_field = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "searchTable")))
        search_field.clear()
        human_like_typing(search_field,"UNPAID")
        time.sleep(20)

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#manageOrderTable tbody tr")))

        driver.save_screenshot(os.path.join(screenshots_folder, "Searched_Order.png"))
        log_action(f"Searched for service: UNPAID", log_file_path=log_file_path)

        filter_payment = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "statusFilter")))
        Select(filter_payment).select_by_value("all")
        log_action("Selected 'All Orders' from Payment Status filter", log_file_path=log_file_path)

        service_status = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "orderStatusFilter")))
        Select(service_status).select_by_value("all")
        log_action("Selected 'All Orders' from Service Order Status filter", log_file_path=log_file_path)

        today_str = datetime.now().strftime("%m/%d/%Y")

        date_range = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "daterange")))
        date_range.clear()
        date_range.send_keys(f"{today_str} - {today_str}")
        date_range.send_keys(Keys.RETURN)
        log_action("Applied Date Range filter", log_file_path=log_file_path)

        # =========================
        # Select Order and View Profile
        # =========================
        checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#manageOrderTable tbody tr:first-child td:first-child input[type="checkbox"]')))
        try:
            checkbox.click()
        except Exception:
            driver.execute_script("arguments[0].click();", checkbox)

        log_action("Checked first order row", log_file_path=log_file_path)
        driver.save_screenshot(os.path.join(screenshots_folder, "First_Order_Row_Checked.png"))

        order_profile_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="manageOrderTable"]/tbody/tr[1]//a[text()="Order Profile"]')))
        driver.execute_script("arguments[0].click();", order_profile_btn)
        log_action("Viewed Order Profile", log_file_path=log_file_path)

        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
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

        wait_and_click_ok(driver)
        log_action("Clicked OK", log_file_path=log_file_path)

        # =========================
        # Manage Orders and Receive Payment
        # =========================
        # manage_orders_url = "http://vm-app-dev01:9001/ManageOrder#" hotel
        manage_orders_url = "http://beta-opibizscd.paybps.ovpn/ManageOrder"
        driver.get(manage_orders_url)
        log_action("Navigated to Manage Order page", log_file_path=log_file_path)

        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'manageOrderTable')))
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="manageOrderTable"]/tbody/tr[1]')))
        time.sleep(20)
        log_action("Manage Order page loaded", log_file_path=log_file_path)

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
        # manage_orders_url = "http://vm-app-dev01:9001/ManageOrder#"
        manage_orders_url = "http://beta-opibizscd.paybps.ovpn/ManageOrder"
        driver.get(manage_orders_url)
        log_action("Navigated to Manage Order", log_file_path=log_file_path)

        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'manageOrderTable')))
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="manageOrderTable"]/tbody/tr[1]')))

        create_new_order_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Create New  Order')]")))
        driver.execute_script("arguments[0].click();", create_new_order_btn)
        log_action("Clicked Create New Order", log_file_path=log_file_path)
        time.sleep(10)
        driver.save_screenshot(os.path.join(screenshots_folder, "Create_New_Order_Page.png"))

        # manage_orders_url = "http://vm-app-dev01:9001/ManageOrder#"
        manage_orders_url = "http://beta-opibizscd.paybps.ovpn/ManageOrder"
        driver.get(manage_orders_url)
        log_action("Navigated to Manage Order", log_file_path=log_file_path)

    except TimeoutException as e:
        log_action(f"Timeout error: {str(e)}", log_file_path=log_file_path)
        driver.save_screenshot(os.path.join(screenshots_folder, "Timeout_Error.png"))
        raise

    except Exception as e:
        log_action(f"An error occurred: {e}", log_file_path=log_file_path)
        driver.save_screenshot(os.path.join(screenshots_folder, "General_Error.png"))
        raise
