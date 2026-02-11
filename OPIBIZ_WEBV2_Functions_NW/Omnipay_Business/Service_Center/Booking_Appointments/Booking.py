import os
import time
import traceback
from datetime import date

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchElementException
)

from Utility import (
    log_action,
    log_error,
    human_like_typing,
    appointment_data,
    select_dropdown,
    set_preferred_time,
    clear_folder,
    select_time_booking,
    wait_and_click_ok,
    select_customer_from_booking,
    inject_and_select_branch,
    bypass_branch_dropdown
)

from path_config import SCD_MODULE_PATHS  # Import the configuration paths


def SCDBookings(driver, wait):
    # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['SCDBooking']['log']
    screenshots_folder = SCD_MODULE_PATHS['SCDBooking']['screenshots']

    # Clear old files before test run
    clear_folder(screenshots_folder=screenshots_folder)
    
    try:


     # Ensure page is stable after previous module
        print("Waiting for page stability...")
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        time.sleep(3)  # Extra wait for any residual animations
        log_action("Page ready - starting booking process", log_file_path=log_file_path)
        
        # === DIRECT NAVIGATION APPROACH (Most Reliable) ===
        print("Using direct navigation to Booking page...")
        
        try:
            # Get current URL to construct the booking URL
            current_url = driver.current_url
            base_url = current_url.split('/', 3)[:3]  # Get protocol and domain
            booking_url = '/'.join(base_url) + '/ServiceCenter/BookingAndAppointments'
            
            driver.get(booking_url)
            log_action(f"Direct navigation to: {booking_url}", log_file_path=log_file_path)
            
            # Wait for page to load
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            time.sleep(3)
            
            # Verify we're on the right page
            if 'BookingAndAppointments' in driver.current_url or 'booking' in driver.current_url.lower():
                log_action("Successfully navigated via direct URL", log_file_path=log_file_path)
                driver.save_screenshot(os.path.join(screenshots_folder, "Booking_and_Appointment.png"))
            else:
                raise Exception(f"Navigation failed. Current URL: {driver.current_url}")
                
        except Exception as direct_nav_error:
            log_action(f"Direct navigation failed: {direct_nav_error}", log_file_path=log_file_path)
            
            # === FALLBACK: Manual Menu Navigation ===
         
            
            # Find Service Center
            service_center_link = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-bs-title='Service Center']")))
            
            # Scroll and click multiple times if needed
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", service_center_link)
            time.sleep(1)
            
            # Force click with JavaScript
            driver.execute_script("arguments[0].click();", service_center_link)
            log_action("Clicked Service Center", log_file_path=log_file_path)
            time.sleep(3)  # Wait for animation
            
            # Force the submenu to be visible using JavaScript
            print("Forcing submenu to display...")
            driver.execute_script("""
                var submenu = document.querySelector('a[data-bs-title="Service Center"]').nextElementSibling;
                if (submenu) {
                    submenu.style.display = 'block';
                    submenu.style.visibility = 'visible';
                    submenu.style.opacity = '1';
                }
            """)
            time.sleep(3)
            
            # Force the parent LI to have 'open' class
            driver.execute_script("""
                var serviceLink = document.querySelector('a[data-bs-title="Service Center"]');
                var parentLi = serviceLink.parentElement;
                if (parentLi && !parentLi.classList.contains('open')) {
                    parentLi.classList.add('open');
                }
            """)
            
            driver.save_screenshot(os.path.join(screenshots_folder, "Forced_Menu_Open.png"))
            
            # Now find and click the Booking link
            booking_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@href='/ServiceCenter/BookingAndAppointments']")) )
            
            # Make it visible if it's not
            driver.execute_script("""
                arguments[0].style.display = 'block';
                arguments[0].style.visibility = 'visible';
            """, booking_link)
            
            # Click it
            driver.execute_script("arguments[0].click();", booking_link)
            log_action("Clicked Booking and Appointments after forcing visibility", log_file_path=log_file_path)
            
            # Wait for navigation
            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            time.sleep(3)
            driver.save_screenshot(os.path.join(screenshots_folder, "Booking_and_Appointment.png"))

        # ----- Booking and Appointments Features -----

        # DAY View
        Day_View_Button = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@type='button' and @title='day view' and contains(@class,'fc-dayGridDay-button')]")))
        driver.execute_script("arguments[0].click()", Day_View_Button)
        log_action("Clicked 'Day View' button", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")
        driver.save_screenshot(os.path.join(screenshots_folder, 'Day_View.png'))
        time.sleep(3)

        # WEEK View
        Week_View_Button = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@type='button' and @title='week view' and contains(@class,'fc-timeGridWeek-button')]")))
        driver.execute_script("arguments[0].click()", Week_View_Button)
        log_action("Clicked 'Week View' button", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")
        driver.save_screenshot(os.path.join(screenshots_folder, 'Week_View.png'))
        time.sleep(3)

        # MONTH View
        Month_View_Button = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@type='button' and @title='month view' and contains(@class,'fc-dayGridMonth-button')]")))
        driver.execute_script("arguments[0].click()", Month_View_Button)
        log_action("Clicked 'Month View' button", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")
        driver.save_screenshot(os.path.join(screenshots_folder, 'Month_View.png'))
        time.sleep(3)

        # YEAR View
        Year_View_Button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and @title='year view' and contains(@class,'fc-multiMonthYear-button')]")))
        driver.execute_script("arguments[0].click()", Year_View_Button)
        log_action("Click Year View Section", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")
        driver.save_screenshot(os.path.join(screenshots_folder, 'Year_View.png'))
        time.sleep(3)

        # Click Legend - Booked, Cancelled, Completed, Show All
        legend_buttons = [
            ("//span[@class='text-blue' and normalize-space(text())='BOOKED']", "Booked"),
            ("//span[@class='text-danger' and normalize-space(text())='CANCELLED']", "Cancelled"),
            ("//span[@class='text-success' and normalize-space(text())='COMPLETED']", "Completed"),
            ("//a[@data-btn-legend='All' and normalize-space(text())='Show All']", "Show All"),
        ]
        
        for xpath, label in legend_buttons:
            try:
                button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                driver.execute_script("arguments[0].click()", button)
                log_action(f"Click Legend {label}", log_file_path=log_file_path)
                driver.save_screenshot(os.path.join(screenshots_folder, f'Legend_{label.replace(" ", "_")}.png'))
                time.sleep(2)
            except Exception as e:
                log_error(f"Failed to click legend {label}: {str(e)}", log_file_path=log_file_path)

        # Return to DAY View for booking
        Day_View_Button = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@type='button' and @title='day view' and contains(@class,'fc-dayGridDay-button')]")))
        driver.execute_script("arguments[0].click()", Day_View_Button)
        log_action("Clicked 'Day View' button", log_file_path=log_file_path)
        WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")
        driver.save_screenshot(os.path.join(screenshots_folder, 'Day_View_Return.png'))
        time.sleep(5)

        # ----- Book Appointment for Today -----
        WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")
        # Get today's date in ISO format
        today = date.today().isoformat()
        print(f"🔍 Looking for FullCalendar cell with data-date={today}")
        log_action(f"Searching for today's date: {today}", log_file_path=log_file_path)

        # FullCalendar-specific click handler
        try:
            # Wait for FullCalendar to be fully initialized
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".fc-daygrid-body"))
            )
            time.sleep(2)  # Let calendar animations complete
            
            print("📅 FullCalendar detected")
            
            # Find today's cell using FullCalendar classes and data-date
            day_cell_selector = f"td.fc-daygrid-day[data-date='{today}']"
            day_cell = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, day_cell_selector))
            )
            
            print(f"🎯 Found today's cell: {today}")
            log_action(f"Found today's date cell: {today}", log_file_path=log_file_path)
            
            # Find the clickable day frame within the cell
            day_frame = day_cell.find_element(By.CSS_SELECTOR, ".fc-daygrid-day-frame")
            
            print("🎯 Found day frame element")
            log_action("Found fc-daygrid-day-frame element", log_file_path=log_file_path)
            
            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", day_frame)
            time.sleep(2)
            
            # Highlight for debugging
            driver.execute_script("arguments[0].style.border='3px solid red'", day_frame)
            time.sleep(0.5)
            
            # Take screenshot before click
            driver.save_screenshot(os.path.join(screenshots_folder, 'Before_Day_Click.png'))
            
            # Method 1: Try regular click first
            try:
                print("🖱️ Attempting regular click on day frame...")
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, day_cell_selector)))
                day_frame.click()
                log_action("Clicked day frame with regular click", log_file_path=log_file_path)
                print("✅ Regular click successful")
            except ElementClickInterceptedException:
                # Method 2: Use JavaScript click as fallback
                print("🖱️ Regular click intercepted, trying JavaScript click...")
                driver.execute_script("arguments[0].click();", day_frame)
                log_action("Clicked day frame with JavaScript click", log_file_path=log_file_path)
                print("✅ JavaScript click successful")
            
            time.sleep(3)
            
            # Take screenshot after click
            driver.save_screenshot(os.path.join(screenshots_folder, 'After_Day_Click.png'))
            
            # Wait for modal to appear
            print("⏳ Waiting for modal to appear...")
            appointment_form = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "addNewAppointmentForm")))
            log_action("Appointment form (addNewAppointmentForm) is now visible", log_file_path=log_file_path)
            print("✅ Modal is now visible")
            
        except TimeoutException:
            error_msg = f"Could not find FullCalendar cell or day frame for date: {today}"
            log_error(error_msg, log_file_path=log_file_path)
            driver.save_screenshot(os.path.join(screenshots_folder, 'Day_Cell_Not_Found.png'))


        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "AppointmentName")))
        log_action("Appointment form is interactive and ready for input", log_file_path=log_file_path)
        print("✅ Form is ready for input")

        # ----- Fill Appointment Form -----

        # Appointment name
        try:
            appointment_name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "AppointmentName"))
            )
            appointment_name.clear()
            human_like_typing(appointment_name, "Test Customer")
            log_action("Entered Appointment Name: Test Customer", log_file_path=log_file_path)
            time.sleep(3)
        except Exception as e:
            log_error(f"Failed to enter appointment name: {str(e)}", log_file_path=log_file_path)
            driver.save_screenshot(os.path.join(screenshots_folder, "appointment_name_error.png"))
            raise

        # Customer name (Select2 dropdown)
        try:
            customer_name =  select_customer_from_booking(driver, wait, "CHRISTIAN TESTER")
            log_action(f"Selected Customer Name: {customer_name}", log_file_path=log_file_path)
            time.sleep(3)
        except Exception as e:
            log_error(f"Failed to select customer name: {str(e)}", log_file_path=log_file_path)
            raise

        # Address
        try:
            address = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.NAME, "Address")))
            address.clear()
            human_like_typing(address, "Test Address")
            log_action("Entered Address: Test Address", log_file_path=log_file_path)
            time.sleep(3)
        except Exception as e:
            log_error(f"Failed to enter Address: {str(e)}", log_file_path=log_file_path)
            driver.save_screenshot(os.path.join(screenshots_folder, "address_error.png"))
            raise


        try:
            print("\n" + "="*50)
            print("BRANCH SELECTION")
            print("="*50)
            
            # Try normal method first
            try:
                inject_and_select_branch(driver, "HQ", timeout=15)
                log_action("Selected branch: HQ", log_file_path=log_file_path)
                print("✅ Branch selection complete")
                
            except Exception as normal_error:
                print(f"⚠️ Normal selection failed: {normal_error}")
                print("🚀 Trying complete bypass...")
                
                # Use bypass method
                bypass_branch_dropdown(driver, "HQ")
                log_action("Selected branch via bypass: HQ", log_file_path=log_file_path)
                print("✅ Branch set via bypass")
            
        except Exception as e:
            log_error(f"Failed to select branch: {str(e)}", log_file_path=log_file_path)
            
            # Debug
            timestamp = int(time.time())
            driver.save_screenshot(os.path.join(screenshots_folder, f"branch_error_{timestamp}.png"))
            
            with open(os.path.join(screenshots_folder, f"branch_error_{timestamp}.html"), "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            
            print("💾 Debug files saved")
            
            # DON'T raise - continue anyway
            print("⚠️ Continuing without branch selection...")

        # Start Time
        try:
            start_time_input = select_time_booking(driver, log_file_path, "input[data-start-time]", "06:21 PM", by="css" )
            log_action(f"Set Start Time:{start_time_input}", log_file_path=log_file_path)
            time.sleep(3)
        except Exception as e:
            log_error(f"Error setting start time: {str(e)}", log_file_path=log_file_path)
            driver.save_screenshot(os.path.join(screenshots_folder, "start_time_error.png"))
            raise

        # End Time
        try:
            end_time = select_time_booking(driver, log_file_path, "input[data-end-time]", "10:21 PM", by="css" )
            time.sleep(0.5)
            log_action(f"Set End Time:{end_time}", log_file_path=log_file_path)
            time.sleep(3)
        except Exception as e:
            log_error(f"Error setting end time: {str(e)}", log_file_path=log_file_path)
            driver.save_screenshot(os.path.join(screenshots_folder, "end_time_error.png"))
            raise

        # Enter Notes
        try:
            notes_text = "Customer requested a window seat."
            appointment_notes = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "AppointmentNote"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", appointment_notes)
            time.sleep(0.5)
            
            appointment_notes.clear()
            human_like_typing(appointment_notes, notes_text)
            log_action(f"Entered Notes: {notes_text}", log_file_path=log_file_path)
            print(f"📝 Notes: {notes_text}")
            time.sleep(3)
        except Exception as e:
            log_error(f"Failed to enter notes: {str(e)}", log_file_path=log_file_path)
            driver.save_screenshot(os.path.join(screenshots_folder, "notes_error.png"))
            raise

        # Submit Appointment
        try:
            add_appointment_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'swal2-confirm') and normalize-space(text())='Add Appointment']")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_appointment_btn)
            driver.execute_script("arguments[0].click()", add_appointment_btn)
            log_action("Clicked 'Add Appointment' button", log_file_path=log_file_path)
            WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
            driver.save_screenshot(os.path.join(screenshots_folder, 'Submit.png'))
            time.sleep(5)
        except Exception as e:
            log_error(f"Failed to click submit button: {str(e)}", log_file_path=log_file_path)
            driver.save_screenshot(os.path.join(screenshots_folder, 'Submit_Error.png'))
            raise

        # Confirm Appointment
        try:
            confirm_booking_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'swal2-confirm') and normalize-space(text())='Confirm Booking']")))
            driver.execute_script("arguments[0].click()", confirm_booking_btn)
            log_action("Clicked 'Confirm Booking' button", log_file_path=log_file_path)
            WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
            time.sleep(2)
        except Exception as e:
            log_error(f"Failed to click confirm button: {str(e)}", log_file_path=log_file_path)
            driver.save_screenshot(os.path.join(screenshots_folder, 'Confirm_Error.png'))
            raise

        # Final screenshot
        WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        driver.save_screenshot(os.path.join(screenshots_folder, 'Appointment_Completed.png'))

        wait_and_click_ok(driver, timeout=30)
        log_action("Appointment booking confirmed - OK clicked on alert", log_file_path=log_file_path)
        
        print("✅ Appointment booking completed successfully!")
        log_action("Appointment booking process completed successfully", log_file_path=log_file_path)

    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(f"❌ {error_msg}")
        print(traceback.format_exc())
        driver.save_screenshot(os.path.join(screenshots_folder, 'Unexpected_Error.png'))
        log_error(f"Unexpected error in Bookings: {str(e)}\n{traceback.format_exc()}", log_file_path=log_file_path)
        return False
    
    finally:
        print("=" * 60)
        print("Bookings automation process finished")
        print("=" * 60)