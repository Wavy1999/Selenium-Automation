# Standard library imports
import os                     # for file / path operations
import time                   # for timing / sleep operations
import traceback              # for printing exception tracebacks / debugging
from datetime import datetime  # for date-time operations, timestamps, etc.

# Third-party library imports (Selenium WebDriver)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local application / project-specific imports
from Utility import (
    log_action,            # custom logging of actions
    log_error,             # logging of errors/exceptions
    human_like_typing,     # simulate realistic typing in UI testing
    random_employee,       # helper to pick a random employee (test data)
    upload_image_by_name,  # helper to upload image by filename via UI
    clear_folder,          # utility to clear a directory (cleanup)
    wait_and_click_ok,     # helper to wait for OK button / dialog and click it
    Main_Dashboard         # project-specific dashboard helper / class
)
from path_config import SCD_MODULE_PATHS  # config for module paths within project


def NEmployee(driver, wait):
    
    # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['NEmployee']['log']
    screenshots_folder = SCD_MODULE_PATHS['NEmployee']['screenshots']
    
    # Clear old files before test run
    clear_folder(screenshots_folder=screenshots_folder)
    driver.refresh()

    try:
        # Business Hub
        # Business_Hub = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-bs-title='Business Hub' and .//span[text()='Business Hub']]")))
        # Business_Hub = driver.find_element(By.CSS_SELECTOR, '[data-bs-title="Business Hub"]')
        # driver.execute_script("arguments[0].click();", Business_Hub)
        # log_action("Clicked Business Hub menu", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(3)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Business_Hub_Menu.png"))

        # Employee Management
        # Employee_Management = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/header/div/nav/ul/li[5]/ul/li[3]/a")))
        # driver.execute_script("arguments[0].click();", Employee_Management)
        # log_action("Clicked Employee Management", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(3)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Employee_Management_Menu.png"))

        current_url = driver.current_url
        base_url = "/".join(current_url.split("/", 3)[:3]) 
        target_url = base_url + "/EmployeeManagement/AddNewEmployee"

        driver.get(target_url)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Employee_Management_Menu.png"))

        # # Add New Employee
        # add_new_employee = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"//a[@href='/EmployeeManagement/AddNewEmployee' and .//span[text()='Add New Employee']]")))
        # driver.execute_script("arguments[0].click();", add_new_employee)
        # log_action("Clicked Add New Employee fly-out", log_file_path=log_file_path)
        # WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        # time.sleep(3)
        # driver.save_screenshot(os.path.join(screenshots_folder, "Add_New_Employee_Page.png"))

        container_locator = (By.CSS_SELECTOR, ".ob__container.add-employee")
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located(container_locator))

        log_action("Container add employee is now visible", log_file_path=log_file_path)
        time.sleep(3) 
        driver.save_screenshot(os.path.join(screenshots_folder, "Add_New_Employee_Page.png"))

        # Get random employee data
        employee = random_employee()

        # Employee Details
        # First Name
        fname = driver.find_element(By.NAME, "firstName")
        fname.clear()
        human_like_typing(fname, employee["First Name"])
        log_action(f"Entered first name: {employee['First Name']}", log_file_path=log_file_path)

        # Middle Name
        mname = driver.find_element(By.NAME, "middleName")
        mname.clear()
        human_like_typing(mname, employee["Middle Name"])
        log_action(f"Entered middle name: {employee['Middle Name']}", log_file_path=log_file_path)

        # Last Name
        lname = driver.find_element(By.NAME, "lastName")
        lname.clear()
        human_like_typing(lname, employee["Last Name"])
        log_action(f"Entered last name: {employee['Last Name']}", log_file_path=log_file_path)

       # Get birthday from Excel
        birthday_value = employee["Birthday"]

        # Handle different cases (string or datetime)
        if isinstance(birthday_value, datetime):
            birthday = birthday_value  # already a datetime object
        else:
            # force to string, strip spaces
            birthday_str = str(birthday_value).strip()
            # try parsing it safely
            try:
                birthday = datetime.strptime(birthday_str, "%Y-%m-%d")
            except ValueError:
                # fallback if Excel gave something like 05/05/1999
                birthday = datetime.strptime(birthday_str, "%m/%d/%Y")

            # Reformat for your datepicker (MM/DD/YYYY)
            formatted_bday = birthday.strftime("%m/%d/%Y")

            # Fill in the datepicker
            bday = driver.find_element(By.ID, "datepicker")
            bday.clear()
            human_like_typing(bday, formatted_bday)

            log_action(f"Entered birthday: {formatted_bday}", log_file_path=log_file_path)

        # Civil Status
        civil_status = driver.find_element(By.NAME, "civilStatus")
        select = Select(civil_status)
        select.select_by_visible_text(employee["Civil Status"])  # Example: "Single", "Married"
        log_action(f"Selected civil status: {employee['Civil Status']}", log_file_path=log_file_path)
        
        # Citizenship
        citizenship = driver.find_element(By.NAME, "citizenship")
        select = Select(citizenship)
        select.select_by_visible_text(employee["Citizenship"])  # "Filipino" or "Foreign"
        log_action(f"Selected citizenship: {employee['Citizenship']}", log_file_path=log_file_path)

        # TIN
        tin = driver.find_element(By.NAME, "tin")
        tin.clear()
        human_like_typing(tin, employee["TIN"])
        log_action(f"Entered TIN: {employee['TIN']}", log_file_path=log_file_path)

         # Number of Dependencies
        dep = driver.find_element(By.NAME, "nbrDependent")
        dep.clear()
        human_like_typing(dep, str(employee["Number of Dependencies"]))
        log_action(f"Entered dependencies: {employee['Number of Dependencies']}", log_file_path=log_file_path)

        # Mobile Number
        mobile = driver.find_element(By.NAME, "contactMobile")
        mobile.clear()
        human_like_typing(mobile, str(employee["Mobile Number"]))
        log_action(f"Entered mobile number: {employee['Mobile Number']}", log_file_path=log_file_path)

        # Email
        email = driver.find_element(By.NAME, "contactEmail")
        email.clear()
        human_like_typing(email, employee["Email"])
        log_action(f"Entered email: {employee['Email']}", log_file_path=log_file_path)
        
        # After filling text fields
        full_name = f"{employee['First Name']} {employee['Last Name']}"
        uploaded_image = upload_image_by_name(driver, full_name)
        log_action(f"Uploaded image: {upload_image_by_name}", log_file_path=log_file_path)

        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(3)
        driver.save_screenshot(os.path.join(screenshots_folder, "Employee Details.png"))

        # Save New Employee 
        save_employee_btn = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, 'saveNewEmployee')))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", save_employee_btn)
        time.sleep(1)
        driver.execute_script("arguments[0].click()", save_employee_btn)
        log_action("Save New Employee button:", log_file_path=log_file_path)

        # Confirmation Button 
        confirm_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled")))
        driver.execute_script("arguments[0].click()", confirm_btn)
        log_action("Confirmation, are you sure want to create new employee:", log_file_path=log_file_path)       

        # Sucess 
        wait_and_click_ok(driver, timeout=30)
        log_action("Success:", log_file_path=log_file_path)

    except Exception as e:
        error_message = f"Element not found or interaction failed: {traceback.format_exc()}"
        log_error(error_message, log_file_path=log_file_path, driver=driver)
        print(error_message)
