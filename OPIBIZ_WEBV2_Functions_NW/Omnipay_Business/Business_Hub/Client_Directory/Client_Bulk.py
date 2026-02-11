import os
import traceback
import time
import pandas as pd
import shutil

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from Utility import (
    log_action,
    log_error,
    clear_folder,
    wait_and_click_ok,
)

from path_config import SCD_MODULE_PATHS


def Bulk_Client(driver, wait):
    """
    Automates bulk client upload process with address upload and Client ID auto-fill.
    
    Args:
        driver: Selenium WebDriver instance
        wait: WebDriverWait instance
        
    Returns:
        bool: True if upload successful, False otherwise
    """
    
    # -------------------
    # Setup paths
    # -------------------
    log_file_path = SCD_MODULE_PATHS["Client_Bulk"]["log"]
    screenshots_folder = SCD_MODULE_PATHS["Client_Bulk"]["screenshots"]
    clear_folder(screenshots_folder=screenshots_folder)

    try:
        # Use consistent wait timeout
        wait = WebDriverWait(driver, 30)

        # -------------------
        # Navigate to Bulk Client Upload
        # -------------------
        if not _navigate_to_bulk_client(driver, wait, log_file_path, screenshots_folder):
            return False

        # -------------------
        # Upload Client Excel file
        # -------------------
        client_excel_path = r"d:\Bastion\SQA_QualityEnterprise\SoftwareTesting\Projects\Common\Automation\OPI\Files\Testdata\SCD_BULK_ENDCUSTOMER-251029.xlsx"
        
        # Validate file exists
        if not os.path.exists(client_excel_path):
            log_error(f"Client Excel file not found: {client_excel_path}", log_file_path)
            driver.save_screenshot(os.path.join(screenshots_folder, "Client_File_Not_Found.png"))
            return False
            
        log_action(f"Client Excel File Path: {client_excel_path}", log_file_path)

        # Upload client file
        file_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        file_input.send_keys(client_excel_path)
        log_action("Client file added to FilePond", log_file_path)
        time.sleep(1)

        # Click upload button
        upload_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "uploadButton"))
        )
        driver.execute_script("arguments[0].click();", upload_btn)
        log_action("Clicked Upload button for Client", log_file_path)
        driver.save_screenshot(os.path.join(screenshots_folder, "After_Click_Client_Upload.png"))

        # -------------------
        # Wait for upload confirmation dialog and click OK (FIRST OK)
        # -------------------
        try:
            wait_and_click_ok(driver, timeout=15)
            log_action("Clicked OK on first upload confirmation dialog", log_file_path)
        except Exception as e:
            log_action(f"No first upload dialog appeared: {str(e)}", log_file_path)

        # -------------------
        # Wait for Client Upload Success
        # -------------------
        try:
            wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//h1[contains(text(),'Batch Client Successfully Processed!')]")
                )
            )
            driver.save_screenshot(os.path.join(screenshots_folder, "Bulk_Client_Upload_Success.png"))
            log_action("Bulk Client Upload successful", log_file_path)
            
        except TimeoutException:
            log_error("Client success confirmation message not found", log_file_path)
            driver.save_screenshot(os.path.join(screenshots_folder, "Client_Success_Message_Timeout.png"))
            return False

        # -------------------
        # Click OK on success modal (SECOND OK - after bulk client upload success)
        # -------------------
        try:
            wait_and_click_ok(driver, timeout=10)
            log_action("Clicked OK on success modal after bulk client upload", log_file_path)
            time.sleep(2)
        except Exception as e:
            log_action(f"No success modal appeared: {str(e)}", log_file_path)

        # -------------------
        # Click Skip for Now Button
        # -------------------
        try:
            skip_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[@href='/ClientDirectory' and text()='Skip for Now']")
                )
            )
            driver.execute_script("arguments[0].click();", skip_btn)
            log_action("Clicked Skip for Now button", log_file_path)
            time.sleep(3)  # Wait for page to load
            driver.save_screenshot(os.path.join(screenshots_folder, "Skip_For_Now_Clicked.png"))
            
        except TimeoutException:
            log_error("Skip for Now button not found", log_file_path)
            driver.save_screenshot(os.path.join(screenshots_folder, "Skip_Button_Timeout.png"))
            return False

        log_action("="*60, log_file_path)
        log_action("✓ COMPLETE WORKFLOW FINISHED SUCCESSFULLY!", log_file_path)
        log_action("="*60, log_file_path)
        return True

    except TimeoutException as e:
        print(f"Timeout error: {str(e)}")
        print(traceback.format_exc())
        driver.save_screenshot(os.path.join(screenshots_folder, "Timeout_Error.png"))
        log_error(f"Timeout in Bulk_Client: {str(e)}\n{traceback.format_exc()}", log_file_path)
        return False
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        print(traceback.format_exc())
        driver.save_screenshot(os.path.join(screenshots_folder, "Unexpected_Error.png"))
        log_error(f"Unexpected error in Bulk_Client: {str(e)}\n{traceback.format_exc()}", log_file_path)
        return False


def _navigate_to_bulk_client(driver, wait, log_file_path, screenshots_folder):
    """
    Navigate through menus to reach bulk client upload page.
    
    Returns:
        bool: True if navigation successful, False otherwise
    """
    try:
       
        
        # url = "http://vm-app-dev01:9001/ClientDirectory/BatchClient"
        url = "http://beta-opibizscd.paybps.ovpn/ClientDirectory/BatchClient"
        driver.get(url)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        log_action("Navigated to Bulk Client Upload page", log_file_path)
        
        return True
        
    except TimeoutException as e:
        log_error(f"Navigation timeout: {str(e)}", log_file_path)
        driver.save_screenshot(os.path.join(screenshots_folder, "Navigation_Error.png"))
        return False
    except Exception as e:
        log_error(f"Navigation error: {str(e)}", log_file_path)
        driver.save_screenshot(os.path.join(screenshots_folder, "Navigation_Exception.png"))
        return False


def _extract_client_ids_from_table(driver, wait, log_file_path, screenshots_folder):
    """
    Extract Client IDs and names from the results table after bulk client upload.
    
    Returns:
        dict: Mapping of (first_name, last_name) -> client_id
    """
    try:
        # Wait for table to appear
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
        )
        log_action("Results table found, extracting data...", log_file_path)
        driver.save_screenshot(os.path.join(screenshots_folder, "Client_Results_Table.png"))
        
        # Get table headers to understand structure
        headers = driver.find_elements(By.CSS_SELECTOR, "table thead th")
        header_texts = [h.text.strip() for h in headers]
        log_action(f"Table headers: {header_texts}", log_file_path)
        
        # Get all table rows
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        log_action(f"Found {len(rows)} rows in table", log_file_path)
        
        client_id_mapping = {}
        
        for idx, row in enumerate(rows):
            cells = row.find_elements(By.TAG_NAME, "td")
            cell_texts = [cell.text.strip() for cell in cells]
            log_action(f"Row {idx + 1} data: {cell_texts}", log_file_path)
            
            # Assuming table structure: Client ID | First Name | Last Name | ...
            if len(cells) >= 3:
                client_id = cells[0].text.strip()
                first_name = cells[1].text.strip()
                last_name = cells[2].text.strip()
                
                if client_id and first_name and last_name:
                    key = (first_name.lower(), last_name.lower())
                    client_id_mapping[key] = client_id
                    log_action(f"✓ Extracted: {first_name} {last_name} -> {client_id}", log_file_path)
                else:
                    log_action(f"⚠ Incomplete data - ID: '{client_id}', First: '{first_name}', Last: '{last_name}'", log_file_path)
            else:
                log_action(f"⚠ Row {idx + 1} has only {len(cells)} cells, expected at least 3", log_file_path)
        
        log_action(f"{'='*60}", log_file_path)
        log_action(f"Total Client IDs extracted: {len(client_id_mapping)}", log_file_path)
        log_action(f"Mapping: {dict(list(client_id_mapping.items())[:5])}...", log_file_path)
        log_action(f"{'='*60}", log_file_path)
        
        return client_id_mapping
        
    except TimeoutException:
        log_action("Results table not found (may not be displayed)", log_file_path)
        return {}
    except Exception as e:
        log_error(f"Error extracting Client IDs: {str(e)}", log_file_path)
        traceback.print_exc()
        return {}


def _download_and_keep_template(driver, wait, log_file_path, screenshots_folder):
    """
    Download the address template and handle Chrome's 'Keep' download warning.
    
    Returns:
        str: Path to downloaded template file, or None if failed
    """
    try:
        # Find and click the template download link
        template_link = wait.until(
            EC.element_to_be_clickable((By.ID, "templateDownload"))
        )
        template_url = template_link.get_attribute("href")
        log_action(f"Found template download link: {template_url}", log_file_path)
        
        # Get Downloads folder path
        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        log_action(f"Downloads folder: {downloads_folder}", log_file_path)
        
        # Get list of files BEFORE download
        files_before = set(os.listdir(downloads_folder)) if os.path.exists(downloads_folder) else set()
        
        # Click to download template
        driver.execute_script("arguments[0].click();", template_link)
        log_action("Clicked template download link", log_file_path)
        time.sleep(2)
        
        # -------------------
        # HANDLE CHROME'S "KEEP" DOWNLOAD WARNING
        # -------------------
        log_action("Attempting to handle Chrome download warning (Keep button)...", log_file_path)
        
        # Method 1: Try keyboard shortcut to keep file
        try:
            actions = ActionChains(driver)
            # Try multiple key combinations that might work
            
            # Try Alt+K (common for Keep)
            actions.key_down(Keys.ALT).send_keys('k').key_up(Keys.ALT).perform()
            time.sleep(0.5)
            log_action("Sent Alt+K command", log_file_path)
            
            # Try Ctrl+J to open downloads and possibly bypass
            actions.key_down(Keys.CONTROL).send_keys('j').key_up(Keys.CONTROL).perform()
            time.sleep(1)
            log_action("Sent Ctrl+J to open downloads", log_file_path)
            
            # Try pressing Enter to confirm Keep
            actions.send_keys(Keys.ENTER).perform()
            time.sleep(0.5)
            log_action("Sent Enter key", log_file_path)
            
            # Close downloads tab if opened (Ctrl+W)
            actions.key_down(Keys.CONTROL).send_keys('w').key_up(Keys.CONTROL).perform()
            time.sleep(0.5)
            
        except Exception as e:
            log_action(f"Keyboard shortcut attempt: {str(e)}", log_file_path)
        
        # Method 2: Try to find and click "Keep" button in download bar using JavaScript
        try:
            # Try to find download bar elements
            keep_button_js = """
            var downloadBar = document.querySelector('downloads-manager');
            if (downloadBar && downloadBar.shadowRoot) {
                var keepBtn = downloadBar.shadowRoot.querySelector('[id*="keep"]');
                if (keepBtn) keepBtn.click();
            }
            """
            driver.execute_script(keep_button_js)
            log_action("Attempted JavaScript click on Keep button", log_file_path)
        except Exception as e:
            log_action(f"JavaScript Keep attempt: {str(e)}", log_file_path)
        
        # Method 3: Wait and check for file with retries
        downloaded_file_path = None
        max_wait_time = 60  # Maximum wait time in seconds
        
        log_action(f"Waiting for download to complete (max {max_wait_time}s)...", log_file_path)
        
        for i in range(max_wait_time):
            time.sleep(1)
            
            if os.path.exists(downloads_folder):
                files_after = set(os.listdir(downloads_folder))
                new_files = files_after - files_before
                
                # Look for new Excel files
                for f in new_files:
                    if f.endswith(('.xlsx', '.xls')) and not f.endswith('.crdownload'):
                        downloaded_file_path = os.path.join(downloads_folder, f)
                        log_action(f"✓ New file detected: {f}", log_file_path)
                        break
                
                # Also check for template-related files
                if not downloaded_file_path:
                    all_files = os.listdir(downloads_folder)
                    template_files = [
                        f for f in all_files 
                        if ('template' in f.lower() or 'address' in f.lower()) 
                        and f.endswith(('.xlsx', '.xls'))
                        and not f.endswith('.crdownload')
                    ]
                    
                    if template_files:
                        # Get the most recent file
                        template_paths = [os.path.join(downloads_folder, f) for f in template_files]
                        downloaded_file_path = max(template_paths, key=os.path.getctime)
                        # Check if file was created/modified recently (within last 60 seconds)
                        if time.time() - os.path.getctime(downloaded_file_path) < 60:
                            log_action(f"✓ Template file found: {os.path.basename(downloaded_file_path)}", log_file_path)
                            break
                        else:
                            downloaded_file_path = None  # Not recent enough
                
                if downloaded_file_path:
                    break
            
            # Every 5 seconds, try pressing Enter again in case Keep dialog is up
            if i % 5 == 4:
                try:
                    actions = ActionChains(driver)
                    actions.send_keys(Keys.ENTER).perform()
                    log_action(f"Retry {i//5 + 1}: Sent Enter key", log_file_path)
                except:
                    pass
        
        if downloaded_file_path and os.path.exists(downloaded_file_path):
            log_action(f"✓ Template download confirmed: {downloaded_file_path}", log_file_path)
            driver.save_screenshot(os.path.join(screenshots_folder, "Template_Downloaded.png"))
            return downloaded_file_path
        else:
            log_error("Template download not confirmed within timeout", log_file_path)
            driver.save_screenshot(os.path.join(screenshots_folder, "Template_Download_Failed.png"))
            return None
            
    except TimeoutException:
        log_error("Template download link not found", log_file_path)
        driver.save_screenshot(os.path.join(screenshots_folder, "Template_Link_Timeout.png"))
        return None
    except Exception as e:
        log_error(f"Error downloading template: {str(e)}\n{traceback.format_exc()}", log_file_path)
        return None


def _autofill_template_with_client_data(template_path, client_id_mapping, log_file_path, screenshots_folder):
    """
    Auto-fill the downloaded template with client data and addresses.
    
    Args:
        template_path: Path to the downloaded template Excel file
        client_id_mapping: Dictionary mapping (first_name, last_name) -> client_id
        log_file_path: Path to log file
        screenshots_folder: Path to screenshots folder
        
    Returns:
        str: Path to the filled Excel file, or None if failed
    """
    try:
        log_action(f"Auto-filling template: {template_path}", log_file_path)
        
        # Read the template to understand its structure
        try:
            template_df = pd.read_excel(template_path)
            log_action(f"Template columns: {list(template_df.columns)}", log_file_path)
            log_action(f"Template has {len(template_df)} existing rows", log_file_path)
        except Exception as e:
            log_action(f"Could not read template: {str(e)}", log_file_path)
            template_df = None
        
        # Address data to populate
        address_data = [
            {
                'First': 'Frank', 'Last': 'Lee',
                'House': 'Unit 5B', 'Street': 'Pearl Residences, Mango Avenue',
                'Country': 'Philippines', 'Province': 'Metro Manila',
                'City': 'Quezon City', 'Barangay': 'Tandang Sora', 'Postal': '1116'
            },
            {
                'First': 'May', 'Last': 'April',
                'House': '12C', 'Street': 'Century Tower, Gen. Luna St.',
                'Country': 'Philippines', 'Province': 'Metro Manila',
                'City': 'Makati', 'Barangay': 'San Antonio', 'Postal': '1203'
            },
            {
                'First': 'Henry', 'Last': '',
                'House': 'Lot 8, Block 3', 'Street': 'Phase 1, Acacia Street',
                'Country': 'Philippines', 'Province': 'Bulacan',
                'City': 'Meycauayan City', 'Barangay': 'Malhacan', 'Postal': '3020'
            },
            
        ]
        
        # Create rows with Client IDs from mapping
        rows = []
        matched_count = 0
        unmatched_count = 0
        
        for addr in address_data:
            key = (addr['First'].lower(), addr['Last'].lower())
            client_id = client_id_mapping.get(key, '')
            
            row = {
                'Client ID': str(client_id) if client_id else '',
                'Client First Name': addr['First'],
                'Client Last Name': addr['Last'],
                'HOUSE / FLOOR / UNIT NO': addr['House'],
                'BLOCK / BLDG / STREET': addr['Street'],
                'COUNTRY': addr['Country'],
                'PROVINCE': addr['Province'],
                'CITY/MUNICIPALITY': addr['City'],
                'BARANGAY': addr['Barangay'],
                'POSTAL CODE': addr['Postal']
            }
            rows.append(row)
            
            if client_id:
                matched_count += 1
                log_action(f"✓ Matched: {addr['First']} {addr['Last']} -> ID: {client_id}", log_file_path)
            else:
                unmatched_count += 1
                log_action(f"⚠ No match for: {addr['First']} {addr['Last']}", log_file_path)
        
        # Create DataFrame
        df = pd.DataFrame(rows)
        
        # Save to the same template file (overwrite)
        df.to_excel(template_path, index=False)
        
        log_action(f"{'='*60}", log_file_path)
        log_action(f"✓ Template Auto-Fill Complete!", log_file_path)
        log_action(f"  Total entries: {len(rows)}", log_file_path)
        log_action(f"  With Client ID: {matched_count}", log_file_path)
        log_action(f"  Without Client ID: {unmatched_count}", log_file_path)
        log_action(f"  File saved: {template_path}", log_file_path)
        log_action(f"{'='*60}", log_file_path)
        
        return template_path
        
    except Exception as e:
        log_error(f"Error auto-filling template: {str(e)}\n{traceback.format_exc()}", log_file_path)
        return None


def _update_address_file_in_place(address_excel_path, client_id_mapping, log_file_path, screenshots_folder):
    """
    Update the address Excel file IN PLACE with Client IDs (same file, same location).
    
    Args:
        address_excel_path: Path to the address Excel file
        client_id_mapping: Dictionary mapping (first_name, last_name) -> client_id
        log_file_path: Path to log file
        screenshots_folder: Path to screenshots folder
        
    Returns:
        str: Path to updated Excel file (same as input), or None if failed
    """
    try:
        log_action(f"{'='*60}", log_file_path)
        log_action(f"Updating File IN PLACE: {address_excel_path}", log_file_path)
        log_action(f"{'='*60}", log_file_path)
        
        # Read the address Excel file
        df = pd.read_excel(address_excel_path)
        log_action(f"Read address file: {len(df)} rows", log_file_path)
        log_action(f"Address file columns: {list(df.columns)}", log_file_path)
        
        # Show sample of what we're looking for
        log_action(f"Client ID mapping available for {len(client_id_mapping)} clients", log_file_path)
        log_action(f"Sample mapping keys: {list(client_id_mapping.keys())[:3]}", log_file_path)
        
        # Track matches
        matches = 0
        unmatched = 0
        already_filled = 0
        
        # Update Client IDs
        for idx, row in df.iterrows():
            # Check if Client ID already exists
            if pd.notna(row.get('Client ID')):
                already_filled += 1
                log_action(f"Row {idx + 1}: Client ID already exists: {row.get('Client ID')}", log_file_path)
                continue
            
            # Create matching key
            first_name = str(row.get('Client First Name', '')).strip()
            last_name = str(row.get('Client Last Name', '')).strip()
            key = (first_name.lower(), last_name.lower())
            
            log_action(f"Row {idx + 1}: Looking for match - '{first_name}' '{last_name}' -> key: {key}", log_file_path)
            
            # Try to find match
            if key in client_id_mapping:
                client_id_value = client_id_mapping[key]
                # Ensure Client ID is stored as string to match Excel format
                df.at[idx, 'Client ID'] = str(client_id_value)
                matches += 1
                log_action(f"  ✓ MATCHED: {first_name} {last_name} -> {client_id_value}", log_file_path)
            else:
                unmatched += 1
                log_action(f"  ✗ NO MATCH: {first_name} {last_name}", log_file_path)
                log_action(f"     Available keys in mapping: {list(client_id_mapping.keys())[:5]}", log_file_path)
        
        # Save to the SAME file (overwrite original)
        df.to_excel(address_excel_path, index=False)
        
        log_action(f"{'='*60}", log_file_path)
        log_action(f"✓ Client ID Auto-Fill Complete!", log_file_path)
        log_action(f"{'='*60}", log_file_path)
        log_action(f"  Total rows:           {len(df)}", log_file_path)
        log_action(f"  Already filled:       {already_filled}", log_file_path)
        log_action(f"  New matches found:    {matches}", log_file_path)
        log_action(f"  Unmatched:            {unmatched}", log_file_path)
        log_action(f"  ✓ File updated:       {address_excel_path}", log_file_path)
        log_action(f"  (Original file overwritten with Client IDs)", log_file_path)
        log_action(f"{'='*60}", log_file_path)
        
        return address_excel_path  # Return same path
        
    except Exception as e:
        log_error(f"Error updating address file with Client IDs: {str(e)}\n{traceback.format_exc()}", log_file_path)
        return None