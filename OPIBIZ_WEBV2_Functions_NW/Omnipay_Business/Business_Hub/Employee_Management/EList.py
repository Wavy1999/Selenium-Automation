# Standard library imports
import os       # for file / path operations
import time     # for sleep / timestamp if needed
import traceback  # for printing exception tracebacks

# Third-party imports (Selenium WebDriver)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException  # handle wait timeouts

# Local utility module imports
from Utility import (
    log_action,               # custom logging for actions
    log_error,                # custom logging for errors
    human_like_typing,        # simulate typing behavior for UI input
    random_employee,          # helper to pick a random employee (test data)
    upload_image_by_name,     # helper to upload image by filename
    clear_folder,             # utility to clear a folder (temp files, etc.)
    get_latest_employee_name_from_log,  # helper to retrieve last logged employee name
    find_employee_row,        # helper to locate an employee row in UI/table
    wait_and_click_ok,        # helper to wait for and click OK buttons/dialogs
    search_and_select_employee,  # helper to find & select employee in UI
)

from path_config import SCD_MODULE_PATHS

def EList(driver, wait):
   
    # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['EList']['log']
    screenshots_folder = SCD_MODULE_PATHS['EList']['screenshots']
    
    # Clear old files before test run
    clear_folder(screenshots_folder=screenshots_folder)

    try:
        # Wait until the side options are clickable
        # Business_Hub = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-bs-title='Business Hub' and .//span[text()='Business Hub']]")))
        # driver.execute_script("arguments[0].click();", Business_Hub)
        # log_action("Clicked Business Hub menu", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(2)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Business_Hub_Menu.png"))

        # Employee Management
        # Employee_Management = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-bs-title='Employee Management' and .//span[text()='Employee Management']]")))
        # Employee_Management = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='ob__breadcrumb-link' and normalize-space(text())='Employee Management']")))
        # driver.execute_script("arguments[0].click();", Employee_Management)
        # log_action("Clicked Employee Management menu", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(2)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Employee_Management_Menu.png"))
       
        # # Employee List
        # employee_list = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[.//span[normalize-space(text())='Employee List']]")))
        # driver.execute_script("arguments[0].click();", employee_list)
        # log_action("Clicked Employee List", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(2)

        #  ADD THIS: Refresh to ensure fresh data from database
        log_action("Refreshing employee list to get latest data", log_file_path=log_file_path)
        driver.refresh()
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(3)  # Give time for data to load

        driver.save_screenshot(os.path.join(screenshots_folder, "Employee_List_Page.png"))

        # Get latest employee email from NEmployee log
        logs_reuse_path = SCD_MODULE_PATHS['NEmployee']['log']
        employee_email = get_latest_employee_name_from_log(logs_reuse_path)
        if not employee_email:
            error_msg = "No email found in NEmployee log."
            log_error(error_msg, log_file_path=log_file_path, driver=driver)
            raise Exception(error_msg)

        log_action(f"Retrieved employee email from log: {employee_email}", log_file_path=log_file_path)

        # ADD THIS: Wait for database synchronization
        log_action("Waiting 5 seconds for database synchronization...", log_file_path=log_file_path)
        time.sleep(5)

        # Wait for employee list container
        employee_list_container_locator = (By.CSS_SELECTOR, ".ob__container.employee-list")
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located(employee_list_container_locator))
        log_action("Container 'employee-list' is now visible", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Employee_List_Container_Visible.png"))

        # Wait for employee table to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='employeeListTable']/tbody/tr")))
        log_action("Employee table loaded", log_file_path=log_file_path)

        # ========== VIEW EMPLOYEE ==========
        search_and_select_employee(driver, wait, employee_email, log_file_path, screenshots_folder)

        # Click View button
        view_employee = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn-outline-secondary ob-button ob-button-sm' and normalize-space(text())='View']")))
        driver.execute_script("arguments[0].click();", view_employee)
        log_action("Clicked View link for employee", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Employee_View_Page.png"))

        # Navigate back to Employee List
        back_text = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//p[@class='back-text' and normalize-space(text())='Back']")))
        driver.execute_script("arguments[0].click();", back_text)
        log_action("Clicked Back to return to employee list", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)

        # ========== EDIT EMPLOYEE ==========
        search_and_select_employee(driver, wait, employee_email, log_file_path, screenshots_folder)

        # Click Edit button
        edit_link = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn-outline-secondary ob-button ob-button-sm' and normalize-space(text())='Edit']")))
        driver.execute_script("arguments[0].click();", edit_link)
        log_action("Clicked Edit link for employee", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Employee_Edit_Page.png"))
        
        # Get random employee data for update
        employee = random_employee()

        # Update Number of Dependencies
        dep = driver.find_element(By.NAME, "nbrDependent")
        dep.clear()
        human_like_typing(dep, str(employee["Number of Dependencies"]))
        log_action(f"Entered dependencies: {employee['Number of Dependencies']}", log_file_path=log_file_path)

        # Click Update Employee button
        update_employee = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "saveNewEmployee")))
        driver.execute_script("arguments[0].click();", update_employee)
        log_action("Clicked Update Employee button", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Update_Employee_Clicked.png"))

        # Confirm update
        confirm_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled")))
        driver.execute_script("arguments[0].click()", confirm_btn)
        log_action("Confirmed employee update", log_file_path=log_file_path)

        # Wait for success message
        wait_and_click_ok(driver, timeout=30)
        log_action("Employee update successful", log_file_path=log_file_path)

        # Wait for return to employee list
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located(employee_list_container_locator))
        log_action("Returned to employee list", log_file_path=log_file_path)

        # ========== DEACTIVATE EMPLOYEE (OPTIONAL) ==========
        search_and_select_employee(driver, wait, employee_email, log_file_path, screenshots_folder)

        try:
            # Attempt to deactivate (may not be available for all employees)
            deactivate_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class,'deactivateEmployee') and normalize-space(text())='Deactivate']")))
            driver.execute_script("arguments[0].click();", deactivate_button)
            log_action("Clicked Deactivate employee link", log_file_path=log_file_path)

            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            time.sleep(2)
            driver.save_screenshot(os.path.join(screenshots_folder, "Employee_Deactivate_Clicked.png"))

            # Confirm deactivation
            confirm_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled")))
            driver.execute_script("arguments[0].click()", confirm_btn)
            log_action("Confirmed employee deactivation", log_file_path=log_file_path)

            # Wait for success message
            wait_and_click_ok(driver, timeout=30)
            log_action("Employee deactivation successful", log_file_path=log_file_path)

        except TimeoutException:
            log_action("Deactivate button not available (employee may already be deactivated or permission restricted)", 
                      log_file_path=log_file_path)

    except Exception as e:
        error_message = f"Element not found or interaction failed: {traceback.format_exc()}"
        log_error(error_message, log_file_path=log_file_path, driver=driver)
        print(error_message)
        raise  