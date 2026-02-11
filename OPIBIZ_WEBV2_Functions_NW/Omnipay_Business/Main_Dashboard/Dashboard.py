# Standard-library imports
import os                      # file / path operations
import time                    # for sleep / delays / timing
import traceback               # for printing exception tracebacks / debugging

# Third-party imports (Selenium WebDriver)
from selenium.webdriver.common.by import By              # for element location in Selenium
from selenium.webdriver.support.wait import WebDriverWait  # explicit wait helper
from selenium.webdriver.support import expected_conditions as EC  # wait condition helpers

# Local / project-specific imports
from Utility import (
    log_action,    # custom action logging
    log_error,     # custom error logging
    clear_folder,  # utility to clear directories / cleanup
    parse_table,   # helper to parse UI / HTML tables
    clean_text     # helper to normalize / clean text from UI
)
from path_config import SCD_MODULE_PATHS  # project config: module paths


def Main_Dashboard(driver, wait):
    # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['Dashboard']['log']
    screenshots_folder = SCD_MODULE_PATHS['Dashboard']['screenshots']

    # Ensure log and screenshot folders exist
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    os.makedirs(screenshots_folder, exist_ok=True)

    # Clear old screenshots before test run
    clear_folder(screenshots_folder=screenshots_folder)

    try:
        # --- MAIN DASHBOARD ---
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[3]/div[1]/div/div/div')))
        log_action("Main Dashboard loaded successfully", log_file_path=log_file_path)
        time.sleep(30)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        driver.save_screenshot(os.path.join(screenshots_folder, 'Main_Dashboard_Loaded.png'))

        #  FIXED: find_element (not find_elements) for single count element
        new_orders = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'newOrdersAndServicesCount')))
        log_action(f"New orders/Service Orders count: {new_orders.text}", log_file_path=log_file_path)

        processing = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'ordersAndServicesForProcessingCount')))
        log_action(f"Orders/Service Orders for Processing count: {processing.text}", log_file_path=log_file_path)

        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        driver.save_screenshot(os.path.join(screenshots_folder, 'Main_Dashboard.png'))

        # --- SETTLE AVAILABLE BALANCE ---
        current_balance_el = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'currentBalance')))
        current_balance = clean_text(current_balance_el.text)
        log_action(f"Current Balance: {current_balance}", log_file_path=log_file_path)

        available_balance_el = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'availableBalance')))
        available_balance = clean_text(available_balance_el.text)
        log_action(f"Available Balance: {available_balance}", log_file_path=log_file_path)

        settle_available_balance = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[3]/div[1]/div/div/div/div[2]/div[2]/div/div/div/div/div[3]/a')))
        driver.execute_script("arguments[0].click();", settle_available_balance)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[3]/div[1]')))
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(10)
        driver.save_screenshot(os.path.join(screenshots_folder, 'Transfer_Funds_to_Settlement_Account.png'))
        log_action("Clicked Settle Available Balance", log_file_path=log_file_path)

        # --- BACK TO DASHBOARD ---
        back_to_dashboard = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[3]/div[1]/div[1]/button/p')))
        driver.execute_script("arguments[0].click();", back_to_dashboard)
        log_action("Back to Main Dashboard", log_file_path=log_file_path)

        # --- GENERATE QR ---
        generate_qr = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'generateQRBtn')))
        driver.execute_script("arguments[0].click();", generate_qr)
        log_action("Clicked Generate QR", log_file_path=log_file_path)

        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(10)
        driver.save_screenshot(os.path.join(screenshots_folder, 'Generate_QR_Code.png'))

        back_to_dashboard = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[3]/div[1]/div/div/button')))
        driver.execute_script("arguments[0].click();", back_to_dashboard)
        log_action("Back to Main Dashboard", log_file_path=log_file_path)

        # --- LAST 10 ORDERS TABLE ---
        orders_table = driver.find_element(By.XPATH, '//*[@id="latestOrdersTbl"]/tbody')
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", orders_table)
        orders_list = parse_table(driver, '//*[@id="latestOrdersTbl"]/tbody', log_file_path, "Latest Orders Table")
        log_action("Latest Orders Table displayed successfully", log_file_path=log_file_path)

        # --- CREATE ORDER VIEW ---
        create_order_viewed = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'createOrderBtn')))
        driver.execute_script("arguments[0].click();", create_order_viewed)
        log_action("Clicked Create Order", log_file_path=log_file_path)

        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(10)
        driver.save_screenshot(os.path.join(screenshots_folder, 'Create_Order_Page.png'))

        # --- BACK TO DASHBOARD ---
        back_to_dashboard = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[3]/div[1]/div/div/button/p')))
        driver.execute_script("arguments[0].click();", back_to_dashboard)
        log_action("Back to Main Dashboard", log_file_path=log_file_path)

        # --- LAST 10 SERVICE ORDERS TABLE ---
        service_order_table = driver.find_element(By.XPATH, '//*[@id="latestServiceOrdersTbl"]/tbody')
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", service_order_table)
        service_list = parse_table(driver, '//*[@id="latestServiceOrdersTbl"]/tbody', log_file_path, "Latest Service Orders Table")
        log_action("Latest Service Orders Table displayed successfully", log_file_path=log_file_path)

         # --- CREATE SERVICE ORDER VIEW ---
        create_service_order_viewed = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'createInvoiceBtn')))
        driver.execute_script("arguments[0].click();", create_service_order_viewed)
        log_action("Clicked Create Order", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(10)
        driver.save_screenshot(os.path.join(screenshots_folder, 'Create_Service_Order_Page.png'))

        back_to_dashboard = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[3]/div[1]/div/div/button/p')))
        driver.execute_script("arguments[0].click();", back_to_dashboard)
        log_action("Back to Main Dashboard", log_file_path=log_file_path)

        # --- CREATE BOOKING ---
        create_booking_viewed = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, ".//a[contains(@href,'BookingAndAppointments') and contains(normalize-space(.),'Create Booking')]")))
        driver.execute_script("arguments[0].click();", create_booking_viewed)
        log_action("Clicked Create Booking", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(10)
        driver.save_screenshot(os.path.join(screenshots_folder, 'Booking.png'))

        # --- BACK TO DASHBOARD ---
        back_to_dashboard = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[3]/div[1]/div/div[1]/button/p')))
        driver.execute_script("arguments[0].click();", back_to_dashboard)
        log_action("Back to Main Dashboard", log_file_path=log_file_path)

        # --- INVENTORY VIEWED ---
        inventory_viewed = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[3]/div[2]/div/div[3]')))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", inventory_viewed)
        log_action("Inventory section viewed successfully", log_file_path=log_file_path)

        # --- ADD NEW PRODUCT ---
        add_new_product = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'addNewProductBtn')))
        driver.execute_script("arguments[0].click();", add_new_product)
        log_action("Clicked Add New Product", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(10)
        driver.save_screenshot(os.path.join(screenshots_folder, 'Add_New_Product_Page.png'))

        # --- BACK TO DASHBOARD ---
        back_to_dashboard = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mainContent"]/div/button/p')))
        driver.execute_script("arguments[0].click();", back_to_dashboard)
        log_action("Back to Main Dashboard", log_file_path=log_file_path)

        # --- INVENTORY UPDATE ---
        inventory_update = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'inventoryUpdateBtn')))
        driver.execute_script("arguments[0].click();", inventory_update)
        log_action("Clicked Inventory Update", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(10)
        driver.save_screenshot(os.path.join(screenshots_folder, 'Inventory_Update_Page.png'))

        # --- BACK TO DASHBOARD ---
        back_to_dashboard = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[3]/div[1]/div[1]/button/p')))
        driver.execute_script("arguments[0].click();", back_to_dashboard)
        log_action("Back to Main Dashboard", log_file_path=log_file_path)

       # 3. INVENTORY HISTORY
        try:
            print("Parsing Inventory History table...")
            inventory_history_xpath = '//*[@id="inventoryHistoryPartialTable"]/tbody'
            inventory_history_data = parse_table(driver, inventory_history_xpath, log_file_path, "Inventory History")
            print(f"Parsed {len(inventory_history_data) if inventory_history_data else 0} inventory records")
        except Exception as e:
            print(f"Error parsing Inventory History: {e}")
            log_error(f"Error parsing Inventory History: {str(e)}", log_file_path=log_file_path)
            inventory_history_data = []

    except Exception as e:
        error_message = f"Element not found or interaction failed: {repr(e)}"
        log_error(error_message, log_file_path=log_file_path, driver=driver)
        print(traceback.format_exc())
