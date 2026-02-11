import os
import traceback
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from Utility import log_action, log_error

def tet(driver, wait):
    # Get the current file's name without the extension for logging
    current_file_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current file
    log_file_path = os.path.join(current_file_dir, '..', '..', 'Files', 'logs','Service Center','Service Management', 'MService.txt')

    try:
      
        print("Service Management...")
        print("What would you like to do...")
        print("Selecting Manage Services...")

        Manage_Services = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="successPage"]/div/div[2]/button[1]')))
        driver.execute_script("arguments[0].click()", Manage_Services)
        log_action("Clicked Manage Service", log_file_path=log_file_path)
        time.sleep(15)

        element = wait.until(EC.presence_of_element_located((By.ID, "servicemanagemenTable")))
        log_action("managementSearch field is present", log_file_path=log_file_path)

        element = wait.until(EC.presence_of_element_located((By.ID, "managementSearch")))
        element.send_keys("apple")
        log_action("Search service", log_file_path=log_file_path)

        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"servicemanagemenTable\"]/tbody/tr[1]")))
            log_action("Service info is available", log_file_path=log_file_path)
        
        except:
            log_action("Service info is not available", log_file_path=log_file_path)
            pass
        
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"serviceManagementSlider\"]/div[1]/div[2]/div[2]/div/a[1]")))
        driver.execute_script("arguments[0].click()", element)
        log_action("Clicked Add New Service button", log_file_path=log_file_path)

        try:
            element = wait.until(EC.presence_of_element_located((By.ID, "Product.ProductName")))
            log_action("Add New Service is available", log_file_path=log_file_path)
            driver.back()
        
        except:
            log_action("Add New Service is not available", log_file_path=log_file_path)
            driver.back()
            pass

        element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"servicemanagemenTable\"]/tbody/tr[1]/td[7]/div/button[1]")))
        driver.execute_script("arguments[0].click()", element)
        log_action("Clicked View Service button", log_file_path=log_file_path)

        try:
            element = wait.until(EC.presence_of_element_located((By.ID, "serviceForm")))
            log_action("View Service is available", log_file_path=log_file_path)
            driver.back()
        
        except:
            log_action("View Service is not available", log_file_path=log_file_path)
            driver.back()
            pass
        
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"servicemanagemenTable\"]/tbody/tr[1]/td[7]/div/button[2]")))
        driver.execute_script("arguments[0].click()", element)
        log_action("Clicked Update Service button", log_file_path=log_file_path)

        try:
            element = wait.until(EC.presence_of_element_located((By.ID, "serviceForm")))
            log_action("Update Service is available", log_file_path=log_file_path)
            driver.back()
        
        except:
            log_action("Update Service is not available", log_file_path=log_file_path)
            driver.back()
            pass

        #Clicked Select Product
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"servicemanagemenTable\"]/tbody/tr[1]/td[1]/input")))
        driver.execute_script("arguments[0].click()", element)
        log_action("Clicked Select Product", log_file_path=log_file_path)

        # Upload photo
        file_path = r"D:\Bastion1\SQA_QualityEnterprise\SoftwareTesting\Projects\Common\Automation\OPI\Files\Images\Service Management\luffy.jpg"

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
       
        upload_input = driver.find_element(By.XPATH, '//*[@id="servicemanagemenTable"]/tbody/tr[2]/td[6]/div/label/input')
        driver.execute_script("arguments[0].style.display = 'block';", upload_input)
        upload_input.send_keys(file_path)
        driver.find_element(By.ID, "uploadAllBtn").click()
        log_action("Uploaded photo", log_file_path=log_file_path)

        # Delay to see the uploaded photo before moving on
        time.sleep(5)  # wait 5 seconds (adjust if needed)
        element = wait.until(EC.presence_of_element_located((By.ID, "servicemanagemenTable")))
        log_action("Photo upload completed", log_file_path=log_file_path)
        
        # Clicked Add New Service
        create_bulk_order_btn = wait.until(EC.element_to_be_clickable((By.ID, "createBulkOrderButton")))
        driver.execute_script("arguments[0].click()", create_bulk_order_btn)
        log_action("Clicked Create Bulk Service Order Button", log_file_path=log_file_path)

        #Select Client and Address
        client = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"clientList\"]/li[3]/label")))
        driver.execute_script("arguments[0].click()", client)
        log_action("Selected a Client", log_file_path=log_file_path)

        address = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"addressList\"]/li/label")))
        driver.execute_script("arguments[0].click()", address)
        log_action("Selected an Address", log_file_path=log_file_path)

        #Clicked Submit Bulk Service Order Button
        submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "submit-bulk-order-button")))
        driver.execute_script("arguments[0].click()", submit_btn)
        log_action("Clicked Submit Bulk Service Order Button", log_file_path=log_file_path)
        time.sleep(15)

        order_adjustment = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"orderAdjustmentTable\"]/tbody/tr/td[5]/input")))
        order_adjustment.send_keys("6300.00")
        log_action("Entered Order Adjustment Amount", log_file_path=log_file_path)

        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"orderAdjustmentTable\"]/tbody/tr/td[6]/input")))
        element.send_keys("144.00")
        log_action("Entered Order Shipping Amount", log_file_path=log_file_path)

        # Select Tax Type
        tax_type = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'tax-dropdown-toggle')]")))
        tax_type.click()
        time.sleep(1)
        log_action("Clicked Tax Type Dropdown", log_file_path=log_file_path)

        custom_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='dropdown-item' and normalize-space(text())='Custom']")))
        driver.execute_script("arguments[0].click();", custom_option)
        time.sleep(1)  # Wait for the input to be clickable
        log_action("Selected Tax Type: Custom", log_file_path=log_file_path)

        custom_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'tax-input-group')]/input")))
        custom_input.clear()
        custom_input.send_keys("5")
        log_action("Entered Custom Tax Percent: 5%", log_file_path=log_file_path)

        # Click Finalize Bulk Order Button
        bulk_order_btn = wait.until(EC.element_to_be_clickable((By.ID, "finalize-bulk-order-button")))
        driver.execute_script("arguments[0].click()", bulk_order_btn)
        log_action("Clicked Finalize Bulk Order Button", log_file_path=log_file_path)
        time.sleep(10)

        # Uncomment if you want click payment link button
        # # Click Payment Link Button
        # Payment_link = wait.until(EC.element_to_be_clickable((By.ID, "payment-button-0")))
        # driver.execute_script("arguments[0].click()", Payment_link)
        # log_action("Clicked Payment Link Button", log_file_path=log_file_path)

        # driver.get("http://localhost:8011/ServiceCenter/ServiceManagement#")

        # # Check if Order is successful
        # verified_order = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="exportButton"]')))
        # log_action("Check if Order is successful", log_file_path=log_file_path)
        # time.sleep(5)

    except Exception as e:
        error_message = f"Element not found or interaction failed: {traceback.format_exc()}"
        log_error(error_message, log_file_path=log_file_path, driver=driver)
        print(error_message)