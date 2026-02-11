OPI Restaurant Center Automation
================================

This guide explains how to set up and run the Restaurant Center automation scripts.

1. Activate Python Virtual Environment
--------------------------------------
Open your terminal (PowerShell or CMD) and run:

.venv\Scripts\activate

You should see `(.venv)` in your terminal prompt after activation.

2. Install Dependencies
-----------------------
If not already installed, run:

pip install -r requirements.txt

Make sure `selenium` and `webdriver-manager` are installed.

3. Set the Active System
------------------------
Open `path_config.py` and set the system you want to test:

# ==========================================
# Choose ACTIVE System at runtime
# Options: "SCD", "REST", "ALL"
# ==========================================

ACTIVE_SYSTEM = "REST"    # <-- change as needed

Options:
- SCD – runs SCD modules only
- REST – runs Restaurant Center modules only
- ALL – runs both SCD and REST

4. Run Tests
------------
Navigate to your project folder where `SCD_ADMIN.py or test_scd_web.py` and is located and run:

pytest

- Executes all test modules based on the active system
- Test results will be logged in `Files/logs/`
- Screenshots of failures will be saved in `Files/screenshots/`

Optional: For detailed output:

pytest --verbose

Stop execution anytime with Ctrl+C.

5. Notes
--------
- Chrome browser is controlled automatically via Selenium WebDriver
- All modules must exist in the `OPI/Restaurant` structure
- If you encounter `ModuleNotFoundError`:
  1. Ensure the virtual environment is activated
  2. Confirm `sys.path` points to the OPI root where `path_config.py` exists
  3. Ensure folders are created properly (the automation creates them on import)

