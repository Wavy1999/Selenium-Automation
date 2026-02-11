# Standard library imports
import os                      # for filesystem / path operations
import time                    # for delays, sleeps, time-based operations
import traceback               # for exception tracebacks / debugging
import time                    # time delays

# Third-party imports (Selenium WebDriver)
from selenium.webdriver.common.by import By                # locate elements
from selenium.webdriver.common.keys import Keys            # simulate keyboard input
from selenium.webdriver.support.ui import WebDriverWait    # explicit wait helper
from selenium.webdriver.support import expected_conditions as EC  # wait conditions support

# Local / project-specific imports
from Utility import (  
    log_action,  
    log_error,  
    human_like_typing,        # simulate typing in UI tests  
    clear_folder,             # cleanup helper for directories  
    get_latest_client_list_from_log,  # fetch last client list from log  
    find_client_row,          # helper to locate a client row in UI/table  
    add_new_address,          # helper to add address for a client  
    wait_and_click_ok,        # helper to wait & click OK/dialogs  
    add_new_client,           # helper to add a new client via UI  
    fill_up_address           # helper to populate address fields  
)
from path_config import SCD_MODULE_PATHS  # project constants / config for module paths

def CList(driver, wait):
    log_file_path = SCD_MODULE_PATHS['CList']['log']
    screenshots_folder = SCD_MODULE_PATHS['CList']['screenshots']

    clear_folder(screenshots_folder=screenshots_folder)

    try:
        # --- NAVIGATE TO CLIENT LIST --- #
#         try:
#             # business_hub = WebDriverWait(driver, 30).until(
#             #     EC.element_to_be_clickable((By.XPATH, "//a[@data-bs-title='Business Hub' and .//span[text()='Business Hub']]"))
#             # )
#             # driver.execute_script("arguments[0].click();", business_hub)
#             # log_action("Clicked Business Hub menu", log_file_path=log_file_path)
#             # time.sleep(2)
#             # driver.save_screenshot(os.path.join(screenshots_folder, "Business_Hub_Menu.png"))

#             # client_directory = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-bs-title='Client Directory' and .//span[text()='Client Directory']]")))
#             client_directory = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='ob__breadcrumb-link' and normalize-space(text())='Client Directory']")))
#             driver.execute_script("arguments[0].click();", client_directory)
#             log_action("Clicked Client Directory", log_file_path=log_file_path)
#             time.sleep(2)
#             driver.save_screenshot(os.path.join(screenshots_folder, "Client_Directory_Menu.png"))

#             client_list = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/ClientDirectory' and .//span[text()='Client List']]"))
# )
#             driver.execute_script("arguments[0].click();", client_list)
#             log_action("Clicked Client List submenu", log_file_path=log_file_path)
#             time.sleep(2)
#             driver.save_screenshot(os.path.join(screenshots_folder, "Client_List_Menu.png"))

#         except Exception as e:
#             log_error(f"Failed to navigate to Client List: {str(e)}\n{traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
#             raise

        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)


        # url = "http://vm-app-dev01:9001/ClientDirectory"
        url = "http://beta-opibizscd.paybps.ovpn/ClientDirectory"
        driver.get(url)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshots_folder, "Client List.png"))

        # --- GET LATEST CLIENT EMAIL --- #
        logs_path = SCD_MODULE_PATHS['ANClient']['log']
        client_email = get_latest_client_list_from_log(logs_path)
        if not client_email:
            raise Exception("No client email found in ANClient log.")
        log_action(f"Retrieved client email: {client_email}", log_file_path=log_file_path)
        time.sleep(5)  # Wait for database sync

        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "clientDirectoryTable_wrapper")))
        driver.save_screenshot(os.path.join(screenshots_folder, "Client_Directory_Table.png"))
        log_action("Client Directory table is visible", log_file_path=log_file_path)

        # --- SEARCH CLIENT AND SELECT CHECKBOX --- #
        try:
            search_box = wait.until(EC.presence_of_element_located((By.ID, "searchKey")))
            search_box.clear()
            human_like_typing(search_box, client_email)
            time.sleep(2)
            driver.save_screenshot(os.path.join(screenshots_folder, "Searched_Client.png"))
            log_action(f"Searched for client: {client_email}", log_file_path=log_file_path)

            target_row = find_client_row(driver, client_email)
            if not target_row:
                raise Exception(f"Client '{client_email}' not found in table.")

            checkbox = target_row.find_element(By.CSS_SELECTOR, "td:first-child input[type='checkbox']")
            driver.execute_script("arguments[0].click();", checkbox)
            log_action("Selected client checkbox", log_file_path=log_file_path)

        except Exception as e:
            log_error(f"Failed to search/select client: {str(e)}\n{traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
            raise

        # --- VIEW ORDERS --- #
        try:
            
            view_orders_btn = target_row.find_element(By.XPATH,".//a[contains(@href,'ClientProfile') and contains(text(),'View Orders')]")
            driver.execute_script("arguments[0].click();", view_orders_btn)
            log_action("Clicked 'View Orders' button", log_file_path=log_file_path)
            time.sleep(2)
            driver.save_screenshot(os.path.join(screenshots_folder, "Client_View_Orders.png"))

            back_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//p[@class='back-text' and normalize-space(text())='Back']")))
            driver.execute_script("arguments[0].click();", back_btn)
            log_action("Clicked Back to Client List", log_file_path=log_file_path)
            time.sleep(2)
            WebDriverWait(driver, 10).until(EC.staleness_of(back_btn))
            log_action("Returned to Client Directory", log_file_path=log_file_path)

            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "clientDirectoryTable_wrapper")))
            log_action("Client Directory table is visible again", log_file_path=log_file_path)

            search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchKey")))
            log_action("Search box re-located after Back navigation", log_file_path=log_file_path)

        except Exception as e:
            log_error(f"Failed viewing orders: {str(e)}\n{traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
            raise

        # --- VIEW & UPDATE ADDRESS --- #
        try:

            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "clientDirectoryTable_wrapper")))
            search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchKey")))
            search_box.clear()
            human_like_typing(search_box, client_email)
            time.sleep(2)
            driver.save_screenshot(os.path.join(screenshots_folder, "Searched_Client_Again.png"))
            log_action(f"Re-searched client for address: {client_email}", log_file_path=log_file_path)

            target_row = find_client_row(driver, client_email)
            if not target_row:
                raise Exception(f"Client '{client_email}' not found in table.")

            checkbox = target_row.find_element(By.CSS_SELECTOR, "td:first-child input[type='checkbox']")
            driver.execute_script("arguments[0].click();", checkbox)
            log_action("Selected client checkbox for address", log_file_path=log_file_path)

            view_address_btn = target_row.find_element(By.XPATH,".//button[contains(@data-bs-target,'#addUpdateClientAddress') and contains(text(),'View Address')]")
            driver.execute_script("arguments[0].click();", view_address_btn)
            log_action("Clicked 'View Address'", log_file_path=log_file_path)
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-body")))
            time.sleep(2)
            driver.save_screenshot(os.path.join(screenshots_folder, "Client_View_Address_Modal.png"))

            # Get random client address
            address_data = add_new_address(driver, log_file_path, screenshots_folder)

            # HOUSE / FLOOR / UNIT NO
            HOUSE = driver.find_element(By.NAME, "houseNumber")
            HOUSE.clear()
            human_like_typing(HOUSE, address_data["HOUSE / FLOOR / UNIT NO"])
            log_action(f"Entered HOUSE / FLOOR / UNIT NO: {address_data['HOUSE / FLOOR / UNIT NO']}", log_file_path=log_file_path)
            time.sleep(2)

            # BLOCK / BLDG / STREET
            BLOCK = driver.find_element(By.NAME, "street")
            BLOCK.clear()
            human_like_typing(BLOCK, address_data["BLOCK / BLDG / STREET"])
            log_action(f"Entered BLOCK / BLDG / STREET: {address_data['BLOCK / BLDG / STREET']}", log_file_path=log_file_path)
            time.sleep(2)

            try:
                # COUNTRY
                log_action("=" * 50, log_file_path=log_file_path)
                log_action("Starting COUNTRY selection", log_file_path=log_file_path)
                if fill_up_address(driver, (By.ID, "select2-countryCode-container"), address_data["COUNTRY"]):
                    log_action(f" COUNTRY completed: {address_data['COUNTRY']}", log_file_path=log_file_path)
                else:
                    log_error(f" COUNTRY failed: {address_data['COUNTRY']}", log_file_path=log_file_path)
                    raise Exception(f"Country selection failed for: {address_data['COUNTRY']}")
                time.sleep(0.5)

                # PROVINCE
                log_action("=" * 50, log_file_path=log_file_path)
                log_action("Starting PROVINCE selection", log_file_path=log_file_path)
                if fill_up_address(driver, (By.ID, "select2-province-container"), address_data["PROVINCE"]):
                    log_action(f" PROVINCE completed: {address_data['PROVINCE']}", log_file_path=log_file_path)
                else:
                    log_error(f" PROVINCE failed: {address_data['PROVINCE']}", log_file_path=log_file_path)
                    raise Exception(f"Province selection failed for: {address_data['PROVINCE']}")
                time.sleep(0.5)

                # CITY
                log_action("=" * 50, log_file_path=log_file_path)
                log_action("Starting CITY selection", log_file_path=log_file_path)
                if fill_up_address(driver, (By.ID, "select2-city-container"), address_data["CITY/MUNICIPALITY"]):
                    log_action(f" CITY completed: {address_data['CITY/MUNICIPALITY']}", log_file_path=log_file_path)
                else:
                    log_error(f"CITY failed: {address_data['CITY/MUNICIPALITY']}", log_file_path=log_file_path)
                    raise Exception(f"City selection failed for: {address_data['CITY/MUNICIPALITY']}")
                time.sleep(0.5)

                # BARANGAY
                log_action("=" * 50, log_file_path=log_file_path)
                log_action("Starting BARANGAY selection", log_file_path=log_file_path)
                if fill_up_address(driver, (By.ID, "select2-barangay-container"), address_data["OTHERS"]):
                    log_action(f" BARANGAY completed: {address_data['OTHERS']}", log_file_path=log_file_path)
                else:
                    log_error(f"BARANGAY failed: {address_data['OTHERS']}", log_file_path=log_file_path)
                    raise Exception(f"Barangay selection failed for: {address_data['OTHERS']}")
                
                log_action("=" * 50, log_file_path=log_file_path)
                log_action(" ALL ADDRESS FIELDS COMPLETED SUCCESSFULLY ✓✓✓", log_file_path=log_file_path)

            except Exception as e:
                log_error(f"Address filling stopped: {e}", log_file_path=log_file_path)
                # Optionally take screenshot for debugging
                # driver.save_screenshot(f"error_{int(time.time())}.png")
                raise

            log_action(" All address fields completed successfully!", log_file_path=log_file_path)

            # OTHERS (normal input)
            OTHERS = driver.find_element(By.NAME, "barangayOtherInput")
            OTHERS.clear()
            human_like_typing(OTHERS, address_data["BARANGAY"])

            # POSTAL CODE
            POSTAL = driver.find_element(By.NAME, "postCode")
            POSTAL.clear()
            human_like_typing(POSTAL, address_data["POSTAL CODE"])
            log_action(f"Entered POSTAL CODE: {address_data['POSTAL CODE']}", log_file_path=log_file_path)
            time.sleep(2)
        
            driver.save_screenshot(os.path.join(screenshots_folder, "Fillup_Address.png"))

            save_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-save-address='' and contains(text(),'Save Address')]")))
            driver.execute_script("arguments[0].click();", save_btn)
            log_action("Clicked 'Save Address'", log_file_path=log_file_path)
            time.sleep(2)
            driver.save_screenshot(os.path.join(screenshots_folder, "Save_Address.png"))

            confirm_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled")))
            driver.execute_script("arguments[0].click()", confirm_btn)

            close_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-address-close='' and contains(text(),'Close')]")))
            driver.execute_script("arguments[0].click();", close_btn)
            log_action("Clicked 'Close' button", log_file_path=log_file_path)
            
        except Exception as e:
            log_error(f"Failed viewing/updating address: {str(e)}\n{traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
            raise

        # --- EDIT CLIENT --- #
        try:
            search_box.clear()
            human_like_typing(search_box, client_email)
            time.sleep(2)
            driver.save_screenshot(os.path.join(screenshots_folder, "Searched_Client_For_Edit.png"))
            log_action(f"Re-searched client for editing: {client_email}", log_file_path=log_file_path)

            target_row = find_client_row(driver, client_email)
            if not target_row:
                raise Exception(f"Client '{client_email}' not found in table.")

            checkbox = target_row.find_element(By.CSS_SELECTOR, "td:first-child input[type='checkbox']")
            driver.execute_script("arguments[0].click();", checkbox)
            log_action("Selected client checkbox for editing", log_file_path=log_file_path)

            edit_client_btn = target_row.find_element(By.XPATH,".//a[contains(@href,'NewClient') and contains(@href,'type=edit') and contains(text(),'Edit Client')]")
            driver.execute_script("arguments[0].click();", edit_client_btn)
            log_action("Clicked 'Edit Client'", log_file_path=log_file_path)
            time.sleep(2)
            driver.save_screenshot(os.path.join(screenshots_folder, "Client_Edit_Page.png"))

            client_data = add_new_client(driver, log_file_path, screenshots_folder)

            mobile_input = driver.find_element(By.ID, "mobileNo")
            mobile_input.clear()
            human_like_typing(mobile_input, client_data["Mobile (Optional)"])
            log_action(f"Updated mobile number: {client_data['Mobile (Optional)']}", log_file_path=log_file_path)
            time.sleep(1)

            save_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "saveNewClientBtn")))
            driver.execute_script("arguments[0].click()", save_btn)
            log_action("Clicked save new client button", log_file_path=log_file_path)
            time.sleep(2)

            confirm_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div[6]/button[1]')))
            driver.execute_script("arguments[0].click()", confirm_btn)
            wait_and_click_ok(driver, timeout=20)
            log_action("Client edit confirmed", log_file_path=log_file_path)
            time.sleep(2)

            client_list_table = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "client-directory")))
            driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", client_list_table)
            driver.save_screenshot(os.path.join(screenshots_folder, "Client_List.png"))
            log_action("Client list displayed after edit", log_file_path=log_file_path)

        except Exception as e:
            log_error(f"Failed editing client: {str(e)}\n{traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
            raise

    except Exception as e:
        log_error(f"CList function encountered an error: {traceback.format_exc()}", log_file_path=log_file_path, driver=driver)
        driver.save_screenshot(os.path.join(screenshots_folder, "Critical_Error.png"))
        raise
