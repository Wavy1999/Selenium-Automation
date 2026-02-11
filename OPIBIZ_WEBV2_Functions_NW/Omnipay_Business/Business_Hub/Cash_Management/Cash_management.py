# Standard library imports
import os                  # for file system / path operations
import time                # for delays or waiting
import traceback           # to print exception tracebacks / debug info
from datetime import datetime, timedelta  # for date & time manipulation

# Third-party imports (Selenium WebDriver)
from selenium.webdriver import ActionChains  # for advanced user actions (mouse, keyboard)
from selenium.webdriver.common.by import By  # for locating elements
from selenium.webdriver.common.keys import Keys  # for keyboard key inputs
from selenium.webdriver.support.ui import WebDriverWait  # explicit wait helper
from selenium.webdriver.support import expected_conditions as EC  # wait-condition checker

# Local application / project-specific imports
from Utility import (  
    log_action,       # custom function to log actions during automation
    log_error,        # custom function to log errors/exceptions
    parse_table,      # helper to parse HTML / UI tables
    clear_folder,     # utility to clear a directory (cleanup)  
    clean_text,       # helper to clean / normalize text extracted from UI  
    open_module       # helper to open a particular module/page in UI  
)
from path_config import SCD_MODULE_PATHS  # project-specific configuration of module paths

def CashManagement(driver, wait):

    # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['CashManagement']['log']
    screenshots_folder = SCD_MODULE_PATHS['CashManagement']['screenshots']
    
    # Clear old files before test run
    clear_folder(screenshots_folder=screenshots_folder)
    driver.refresh()

    try:
        # ---------------------------
        # Navigate directly to Cash Management
        # ---------------------------
        # base_url = "http://vm-app-dev01:9001"     # ← Use your actual base URL
        # driver.get(base_url + "/EcoPay")
        # log_action("Navigated directly to Cash Managemen", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(2)
        # driver.save_screenshot(os.path.join(screenshots_folder, "CashManagement_Landing.png"))

        Business_Hub = driver.find_element(By.CSS_SELECTOR, '[data-bs-title="Business Hub"]')
        driver.execute_script("arguments[0].click();", Business_Hub)
        log_action("Clicked Business Hub menu", log_file_path=log_file_path)
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Business_Hub_Menu.png"))

        Cash_Management = driver.find_element(By.CSS_SELECTOR, '[data-bs-title="Cash Management"]')
        driver.execute_script("arguments[0].click();", Cash_Management)
        log_action("Clicked Cash Management menu", log_file_path=log_file_path)
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Cash_Management_Menu.png"))

        # --- Cash Collection Balance --- #
        current_balance_el = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'currentBalance')))
        current_balance = clean_text(current_balance_el.text)
        log_action(f"Current Balance: {current_balance}", log_file_path=log_file_path)
        time.sleep(2)

        available_balance_el = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'availableBalance')))
        available_balance = clean_text(available_balance_el.text)
        log_action(f"Available Balance: {available_balance}", log_file_path=log_file_path)
        time.sleep(2)

        # --- Settlement Account Balance --- #
        settlement_acc_bal = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'settlementBalance')))
        log_action(f"Settlement Balance: {settlement_acc_bal.text}", log_file_path=log_file_path)
        time.sleep(2)

        # Settle Available Balance
        Settle_Balance = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-settlement='Settlement' and contains(text(), 'Settle Available Balance')]")))
        driver.execute_script("arguments[0].click();", Settle_Balance)
        log_action("Clicked Settle Available Balance button", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Settle_Available_Balance.png"))

        # Back
        Back_Button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//p[contains(@class, 'back-text') and normalize-space(text())='Back']")))
        driver.execute_script("arguments[0].click();", Back_Button)
        log_action("Clicked Back button", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Back_Button.png"))

        # Transfer Funds
        Transfer_Funds = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-primary') and contains(text(), 'Transfer Funds')]")))
        driver.execute_script("arguments[0].click();", Transfer_Funds)
        log_action("Clicked Transfer Funds button", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Transfer_Funds.png"))

        To_Another_Bank = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-transfer-type='bank' and contains(normalize-space(text()), 'To Another Bank')]")))
        driver.execute_script("arguments[0].click();", To_Another_Bank)
        log_action("Clicked To Another Bank button", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "To_Another_Bank.png"))

        # Back
        Back_Button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//p[contains(@class, 'back-text') and normalize-space(text())='Back']")))
        driver.execute_script("arguments[0].click();", Back_Button)
        log_action("Back to Cash Management", log_file_path=log_file_path)
        time.sleep(2)

        # Merchant Account History
        Merchant_Account_History = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='nav-ma-transactions-tab' and contains(normalize-space(text()), 'Merchant Account History')]")))
        driver.execute_script("arguments[0].click();", Merchant_Account_History)
        log_action("Clicked Merchant Account History tab", log_file_path=log_file_path)
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Merchant_Account_History_Tab.png"))

        parse_table(driver, '//*[@id="maTransactionsTable"]/tbody', log_file_path, "Merchant Account History")

        # Payment Collections
        Payment_Collections = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='nav-collection-transactions-tab' and contains(normalize-space(text()), 'Payment Collections')]")))
        driver.execute_script("arguments[0].click();", Payment_Collections)
        log_action("Clicked Payment Collections tab", log_file_path=log_file_path)
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Payment_Collections_Tab.png"))

        parse_table(driver, '//*[@id="collectionTransactionsTable"]/tbody', log_file_path, "Payment Collections")

        # Fund Transfer
        Fund_Transfers = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='nav-payout-transactions-tab' and contains(normalize-space(text()), 'Fund Transfers')]")))
        driver.execute_script("arguments[0].click();", Fund_Transfers)
        log_action("Clicked Fund Transfers tab", log_file_path=log_file_path)
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Fund_Transfers_Tab.png"))

        parse_table(driver, '//*[@id="payoutTransactionsTable"]/tbody', log_file_path, "Fund Transfer")

        # Back to Payment Collections Tab
        Payment_Collections = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='nav-collection-transactions-tab' and contains(normalize-space(text()), 'Payment Collections')]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Payment_Collections)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", Payment_Collections)
        log_action("Clicked Payment Collections tab again", log_file_path=log_file_path)
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Payment_Collections_Tab_Again.png"))


        # Filter last 7 days
        today = datetime.today()
        seven_days_ago = today - timedelta(days=7)
        date_range = f"{seven_days_ago.strftime('%m/%d/%Y')} - {today.strftime('%m/%d/%Y')}"

        Date_Filter = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "collectionDateRange")))
        log_action("Using Collection Date Filter", log_file_path=log_file_path)

        Date_Filter.clear()
        Date_Filter.send_keys(date_range)
        Date_Filter.send_keys(Keys.ENTER)

        log_action(f"Applied last 7 days filter: {date_range}", log_file_path=log_file_path)
        time.sleep(3)
        driver.save_screenshot(os.path.join(screenshots_folder, "Collection_Last7Days_Filter.png"))

        # Generate QR
        Generate_QR = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ob-button--create-order') and contains(normalize-space(text()), 'Generate QR')]")))
        driver.execute_script("arguments[0].click();", Generate_QR)
        log_action("Clicked Generate QR button", log_file_path=log_file_path)
        time.sleep(3)
        driver.save_screenshot(os.path.join(screenshots_folder, "Generate_QR_Button.png"))

        Generate_QR_Container = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.generate-qr")))
        log_action("Generate QR container is visible", log_file_path=log_file_path)

    except Exception:
        log_action("Cash Management Failed", log_file_path=log_file_path)
        log_error(traceback.format_exc(), log_file_path=log_file_path)