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
from selenium.common.exceptions import TimeoutException  # Handle Selenium timeouts

# ---------------------------
# Local / project-specific imports
# ---------------------------
from path_config import SCD_MODULE_PATHS  # Project-specific constants for module paths
from Utility import (                     # Custom helper functions for automation
    log_action,                           # Log successful actions for debugging/auditing
    log_error,                             # Log exceptions/errors for diagnostics
    clear_folder,                          # Clear temporary folders or files
    parse_table,                            # Parse table elements from the UI
)

def SDashboard(driver, wait):
    # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['SDashboard']['log']
    screenshots_folder = SCD_MODULE_PATHS['SDashboard']['screenshots']

    # Clear old files before test run  
    clear_folder(screenshots_folder=screenshots_folder)

    try:
        # === NAVIGATE TO SELLER CENTER DASHBOARD ===
        print("Navigating to Seller Center Dashboard...")
        Seller_Center = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/header/div/nav/ul/li[2]/a")))
        driver.execute_script("arguments[0].click()", Seller_Center)
        log_action("Clicked Seller Center", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        Seller_Center_Dashboard = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/header/div/nav/ul/li[2]/ul/li[1]/a")))
        driver.execute_script("arguments[0].click()", Seller_Center_Dashboard)
        log_action("Clicked Seller Center Dashboard", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(10)
     
        # === WAIT FOR DASHBOARD TO LOAD ===
        print("Waiting for dashboard to load...")
        metric_container = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.metrics-container")))
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'card-metrics')))
        log_action("Seller Dashboard loaded successfully", log_file_path=log_file_path)

        invoiced_body = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[3]/div[1]/section[1]/div/div[2]')))
        log_action("Invoiced Amount panel found", log_file_path=log_file_path)
        time.sleep(10)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        driver.save_screenshot(os.path.join(screenshots_folder, 'SDashboard_Main.png'))

        # === CAPTURE DASHBOARD METRICS ===
        print("Capturing dashboard metrics...")
        try:
            orders_processing = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'widget-content-processing-orders')))
            log_action(f"Orders for Processing: {orders_processing.text}", log_file_path=log_file_path)
        except TimeoutException:
            log_error("Orders for Processing widget not found", log_file_path=log_file_path)

        try:
            unpaid_orders = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'widget-content-unpaid-orders')))
            log_action(f"Unpaid Orders: {unpaid_orders.text}", log_file_path=log_file_path)
        except TimeoutException:
            log_error("Unpaid Orders widget not found", log_file_path=log_file_path)

        try:
            completed_sales = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'widget-content-total-sales')))
            log_action(f"Total Completed Sales: {completed_sales.text}", log_file_path=log_file_path)
        except TimeoutException:
            log_error("Total Completed Sales widget not found", log_file_path=log_file_path)

        # === CASH COLLECTION BALANCE ===
        try:
            current_bal = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'currentBalance')))
            log_action(f"Cash Collection Balance: {current_bal.text}", log_file_path=log_file_path)

            available_bal = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'availableBalance')))
            log_action(f"Available Balance: {available_bal.text}", log_file_path=log_file_path)
        except TimeoutException:
            log_error("Cash Collection Balance widgets not found", log_file_path=log_file_path)

        # === SETTLE AVAILABLE BALANCE ===
        print("Testing Settle Available Balance...")
        try:
            settle_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="collectionBalance"]/button')))
            driver.execute_script("arguments[0].scrollIntoView(true);", settle_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", settle_button)
            log_action("Clicked Settle Available Balance button", log_file_path=log_file_path)

            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'ecopay-container')))
            log_action("Settle Available Balance modal opened", log_file_path=log_file_path)
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            time.sleep(10)
            driver.save_screenshot(os.path.join(screenshots_folder, 'Settle_Balance_Modal.png'))

            # Back to Seller Dashboard
            back_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[3]/div[1]/div[1]/button/p')))
            driver.execute_script("arguments[0].click();", back_button)
            log_action("Clicked Back to Seller Dashboard button", log_file_path=log_file_path)
            time.sleep(2)
        except TimeoutException:
            log_error("Could not interact with Settle Available Balance section", log_file_path=log_file_path)

        # === LAST 10 ORDERS TABLE ===
        print("Processing Last 10 Orders section...")
        try:
            viewed_all_orders = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'viewLastOrderBtn')))
            driver.execute_script("arguments[0].scrollIntoView(true);", viewed_all_orders)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", viewed_all_orders)
            log_action("Clicked View All Orders button", log_file_path=log_file_path)
            
            # Wait for the expansion animation
            time.sleep(3)
            
            # Wait for table to expand and parse it
            try:
                # Wait for the table container to have expanded class
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tableLastOrder.table--expand")))
                print(" Orders table expanded successfully")
                
                # Wait for rows to be present
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='latestOrdersTbl']//tbody//tr")))
                
                # Parse the table
                orders_table = driver.find_element(By.XPATH, '//*[@id="latestOrdersTbl"]/tbody')
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", orders_table)
                orders_list = parse_table(driver, '//*[@id="latestOrdersTbl"]/tbody', log_file_path, "Latest Orders Table")
                log_action("Latest Orders Table displayed successfully", log_file_path=log_file_path)
                
            except TimeoutException:
                log_error("Latest Orders Table not found or empty", log_file_path=log_file_path)

            # Click back to collapse
            back = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'backLastOrderBtn')))
            driver.execute_script("arguments[0].click();", back)
            log_action("Clicked Back to Seller Dashboard from Orders Table", log_file_path=log_file_path)

            # Click eye icon to view order details
            eye_icon_table = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="latestOrdersTbl"]/tbody/tr[1]/td[3]/button')))
            driver.execute_script("arguments[0].click();", eye_icon_table)
            log_action("Clicked Eye Icon to view Order Details", log_file_path=log_file_path)

            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            time.sleep(10)
            driver.save_screenshot(os.path.join(screenshots_folder, 'Last_10_Orders.png'))
            
        except TimeoutException:
            print(" View All Orders button not found")
            log_error("View All Orders button not found", log_file_path=log_file_path)
        except Exception as e:
            print(f" Error in Orders section: {str(e)}")
            log_error(f"Orders section error: {str(e)}", log_file_path=log_file_path)
   
        # === LAST 10 PAYMENTS TABLE ===
        print("Processing Last 10 Payments section...")
        try:
            # Check if payment button exists
            payment_buttons = driver.find_elements(By.ID, 'viewLastPaymentBtn')
            
            if len(payment_buttons) > 0 and payment_buttons[0].is_displayed():
                viewed_all_payment = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'viewLastPaymentBtn')))
                driver.execute_script("arguments[0].scrollIntoView(true);", viewed_all_payment)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", viewed_all_payment)
                log_action("Clicked View All Payments button", log_file_path=log_file_path)

                # Wait for expansion
                time.sleep(3)

                # Parse the payments table
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='latestPaymentsTbl']//tbody//tr")))
                    payments_table = driver.find_element(By.XPATH, '//*[@id="latestPaymentsTbl"]/tbody')
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", payments_table)
                    payment_list = parse_table(driver, '//*[@id="latestPaymentsTbl"]/tbody', log_file_path, "Latest Payment Table")
                    log_action("Latest Payments Table displayed successfully", log_file_path=log_file_path)
                    
                except TimeoutException:
                    log_error("Latest Payments Table not found or empty", log_file_path=log_file_path)

                # Click back to collapse
                back = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'backLastPaymentBtn')))
                driver.execute_script("arguments[0].click();", back)
                log_action("Clicked Back to Seller Dashboard from Payments Table", log_file_path=log_file_path)

                # Click eye icon to view payment details
                eye_icon_payment = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="latestPaymentsTbl"]/tbody/tr[1]/td[3]/button')))
                driver.execute_script("arguments[0].click();", eye_icon_payment)
                log_action("Clicked Eye Icon to view Payment Details", log_file_path=log_file_path)

                WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
                time.sleep(10)
                driver.save_screenshot(os.path.join(screenshots_folder, 'Last_10_Payments.png'))
            else:
                print(" Payment section not available")
                log_action("Payment section not available on Seller Dashboard", log_file_path=log_file_path)
                
        except TimeoutException:
            log_action("Payment section not available on Seller Dashboard", log_file_path=log_file_path)
        except Exception as e:
            print(f" Error in Payment section: {str(e)}")
            log_action("Payment section skipped", log_file_path=log_file_path)

        # === GENERATE QR ===
        print("Testing Generate QR feature...")
        try:
            qr_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[3]/div[1]/section[2]/div/div[1]/div/div[2]/button[1]')))
            driver.execute_script("arguments[0].scrollIntoView(true);", qr_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", qr_button)
            log_action("Clicked Generate QR button", log_file_path=log_file_path)

            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[3]/div[1]')))
            log_action("Generate QR page loaded", log_file_path=log_file_path)
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            time.sleep(10)
            driver.save_screenshot(os.path.join(screenshots_folder, 'Generate_QR_Page.png'))

            # Back to dashboard
            back_to_dashboard = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[3]/div[1]/div/div/button/p')))
            driver.execute_script("arguments[0].click();", back_to_dashboard)
            log_action("Clicked Back to Seller Dashboard from Generate QR page", log_file_path=log_file_path)
            time.sleep(2)
        except TimeoutException:
            log_error("Generate QR feature not available or failed to load", log_file_path=log_file_path)
        except Exception as e:
            log_error(f"Generate QR error: {str(e)}", log_file_path=log_file_path)

        # === CREATE ORDER ===
        print("Testing Create Order feature...")
        try:
            create_order_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[3]/div[1]/section[2]/div/div[1]/div/div[2]/button[2]')))
            driver.execute_script("arguments[0].scrollIntoView(true);", create_order_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", create_order_button)
            log_action("Clicked Create Order button", log_file_path=log_file_path)

            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[3]/div[1]/div')))
            log_action("Create Order page loaded", log_file_path=log_file_path)
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            time.sleep(3)
            driver.save_screenshot(os.path.join(screenshots_folder, 'Create_Order_Page.png'))

            # Back to dashboard
            back_to_dashboard_from_order = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[3]/div[1]/div/div/button')))
            driver.execute_script("arguments[0].click();", back_to_dashboard_from_order)
            log_action("Clicked Back to Seller Dashboard from Create Order page", log_file_path=log_file_path)
            time.sleep(2)
        except TimeoutException:
            log_error("Create Order feature not available or failed to load", log_file_path=log_file_path)
        except Exception as e:
            log_error(f"Create Order error: {str(e)}", log_file_path=log_file_path)

        print(" Seller Dashboard test completed successfully")
        log_action("=== Seller Dashboard Test Completed Successfully ===", log_file_path=log_file_path)

    except Exception as e:
        error_message = f"Critical error in Seller Dashboard: {traceback.format_exc()}"
        log_error(error_message, log_file_path=log_file_path, driver=driver)
        print(f"✗ {error_message}")
        driver.save_screenshot(os.path.join(screenshots_folder, 'Critical_Error.png'))
        raise