# Standard library imports
import os                # file / path ops
import time              # delays / sleep / timing
import traceback         # print stack traces for exception debugging

# Third-party imports (Selenium WebDriver)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local/project-specific imports
from Utility import (
    log_action,           # custom action logging
    log_error,            # custom error logging
    add_new_client,       # utility function to add a new client in UI
    human_like_typing,    # simulate human typing in input fields (UI test)
    clear_folder,         # clean up temporary folders/files
    wait_and_click_ok,    # helper to wait for dialog and click OK
    Main_Dashboard        # project-specific dashboard helper / class
)
from path_config import SCD_MODULE_PATHS  # configuration paths/constants for project modules


def ANClient(driver, wait):

    # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['ANClient']['log']
    screenshots_folder = SCD_MODULE_PATHS['ANClient']['screenshots']

    # Clear old screenshots before test run
    clear_folder(screenshots_folder=screenshots_folder)

    try:
        # Navigate Business Hub menu
        
        # Main_Dashboard(driver,log_file_path,screenshots_folder)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
      
        # # Business_Hub = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-bs-title='Business Hub' and .//span[text()='Business Hub']]")))
        # Business_Hub = driver.find_element(By.CSS_SELECTOR, '[data-bs-title="Business Hub"]')
        # driver.execute_script("arguments[0].click();", Business_Hub)
        # log_action("Clicked Business Hub menu", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(2)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Business_Hub_Menu.png"))

        # # Navigate Client Directory menu
        # Cient_Directory = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-bs-title="Client Directory"]')))
        # driver.execute_script("arguments[0].click();", Cient_Directory)
        # log_action("Clicked Client Directory", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(2)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Client_Directory_Menu.png"))

        # # Click Add New Client button
        # add_new_client_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,  "//a[@href='/ClientDirectory/NewClient' and .//span[text()='Add New Client']]")))
        # driver.execute_script("arguments[0].click();", add_new_client_btn)
        # log_action("Clicked Add New Client button", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(2)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Add_New_Client_Page.png"))

        # url = "http://vm-app-dev01:9001/ClientDirectory/NewClient"
        url = "http://beta-opibizscd.paybps.ovpn/ClientDirectory/NewClient"
        driver.get(url)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        driver.save_screenshot(os.path.join(screenshots_folder, "Add New Client.png"))

        # Wait for Client Details page
        Client_Details = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "clientForm")))
        log_action("Client Details Page", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Client_Details.png"))

        # Get client data from Excel
        client = add_new_client(driver, log_file_path, screenshots_folder)

        # Select Prefix dropdown from Excel value
        Prefix = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "contactPrefix")))
        log_action("Client type dropdown is present", log_file_path=log_file_path)
        time.sleep(2)

        from selenium.webdriver.support.ui import Select
        select = Select(Prefix)
        option_values = [o.get_attribute("value") for o in select.options]
        if client["Prefix"] not in option_values:
            raise ValueError(f"Prefix '{client['Prefix']}' from Excel not found in dropdown options")
        select.select_by_value(client["Prefix"])
        log_action(f"Selected Prefix from Excel: {client['Prefix']}", log_file_path=log_file_path)

        # Fill form fields
        fname = driver.find_element(By.ID, "contactFirstName")
        fname.clear()
        human_like_typing(fname, client["First Name"])
        log_action(f"Entered first name: {client['First Name']}", log_file_path=log_file_path)
        time.sleep(1)

        lname = driver.find_element(By.ID, "contactLastName")
        lname.clear()
        human_like_typing(lname, client["Last Name"])
        log_action(f"Entered last name: {client['Last Name']}", log_file_path=log_file_path)
        time.sleep(1)

        company_name = driver.find_element(By.ID, "companyName")
        company_name.clear()
        human_like_typing(company_name, client["Company Name (Optional)"])
        log_action(f"Entered company name: {client['Company Name (Optional)']}", log_file_path=log_file_path)
        time.sleep(1)

        mobile_number = driver.find_element(By.ID, "mobileNo")
        mobile_number.clear()
        human_like_typing(mobile_number, client["Mobile (Optional)"])
        log_action(f"Entered mobile number: {client['Mobile (Optional)']}", log_file_path=log_file_path)
        time.sleep(1)

        email = driver.find_element(By.ID, "emailAddress")
        email.clear()
        human_like_typing(email, client["Email Address (Optional)"])
        log_action(f"Entered email address: {client['Email Address (Optional)']}", log_file_path=log_file_path)
        time.sleep(1)

        # Screenshot after filling the form
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Fillup_Client_Details.png"))

        # Click Save button
        save_new_client_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "saveNewClientBtn")))
        driver.execute_script("arguments[0].click()", save_new_client_btn)
        log_action("Clicked save new client button", log_file_path=log_file_path)
        time.sleep(2)

        # Click confirmation dialog
        btn_submit = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div[6]/button[1]')))
        driver.execute_script("arguments[0].click()", btn_submit)
        log_action("Clicked confirmation button after saving client", log_file_path=log_file_path)

        # Click Success "OK" button
        wait_and_click_ok(driver, timeout=20)
        log_action("Clicked Success button after saving client", log_file_path=log_file_path)

        # Verify client list
        client_list = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "client-directory")))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", client_list)
        log_action("Client list displayed and scrolled into view", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Client_List.png"))

    except Exception:
        error_message = f"Element not found or interaction failed:\n{traceback.format_exc()}"
        log_error(error_message, log_file_path=log_file_path)  # fixed: removed 'error' argument
        print(error_message)
