
import time
import os
import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from env_config import BASE_URL 

from Utility import (
    log_action,
    log_error,
    clear_folder,
    wait_and_click_ok,
    fill_all_rows_with_same_values,
)

from path_config import SCD_MODULE_PATHS


def SCDBooking_Bulk(driver, wait):
    # -------------------
    # Setup paths
    # -------------------

    wait = WebDriverWait(driver, 30)

    log_file_path = SCD_MODULE_PATHS["SCDBooking_Bulk"]["log"]
    screenshots_folder = SCD_MODULE_PATHS["SCDBooking_Bulk"]["screenshots"]

    clear_folder(screenshots_folder=screenshots_folder)

    try:
       
        # url = "http://beta-opibizscd.paybps.ovpn/ServiceCenter/BatchUploadBookingAppointments"
        url = f"{BASE_URL}/BatchUploadBookingAppointments"
        driver.get(url)
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        driver.save_screenshot(os.path.join(screenshots_folder, "Navigate_Bulk_Booking.png"))

        # -------------------
        # Upload Excel file
        # -------------------
        excel_path = r"d:\Bastion\SQA_QualityEnterprise\SoftwareTesting\Projects\Common\Automation\OPI\Files\Testdata\SCD_BULK_BOOKINGAPPOINTMENT.xlsx"
        log_action(f"Excel File Path: {excel_path}", log_file_path)

        file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.filepond--browser")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", file_input)
        file_input.send_keys(excel_path)
        log_action("Uploaded Excel file for Bulk Booking Upload", log_file_path)

        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".filepond--item-processing")))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".filepond--item")))
        log_action("File upload processing completed", log_file_path)

        # -------------------
        # Submit Upload
        # -------------------
        upload_button = wait.until(EC.element_to_be_clickable((By.ID, "uploadButton")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", upload_button)
        driver.execute_script("arguments[0].click();", upload_button)
        log_action("Clicked Upload button for Bulk Booking Upload", log_file_path)

        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        driver.save_screenshot(os.path.join(screenshots_folder, "Bulk_Booking_Uploaded.png"))

        wait_and_click_ok(driver, timeout=30)
        driver.save_screenshot(os.path.join(screenshots_folder, "Bulk_Booking_Success.png"))

        # -------------------
        # Fill all rows with same values
        # -------------------
        fill_all_rows_with_same_values(driver, client_name="JOHN SANTOS", branch_name="HQ")
        log_action("Filled all rows with same values", log_file_path)
        time.sleep(2)

        # -------------------
        # Submit the filled data
        # -------------------
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, "submitAppointment")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_button)
        driver.execute_script("arguments[0].click();", submit_button)
        log_action("Clicked Submit button for Bulk Booking Submission", log_file_path)

        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        driver.save_screenshot(os.path.join(screenshots_folder, "Bulk_Booking_Submitted.png"))

        success_container = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.success")))
        log_action("Bulk Upload success screen is visible", log_file_path)

        return True

    except Exception as e:
        print(f" Unexpected error: {str(e)}")
        print(traceback.format_exc())

        driver.save_screenshot(os.path.join(screenshots_folder, "Unexpected_Error.png"))

        log_error(
            f"Unexpected error in SCDBooking_Bulk: {str(e)}\n{traceback.format_exc()}",
            log_file_path,
        )
        return False
