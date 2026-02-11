import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Utility import log_action, log_error,clear_folder
from selenium.webdriver.support.ui import Select, WebDriverWait

from path_config import SCD_MODULE_PATHS


def branch_selection(driver, wait, log_file_path):

    log_file_path = SCD_MODULE_PATHS['BranchSelect']['log']
    screenshots_folder = SCD_MODULE_PATHS['BranchSelect']['screenshots']

    clear_folder(screenshots_folder=screenshots_folder)

    max_attempts = 10
    attempts = 0
    selection_successful = False

    while attempts < max_attempts and not selection_successful:
        try:
            # Wait for branch dropdown
            branch_dropdown = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, "branchSelect"))
            )

            Select(branch_dropdown).select_by_value("1")
            log_action("Selected HQ branch option", log_file_path=log_file_path)

            # Wait for terminal dropdown
            terminal_dropdown = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, "paymentTerminalSelect"))
            )

            select = Select(terminal_dropdown)

            for option in select.options:
                if "16080001" in option.get_attribute("value"):
                    select.select_by_value(option.get_attribute("value"))
                    log_action(
                        f"Selected terminal option: {option.get_attribute('value')}",
                        log_file_path=log_file_path
                    )
                    break

            # Wait for confirm button
            confirm_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[6]/button[1]"))
            )

            confirm_btn.click()
            log_action("Clicked branch confirmation button", log_file_path=log_file_path)

            selection_successful = True

        except Exception as e:
            attempts += 1
            log_action(
                f"Attempt {attempts} failed: {str(e)}",
                log_file_path=log_file_path
            )

    if not selection_successful:
        log_error(
            "Failed to select branch after multiple attempts",
            log_file_path=log_file_path
        )