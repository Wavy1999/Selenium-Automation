# Standard library imports
import os
import traceback
from datetime import datetime

# Third-party imports (Selenium)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local / project-specific imports
from Utility import (
    log_action,
    log_error,
    clear_folder,
)
from path_config import SCD_MODULE_PATHS


def AnotherBank(driver, wait):

    # Get paths from configuration
    log_file_path = SCD_MODULE_PATHS['AnotherBank']['log']
    screenshots_folder = SCD_MODULE_PATHS['AnotherBank']['screenshots']

    # Clear old files before test run
    clear_folder(screenshots_folder=screenshots_folder)

    try:
        url = "http://beta-opibizscd.paybps.ovpn/EcoPay/TransferToOmnipay?tab=bank"
        driver.get(url)
        log_action(f"Navigated to {url}", log_file_path=log_file_path)

        # Wait for full page load (replaces time.sleep)
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))

        driver.save_screenshot(os.path.join(screenshots_folder, "To_Another_Account.png"))
        log_action("Another Bank page loaded successfully", log_file_path=log_file_path)

    except Exception:
        log_error(f"Send Money function encountered an error:\n{traceback.format_exc()}",log_file_path=log_file_path,driver=driver)
        driver.save_screenshot(os.path.join(screenshots_folder, "Critical_Error.png"))
        raise
