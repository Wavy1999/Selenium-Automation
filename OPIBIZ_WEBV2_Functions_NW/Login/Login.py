# Standard library imports
import os
import time
import traceback

# Third‑party imports
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Local / project‑specific imports
from Utility import (
    log_action,
    log_error,
    clear_folder,
)
from path_config import LOGIN_PATHS

# =========================================================
#                    CORE LOGIN FUNCTION
# =========================================================
def perform_login(driver, username, password, log_file_path, screenshots_folder, label, wait_time=15):

    try:
        wait = WebDriverWait(driver, wait_time)

        # Wait for username input
        username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_input.clear()
        username_input.send_keys(username)
        log_action(f"Enter username [{label}]", log_file_path=log_file_path)

        # Wait for password input
        password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_input.clear()
        password_input.send_keys(password)
        log_action(f"Enter password [{label}]", log_file_path=log_file_path)

        # Take screenshot before submit
        screenshot_path = os.path.join(screenshots_folder, f"{label}_Login.png")
        driver.save_screenshot(screenshot_path)
        log_action(f"Login screenshot saved [{label}]", log_file_path=log_file_path)

        # Wait for login button and click
        login_button = wait.until(EC.element_to_be_clickable((By.NAME, "submit")))
        login_button.click()
        log_action(f"Click submit [{label}]", log_file_path=log_file_path)

    except (TimeoutException, NoSuchElementException) as e:
        log_error(f"Login failed for {label}: {e}", log_file_path=log_file_path)
        screenshot_path = os.path.join(screenshots_folder, f"{label}_Login_Failed.png")
        driver.save_screenshot(screenshot_path)
        raise Exception(f"Login failed for {label}: {e}")


# =========================================================
#                  DYNAMIC LOGIN FUNCTIONS
# =========================================================
def login_generic(driver, excel_path, login_key, username_override=None, password_override=None):

    config = LOGIN_PATHS[login_key]
    clear_folder(screenshots_folder=config['screenshots'])

    # Read Excel data for this login type
    data = pd.read_excel(excel_path, sheet_name=login_key)
    row = data.sample(n=1).iloc[0]

    username = username_override or row.get('Username') or "C.r001.OBiz.masteradmin"
    password = password_override or row.get('Password') or ":UOqNEzRvS0B"

    perform_login(driver, username, password, config['log'], config['screenshots'], login_key)
    return username, password


# =========================================================
#              INDIVIDUAL LOGIN WRAPPERS
# =========================================================
def login_admin(driver, excel_path):
    return login_generic(driver, excel_path, "Admin", username_override="C.r001.OBiz.masteradmin", password_override=":UOqNEzRvS0B")

def login_s1(driver, excel_path):
    return login_generic(driver, excel_path, "S1", username_override="B.R004.OBiz.branchopstaff", password_override="MRgC04H21G30")

def login_s2(driver, excel_path):
    return login_generic(driver, excel_path, "S2", username_override="B.R004.OBiz.branchopstaff", password_override="MRgC04H21G30")

def login_logistics(driver, excel_path):
    return login_generic(driver, excel_path, "Logistics")

def login_secad(driver, excel_path):
    return login_generic(driver, excel_path, "SecAd")

def login_class_c(driver, excel_path):
    return login_generic(driver, excel_path, "Class_C", username_override="C.r001.OBiz.masteradmin", password_override=":UOqNEzRvS0B")
