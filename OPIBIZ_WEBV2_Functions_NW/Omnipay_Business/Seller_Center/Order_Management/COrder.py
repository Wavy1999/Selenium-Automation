# ---------------------------
# Standard library imports
# ---------------------------
import os                  # File and directory operations
import time                # Delays/sleep or timestamp operations
import datetime            # Date and time manipulations
import traceback           # Capturing stack traces in exception handling

# ---------------------------
# Third-party imports (Selenium WebDriver)
# ---------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------------------------
# Local / project-specific imports
# ---------------------------
from path_config import SCD_MODULE_PATHS  # Project-specific constants for paths
from Utility import (                     # Custom helper functions for automation
    log_action,                           # Log successful actions for debugging/auditing
    log_error,                            # Log exceptions/errors for diagnostics
    human_like_typing,                     # Simulate realistic typing in UI automation
    random_client_product,                 # Select random client product for testing
    select_dropdown,                       # Select an option in a dropdown
    select_adjustment_type,                # Select adjustment type in UI forms
    clear_folder,                          # Clear temporary folders/files
    select_product,                        # Select product in UI forms or tables
    select_tax_type,                        # Select tax type in UI forms
)

def COrder(driver, wait):
   
    # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['COrder']['log']
    screenshots_folder = SCD_MODULE_PATHS['COrder']['screenshots']
    
    # Clear old files before test run
    clear_folder(screenshots_folder=screenshots_folder)

    try:
       
        # Click Create Order
        Order_Management = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[.//span[contains(text(), 'Order Management')]]")))
        driver.execute_script("arguments[0].click()", Order_Management)
        log_action("Clicked Order Management", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshots_folder, "Order_Management_Page_Flyout.png"))
        
        # Create Single Order
        Create_Single_Order = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/header/div/div/div[2]/ul/li[1]/a/div/img")))
        driver.execute_script("arguments[0].click()", Create_Single_Order)
        log_action("Clicked Create Single Order", log_file_path=log_file_path)
        time.sleep(5)

        # Leave the page
        leave_page = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div[6]/button[1]")))
        driver.execute_script("arguments[0].click();", leave_page)
        log_action("Clicked Yes,leave page to proceed in Create Single Order", log_file_path=log_file_path)

        WebDriverWait(driver,30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "card-body")))
        driver.save_screenshot(os.path.join(screenshots_folder, "Create_Single_Order_Page.png"))
        log_action("Create Order page loaded", log_file_path=log_file_path)


        # Client Details
        search = wait.until(EC.element_to_be_clickable((By.ID, "searchClient")))
        driver.execute_script("arguments[0].click()", search)
        log_action("Click Search Button", log_file_path=log_file_path)

        # SEARCH CLIENT
        search_client = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "clientSearchInput")))
        search_client.clear()
        search_client.send_keys("JOHN SANTOS")
        log_action("Search specific client", log_file_path=log_file_path)
        time.sleep(2)
        
        # CLOSE SEARCH
        close_search = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="clientListModal"]/div/div/div[3]/button[1]')))
        driver.execute_script("arguments[0].click()", close_search)
        log_action("Closse search", log_file_path=log_file_path)
        time.sleep(2)

        # CHECKOUT AS GUEST
        checkout_guest = wait.until(EC.element_to_be_clickable((By.ID, "checkoutGuest")))
        driver.execute_script("arguments[0].click()", checkout_guest)
        log_action("Click Checkout as guest option", log_file_path=log_file_path)
        time.sleep(2)

        # Get random employee data
        client = random_client_product()

        #-----Personal Information-----#

        # First Name
        fname = driver.find_element(By.NAME, "firstName")
        fname.clear()
        human_like_typing(fname, client["First Name"])
        log_action(f"Entered first name: {client['First Name']}", log_file_path=log_file_path)
        time.sleep(2)

        # Middle Name
        mname = driver.find_element(By.NAME, "middleName")
        mname.clear()
        human_like_typing(mname, client["Middle Name"])
        log_action(f"Entered middle name: {client['Middle Name']}", log_file_path=log_file_path)
        time.sleep(2)

        # Last Name
        lname = driver.find_element(By.NAME, "lastName")
        lname.clear()
        human_like_typing(lname, client["Last Name"])
        log_action(f"Entered last name: {client['Last Name']}", log_file_path=log_file_path)
        time.sleep(2)

        # Company Name
        cname = driver.find_element(By.NAME, "companyName")
        cname.clear()
        human_like_typing(cname, client["Company Name"])
        log_action(f"Entered Company Name: {client['Company Name']}", log_file_path=log_file_path)
        time.sleep(2)

        #-----Contact Information-----#

       # Mobile Number
        mobile = driver.find_element(By.NAME, "mobileNumber")
        mobile.clear()
        human_like_typing(mobile, str(client["Mobile Number"]))
        log_action(f"Entered mobile number: {client['Mobile Number']}", log_file_path=log_file_path)
        time.sleep(2)

        # Email
        email = driver.find_element(By.NAME, "email")
        email.clear()
        human_like_typing(email, client["Email"])
        log_action(f"Entered email: {client['Email']}", log_file_path=log_file_path)
        time.sleep(2)

        #-----Address -----#

        # HOUSE / FLOOR / UNIT NO
        house_no = driver.find_element(By.NAME, "houseNumber")
        house_no.clear()
        human_like_typing(house_no, client["House/Floor/Unit No."])
        log_action(f"Entered House/Floor/Unit No.: {client['House/Floor/Unit No.']}", log_file_path=log_file_path)
        time.sleep(2)

        # BLOCK / BLDG / STREET
        bloc_no = driver.find_element(By.NAME, "street")
        bloc_no.clear()
        human_like_typing(bloc_no, client["Block/Building/Street"])
        log_action(f"Entered Block/Building/Street: {client['Block/Building/Street']}", log_file_path=log_file_path)
        time.sleep(2)

        # Country
        select_dropdown(driver, wait, "select2-countryCode-container", client["Country"])
        log_action(f"Selected Country: {client['Country']}", log_file_path=log_file_path)
        time.sleep(2)

        # Province
        select_dropdown(driver, wait, "select2-province-container", client["Province"])
        log_action(f"Selected Province: {client['Province']}", log_file_path=log_file_path)
        time.sleep(2)

        # CITY/MUNICIPALITY
        select_dropdown(driver, wait, "select2-city-container", client["City/Municipality"])
        log_action(f"Selected City/Municipality: {client['City/Municipality']}", log_file_path=log_file_path)
        time.sleep(2)

        # BARANGAY
        select_dropdown(driver, wait, "select2-barangay-container", client["Barangay"])
        log_action(f"Selected Barangay: {client['Barangay']}", log_file_path=log_file_path)
        time.sleep(2)

        # POSTAL CODE
        postal_code = driver.find_element(By.NAME, "postCode")
        postal_code.clear()
        human_like_typing(postal_code, str(client["Postal Code"]))
        log_action(f"Entered Postal Code: {client['Postal Code']}", log_file_path=log_file_path)
        time.sleep(2)

        # ORDER NOTES
        order_notes = driver.find_element(By.NAME, "orderNotes")
        order_notes.clear()
        human_like_typing(order_notes, client["Order Notes"])
        log_action(f"Entered Order Notes: {client['Order Notes']}", log_file_path=log_file_path)
        time.sleep(2)

        WebDriverWait(driver,30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        driver.save_screenshot(os.path.join(screenshots_folder, "Client_Details_Filled.png"))

        #-----Client's Product Request -----#

        # PRODUCT CATALOG
        product = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.NAME, 'PurchaseOrders[0].Item')))
        driver.execute_script("arguments[0].click()", product)
        log_action("Clicked to select item in purchase order", log_file_path=log_file_path)

        # SELECT PRODUCT
        success = select_product(
        driver=driver,
        product_name=client["Product"],
        screenshots_folder=screenshots_folder,
        log_file_path=log_file_path
        )
        time.sleep(5)
        WebDriverWait(driver,30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # SELECT PRODUCT CONFIRMATION
        confirm_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-action="confirm"]')))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", confirm_button)
        time.sleep(0.2)
        driver.execute_script("arguments[0].click();", confirm_button)
        log_action("Confirmed selected product", log_file_path=log_file_path)
        time.sleep(10)

        WebDriverWait(driver,30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        driver.save_screenshot(os.path.join(screenshots_folder, "Product_Confirmed.png"))
        
        # PRODUCT QUANTITY
        product_quantity = driver.find_element(By.NAME,"PurchaseOrders[0].Quantity")
        product_quantity.clear()
        product_quantity.send_keys("2")
        log_action("Entered product quantity", log_file_path=log_file_path)
        time.sleep(2)
        
        # SCROLL TO TOP
        scroll_top = driver.find_element(By.CSS_SELECTOR, "div.card-body")
        driver.execute_script("arguments[0].scrollIntoView();", scroll_top)
        
        # Get Due Date from Excel
        due_date = client["Due Date"]
        formatted_due_date = None

        # Handle different cases (string or datetime)
        if isinstance(due_date, datetime.datetime):
            formatted_due_date = due_date.strftime("%m/%d/%Y")
            log_action(f"Due Date is datetime object: {formatted_due_date}", log_file_path=log_file_path)
        else:
            # force to string, strip spaces
            due_date_str = str(due_date).strip()
            # Handle NaN or empty values
            if due_date_str.lower() in ['nan', 'none', '']:
                log_action("Warning: Due Date is empty or NaN, skipping date entry", log_file_path=log_file_path)
                return
        
            # try parsing it safely
            try:
                parsed_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d")
                formatted_due_date = parsed_date.strftime("%m/%d/%Y")
            except ValueError:
                try:
                    parsed_date = datetime.datetime.strptime(due_date_str, "%m/%d/%Y")
                    formatted_due_date = parsed_date.strftime("%m/%d/%Y")
                except ValueError:
                    try:
                        parsed_date = datetime.datetime.strptime(due_date_str, "%m-%d-%Y")
                        formatted_due_date = parsed_date.strftime("%m/%d/%Y")
                    except ValueError:
                        log_action(f"Error: Could not parse due date '{due_date_str}'. Skipping.", log_file_path=log_file_path)
                        return
                    
            log_action(f"Parsed Due Date from string: {formatted_due_date}", log_file_path=log_file_path)

        # NOW ENTER THE DATE (OUTSIDE THE IF/ELSE BLOCK)
        if formatted_due_date:
            try:
                # Wait for and find the date field
                date_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "dueDate"))
                )
                
                # Scroll to make it visible
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", date_field)
                time.sleep(1)
                
                # CRITICAL: Click the field to activate the datepicker
                driver.execute_script("arguments[0].click();", date_field)
                log_action("Clicked date field to activate datepicker", log_file_path=log_file_path)
                time.sleep(1)
                
                # Now set the date using JavaScript
                driver.execute_script("""
                    var element = arguments[0];
                    var date = arguments[1];
                    
                    // Remove readonly if present
                    $(element).removeAttr('readonly');
                    
                    // Set the value
                    $(element).val(date);
                    
                    // Use datepicker API if available
                    if ($.fn.datepicker && $(element).hasClass('hasDatepicker')) {
                        $(element).datepicker('setDate', date);
                    }
                    
                    // Trigger events to ensure UI updates
                    $(element).trigger('input').trigger('change').trigger('blur');
                """, date_field, formatted_due_date)
                
                log_action(f"✓ Entered Due Date via JavaScript: {formatted_due_date}", log_file_path=log_file_path)
                time.sleep(2)
                
                # Verify the date was entered
                entered_value = date_field.get_attribute('value')
                if entered_value:
                    log_action(f"✓ Verified date in field: {entered_value}", log_file_path=log_file_path)
                else:
                    log_action("⚠ Warning: Field appears empty, trying fallback method", log_file_path=log_file_path)
                    
                    # Fallback: Manual typing
                    date_field.clear()
                    time.sleep(0.5)
                    human_like_typing(date_field, formatted_due_date)
                    time.sleep(0.5)
                    from selenium.webdriver.common.keys import Keys
                    date_field.send_keys(Keys.TAB)
                    log_action(f"✓ Entered Due Date via typing (fallback): {formatted_due_date}", log_file_path=log_file_path)
                
                time.sleep(2)
                driver.save_screenshot(os.path.join(screenshots_folder, "Due_Date_Entered.png"))
                
            except Exception as e:
                log_action(f"✗ ERROR entering due date: {str(e)}", log_file_path=log_file_path)
                driver.save_screenshot(os.path.join(screenshots_folder, "Due_Date_Error.png"))

        # SCROLL TO BOTTOM
        scroll_bottom = driver.find_element(By.CSS_SELECTOR, "div.card-body")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);",scroll_bottom)
        WebDriverWait(driver,30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # ADD ITEM 
        add_item_btn =WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@onclick=\"addNewItem('#orderItems', event)\"]")))
        driver.execute_script("arguments[0].click();", add_item_btn)
        log_action("Click Add Item", log_file_path=log_file_path)

        time.sleep(10)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.remove-btn-container")))
        log_action("Remove Item field loaded", log_file_path=log_file_path)
        driver.save_screenshot(os.path.join(screenshots_folder, "Add_Item_Field_Prompt.png"))
        time.sleep(20)

        # REMOVE EMPTY PURCHASE ORDER ITEMS
        print("="*50)
        print("Starting removal of empty purchase order items...")
        print("="*50)

        # Try multiple selectors to find all purchase order items
        try:
            # Wait for container to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "orderItems"))
            )
            time.sleep(1)  # Let DOM settle
            
            # Try different selectors to find all rows
            purchase_items = driver.find_elements(By.CSS_SELECTOR, "#orderItems [data-purchase-order]")
            
            # If that doesn't work, try finding by the container structure
            if len(purchase_items) == 0:
                purchase_items = driver.find_elements(By.CSS_SELECTOR, "#orderItems .purchase-order-item")
            
            # Alternative: find by input groups
            if len(purchase_items) == 0:
                purchase_items = driver.find_elements(By.CSS_SELECTOR, "#orderItems > div")
            
            print(f"Found {len(purchase_items)} purchase order item row(s)")
            
            # Also check for individual product catalog inputs as a fallback count
            all_item_inputs = driver.find_elements(By.CSS_SELECTOR, "#orderItems input.item-input")
            print(f"Cross-check: Found {len(all_item_inputs)} item input field(s)")
            
            if len(purchase_items) == 0:
                print("⚠ No purchase order items found with standard selectors")
                print("Attempting to find items by input fields...")
                # Find parent containers of item inputs
                purchase_items = []
                for input_field in all_item_inputs:
                    parent = input_field.find_element(By.XPATH, "./ancestor::div[contains(@class, 'row') or @data-purchase-order]")
                    if parent not in purchase_items:
                        purchase_items.append(parent)
                print(f"Found {len(purchase_items)} items via input fields")
            
        except Exception as e:
            print(f"✗ Error finding purchase order items: {e}")
            purchase_items = []

        if len(purchase_items) == 0:
            print("⚠ No purchase order items found to process")
        else:
            removed_count = 0
            kept_count = 0
            
            # Process each item starting from the last one
            for idx, item in enumerate(reversed(purchase_items), start=1):
                try:
                    # Get the product catalog input
                    item_input = item.find_element(By.CSS_SELECTOR, "input.item-input")
                    item_value = item_input.get_attribute("value")
                    if item_value:
                        item_value = item_value.strip()
                    else:
                        item_value = ""
                    
                    item_placeholder = item_input.get_attribute("placeholder")
                    if item_placeholder:
                        item_placeholder = item_placeholder.strip()
                    else:
                        item_placeholder = ""
                    
                    # Get the quantity input
                    quantity_input = item.find_element(By.CSS_SELECTOR, "input[data-field='quantity']")
                    quantity_value = quantity_input.get_attribute("value")
                    if quantity_value:
                        quantity_value = quantity_value.strip()
                    else:
                        quantity_value = ""
                    
                    quantity_placeholder = quantity_input.get_attribute("placeholder")
                    if quantity_placeholder:
                        quantity_placeholder = quantity_placeholder.strip()
                    else:
                        quantity_placeholder = ""
                    
                    # Check if item is empty (no selection made)
                    is_item_empty = (
                        not item_value or 
                        item_value == item_placeholder or 
                        item_value.lower() == "item" or
                        len(item_value) == 0
                    )
                    
                    # Check if quantity is empty or zero
                    is_quantity_empty = (
                        not quantity_value or 
                        quantity_value == quantity_placeholder or 
                        quantity_value == "0" or
                        quantity_value.lower() == "quantity" or
                        len(quantity_value) == 0
                    )
                    
                    print(f"\n[Row {idx}] Checking item:")
                    print(f"  Item: '{item_value}' | Placeholder: '{item_placeholder}'")
                    print(f"  Quantity: '{quantity_value}' | Placeholder: '{quantity_placeholder}'")
                    print(f"  Is Item Empty: {is_item_empty}")
                    print(f"  Is Quantity Empty: {is_quantity_empty}")
                    
                    # Only remove if BOTH are empty
                    if is_item_empty and is_quantity_empty:
                        print(f"  → This row is EMPTY - Removing...")
                        
                        # Find and click the remove button
                        remove_btn = item.find_element(By.CSS_SELECTOR, "button.remove-btn")
                        
                        # Scroll into view
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", remove_btn)
                        time.sleep(0.3)
                        
                        # Wait and click
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(remove_btn))
                        driver.execute_script("arguments[0].click();", remove_btn)
                        
                        log_action(f"Removed empty row: item='{item_value}', qty='{quantity_value}'", 
                                log_file_path=log_file_path)
                        
                        print(f"  ✓ Successfully removed empty row")
                        removed_count += 1
                        time.sleep(0.5)
                        
                    else:
                        print(f"  ✓ This row has data - KEEPING")
                        kept_count += 1
                        
                except Exception as e:
                    log_error(f"Error processing row {idx}: {str(e)}", log_file_path=log_file_path)
                    print(f"\n[Row {idx}] ✗ Error: {e}")
            
            print("\n" + "="*50)
            print(f"Summary: Removed {removed_count} empty row(s), Kept {kept_count} valid row(s)")
            print("="*50)

        # REMOVE EXTRA "ADD ITEM" BUTTONS (keep only 1)
        print("\nChecking for extra 'Add Item' buttons...")
        time.sleep(1)

        add_item_buttons = driver.find_elements(By.CSS_SELECTOR, "#orderItems button[onclick*='addNewItem']")
        print(f"Found {len(add_item_buttons)} 'Add Item' button(s)")

        if len(add_item_buttons) > 1:
            print(f"Removing {len(add_item_buttons) - 1} extra 'Add Item' button(s)...")
            
            for idx, btn in enumerate(add_item_buttons[1:], start=2):
                try:
                    driver.execute_script("arguments[0].remove();", btn)
                    print(f"  ✓ Removed extra 'Add Item' button #{idx}")
                except Exception as e:
                    print(f"  ✗ Failed to remove button #{idx}: {e}")
            
            print(f"✓ Kept 1 'Add Item' button")
        elif len(add_item_buttons) == 1:
            print("✓ Only 1 'Add Item' button - perfect!")
        else:
            print("⚠ No 'Add Item' buttons found")

        print("\n" + "="*50)
        print("Finished processing purchase order items")
        print("="*50)
        

        WebDriverWait(driver,30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(10)
        driver.save_screenshot(os.path.join(screenshots_folder, "Product_Added.png"))

        # APPLY PRICE ADJUSTMENT
        apply_price_adj = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="orderForm"]/div[10]/button[1]')))
        driver.execute_script("arguments[0].click()", apply_price_adj)
        log_action("Click Apply Price Adjustment", log_file_path=log_file_path)

        # ENTER ADJUSTMENT AMOUNT
        amount = wait.until(EC.presence_of_element_located((By.ID, "adjustmentAmount")))
        amount.clear()
        amount.send_keys("5")
        log_action("Inputted Amount", log_file_path=log_file_path)
        WebDriverWait(driver,10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # ADJUSTMENT TYPE
        select_adjustment_type(driver, "increase")
        log_action("Selected: Increase Subtotal", log_file_path=log_file_path)
        WebDriverWait(driver,10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # APPLY ADJUSTMENT BUTTON
        apply_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'swal2-confirm') and text()='Apply']")))
        driver.execute_script("arguments[0].click();", apply_btn)
        log_action("Click Apply", log_file_path=log_file_path)
        WebDriverWait(driver,10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # APPLY SHIPPING FEE
        shipping_fee_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Apply Shipping Fee')]")))
        driver.execute_script("arguments[0].click()", shipping_fee_btn)
        log_action("Click Apply Shipping Fee", log_file_path=log_file_path)
        WebDriverWait(driver,10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # ENTER SHIPPING FEE AMOUNT
        shipping_fee_amount = wait.until(EC.presence_of_element_located((By.ID, "shippingFeeAdjustment")))
        shipping_fee_amount.send_keys("5")
        log_action("Inputted Amount", log_file_path=log_file_path)
        WebDriverWait(driver,10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # APPLY SHIPPING FEE BUTTON
        apply_shipping_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'swal2-confirm') and text()='Apply']")))
        driver.execute_script("arguments[0].click()", apply_shipping_btn)
        log_action("Click Apply", log_file_path=log_file_path)
        WebDriverWait(driver,10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # APPLY TAX    
        apply_tax_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@onclick='showTaxAdjustment()']")))
        driver.execute_script("arguments[0].click();", apply_tax_btn)
        log_action("Clicked Apply Tax", log_file_path=log_file_path)
        WebDriverWait(driver,10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # TAX TYPE
        tax_select = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "taxSelect")))
        selected_tax = select_tax_type(driver, tax_type="VAT", log_file_path=log_file_path) 
        WebDriverWait(driver,10).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        
        # TAX PERCENTAGE
        tax_percent = wait.until(EC.presence_of_element_located((By.ID, "taxAdjustment")))
        tax_percent.send_keys("12")
        log_action("Inputted Amount", log_file_path=log_file_path)
        WebDriverWait(driver,10).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    
        # APPLY TAX PERCENTAGE
        apply_tax_percent_btn = driver.find_element(By.CSS_SELECTOR, "button.swal2-confirm")
        driver.execute_script("arguments[0].click()", apply_tax_percent_btn)
        log_action("Click Apply", log_file_path=log_file_path)
        WebDriverWait(driver,10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # GRAND TOTAL
        grand_total = wait.until(EC.presence_of_element_located((By.ID, "Total")))
        log_action(f"Check Grand Total{grand_total.text}", log_file_path=log_file_path)
        WebDriverWait(driver,10).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(10)
        driver.save_screenshot(os.path.join(screenshots_folder, "Payment_Details.png"))

        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
       
        # SUBMIT SERVICE ORDER
        submit_order = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "submitOrder")))
        driver.execute_script("arguments[0].click();", submit_order)
        log_action("Submit Service Order",log_file_path=log_file_path)

        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(10)
        driver.save_screenshot(os.path.join(screenshots_folder, "After_Submit_Service_Order.png"))
        log_action("Service Order Submitted Successfully", log_file_path=log_file_path)

    except Exception as e:
        error_message = f"Element not found or interaction failed: {traceback.format_exc()}"
        log_error(error_message, log_file_path=log_file_path, driver=driver)
        print(error_message)
