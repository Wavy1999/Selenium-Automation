# conftest.py
# Shared pytest fixtures for SCD Web Test Suite
# Based on Admin.py automation structure

import os
import sys
import time
import pytest
from datetime import datetime
from typing import Optional
import base64
import shutil
import io
from contextlib import redirect_stdout

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait

# Process and monitor management
import psutil
import screeninfo

# Allure reporting
import allure
from allure_commons.types import AttachmentType

# Add paths to custom modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'OPIBIZ_WEBV2_Functions_NW')))

# Utility Files
from Utility import log_action, clear_terminal, clear_folder, log_error


# ==========================================
#           VERSION INFORMATION
# ==========================================
VERSION = "1.2.2.R0002B"
BUILD_DATE = "2026-1-23"


# ==========================================
#           GLOBAL VARIABLES
# ==========================================
browser_version = "Unknown"
start_time = None
end_time = None 
test_results = {
    'passed': [],
    'failed': [],
    'skipped': []
}
_test_logs = {}  # Stores captured logs per test nodeid
_current_log_file_path = None  # Global log file path for hooks
_current_test_output = {}  # NEW: Stores stdout capture per test (from capfd fixture)

# OmniPay Logo Path
OMNIPAY_LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "omnipay_logo.png")


# ==========================================
#           CONFIGURATION CLASS
# ==========================================
class TestConfig:
    """Test configuration settings - Modify these values as needed"""
    
    # Environment configuration
    BASE_URL: str = "http://vm-app-dev01:9001/"
    LOGIN_TYPE: str = "s1"  # Options: "admin", "s1", "s2"
    
    # Tester configuration
    TESTER_NAME: str = "Christian"
    BROWSER: str = "Chrome"
    
    # Monitor configuration
    USE_SECOND_MONITOR: bool = True
    MONITOR_OFFSET: int = 1920  # X offset (typically primary monitor width)
    
    # Timeout settings
    DEFAULT_WAIT: int = 15
    PAGE_LOAD_TIMEOUT: int = 30
    IMPLICIT_WAIT: int = 10
    
    # Page zoom
    PAGE_ZOOM: str = "75%"
    
    # Paths (will be set during setup)
    SCREENSHOTS_DIR: Optional[str] = None
    REPORTS_DIR: Optional[str] = None
    LOG_FILE_PATH: Optional[str] = None
    
    # Browser version (will be set after initialization)
    BROWSER_VERSION: Optional[str] = None


# Global config instance
_config = TestConfig()


# ==========================================
#           TESTER INFORMATION
# ==========================================
TESTER_NAME = "Christian"


# =====================================
# CONFIGURATION
# =====================================
BASE_URL = "http://vm-app-dev01:9001/"
USE_SECOND_MONITOR = True
MONITOR_OFFSET = 1920
PAGE_ZOOM = "75%"
BROWSER = "Chrome"


# ==========================================
#           HELPER FUNCTIONS
# ==========================================

def get_logo_base64():
    """Get logo as base64 string"""
    try:
        if os.path.exists(OMNIPAY_LOGO_PATH):
            with open(OMNIPAY_LOGO_PATH, "rb") as f:
                return base64.b64encode(f.read()).decode()
    except Exception:
        pass
    return None


def print_header(config: TestConfig) -> None:
    """Print test execution header"""
    print("=" * 80)
    print("OMNIPAY BUSINESS SCD WEB TEST SUITE".center(80))
    print(f"Version {VERSION}".center(80))
    print("=" * 80)
    print()
    print(f"  📋 Project      : Omnipay SCD Web")
    print(f"  🏷️  Version      : {VERSION} (Build: {BUILD_DATE})")
    print(f"  👤 Tester       : {config.TESTER_NAME}")
    print(f"  🌐 Browser      : {config.BROWSER}")
    print(f"  🔗 Environment  : {config.BASE_URL}")
    print(f"  📅 Date         : {datetime.now().strftime('%Y-%m-%d')}")
    print(f"  ⏰ Start Time   : {datetime.now().strftime('%H:%M:%S')}")
    if config.USE_SECOND_MONITOR:
        print(f"  🖥️  Monitor      : Second Monitor (offset: {config.MONITOR_OFFSET}px)")
    else:
        print(f"  🖥️  Monitor      : Primary Monitor")
    print()
    print("=" * 80)
    print()


def setup_directories() -> tuple:
    """Setup log and screenshot directories"""
    global _current_log_file_path
    
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(current_file_dir, "Reports")
    screenshots_dir = os.path.join(current_file_dir, "Screenshots")
    
    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(screenshots_dir, exist_ok=True)
    clear_folder(screenshots_dir)
    
    log_filename = f"test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    log_file_path = os.path.join(reports_dir, log_filename)
    
    # Set global log file path for use in hooks
    _current_log_file_path = log_file_path
    
    print(f"📁 Reports directory: {reports_dir}")
    print(f"📁 Screenshots directory: {screenshots_dir}")
    print(f"📝 Log file: {log_file_path}")
    
    return reports_dir, screenshots_dir, log_file_path


def capture_screenshot(driver, name: str, screenshots_dir: str) -> Optional[str]:
    """Capture screenshot and attach to Allure report"""
    try:
        os.makedirs(screenshots_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = os.path.join(screenshots_dir, f"{name}_{timestamp}.png")
        
        driver.save_screenshot(filepath)
        allure.attach(
            driver.get_screenshot_as_png(),
            name=name,
            attachment_type=AttachmentType.PNG
        )
        print(f"📸 Screenshot captured: {name}")
        return filepath
    except Exception as e:
        print(f"⚠️ Screenshot failed: {e}")
        return None


def setup_chrome_driver(config: TestConfig) -> tuple:
    """Setup Chrome WebDriver with advanced configuration"""
    global browser_version  # CRITICAL: Declare global to update module-level variable
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    
    # Stability options
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    # Set page load strategy
    chrome_options.page_load_strategy = 'normal'
    
    # Disable Chrome save dialogs and autofill
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "autofill.profile_enabled": False,
        "autofill.credit_card_enabled": False,
        "autofill.address_enabled": False,
        "autofill.enabled": False
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Initialize ChromeDriver
    print("\n🔧 Initializing Chrome WebDriver...")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Track PIDs for cleanup
    browser_pids = []
    try:
        service_pid = service.process.pid
        service_proc = psutil.Process(service_pid)
        browser_pids = [service_proc.pid] + [c.pid for c in service_proc.children(recursive=True)]
        print(f"📌 Tracking {len(browser_pids)} browser process(es) for cleanup")
    except Exception:
        pass
    
    # ============================================
    # DETECT BROWSER VERSION - MULTIPLE METHODS
    # ============================================
    try:
        # Method 1: Get from capabilities (most reliable)
        caps = driver.capabilities
        
        # Try different capability keys
        browser_version = caps.get('browserVersion') or \
                         caps.get('version') or \
                         caps.get('chrome', {}).get('chromedriverVersion', '').split(' ')[0] or \
                         "Unknown"
        
        # Method 2: If still unknown, try to get from userAgent
        if browser_version == "Unknown":
            user_agent = driver.execute_script("return navigator.userAgent;")
            # Parse Chrome version from userAgent
            # Example: "Mozilla/5.0 ... Chrome/120.0.6099.109 Safari/537.36"
            import re
            chrome_match = re.search(r'Chrome/(\d+\.\d+\.\d+\.\d+)', user_agent)
            if chrome_match:
                browser_version = chrome_match.group(1)
        
        # Get additional browser info
        browser_name = caps.get('browserName', 'Chrome')
        platform = caps.get('platformName') or caps.get('platform', 'Unknown')
        
        print(f"✅ {browser_name} v{browser_version} initialized")
        print(f"   Platform: {platform}")
        
    except Exception as e:
        print(f"⚠️ Could not detect browser version: {e}")
        browser_version = "Unknown"
    
    # Update config
    config.BROWSER_VERSION = browser_version
    
    return driver, browser_pids


def setup_monitor_position(driver, config: TestConfig) -> None:
    """Setup browser position on monitor"""
    if config.USE_SECOND_MONITOR:
        try:
            monitors = screeninfo.get_monitors()
            if len(monitors) >= 2:
                m = monitors[1]
                print(f"🖥️  Moving browser to second monitor: {m.name} ({m.width}x{m.height})")
                driver.set_window_size(m.width, m.height)
                driver.set_window_position(m.x, m.y)
            else:
                print(f"⚠️ Only one monitor detected, using offset method")
                driver.set_window_position(config.MONITOR_OFFSET, 0)
            driver.maximize_window()
        except Exception as e:
            print(f"⚠️ Monitor detection failed: {e}")
            try:
                driver.set_window_position(config.MONITOR_OFFSET, 0)
                driver.maximize_window()
            except Exception:
                pass
    else:
        driver.maximize_window()


def cleanup_browser(driver, browser_pids: list, log_file_path: str) -> None:
    """Cleanup browser resources"""
    print("\n🧹 Cleaning up...")
    time.sleep(3)
    
    if driver:
        try:
            driver.quit()
            print("✅ Browser closed successfully")
        except Exception as e:
            print(f"⚠️ Driver quit warning: {str(e)}")
    
    # Force kill any remaining browser processes
    if browser_pids:
        killed_count = 0
        for pid in browser_pids:
            try:
                proc = psutil.Process(pid)
                if proc.is_running():
                    proc.terminate()
                    proc.wait(timeout=5)
                    killed_count += 1
            except (psutil.NoSuchProcess, psutil.TimeoutExpired, psutil.AccessDenied):
                pass
        if killed_count > 0:
            print(f"🔪 Force terminated {killed_count} remaining process(es)")
    
    if log_file_path:
        log_action("Browser closed and session ended", log_file_path=log_file_path)


# ==========================================
#           PYTEST FIXTURES
# Provide test configuration
# Provide log file path
# Provide screenshots directory
# Setup and teardown Chrome WebDriver
# ==========================================

@pytest.fixture(scope="session")
def test_config():
    
    config = TestConfig()
    config.REPORTS_DIR, config.SCREENSHOTS_DIR, config.LOG_FILE_PATH = setup_directories()
    return config

@pytest.fixture(scope="session")
def log_file_path(test_config):
    
    return test_config.LOG_FILE_PATH

@pytest.fixture(scope="session")
def screenshots_dir(test_config):
   
    return test_config.SCREENSHOTS_DIR

@pytest.fixture(scope="session")
def driver(test_config):
    
    global browser_version  # CRITICAL: Declare global here too
    
    clear_terminal()
    print_header(test_config)
    
    driver = None
    browser_pids = []
    
    try:
        # Setup driver (this sets browser_version globally)
        driver, browser_pids = setup_chrome_driver(test_config)
        
        # Ensure browser_version is synced from config
        if test_config.BROWSER_VERSION and test_config.BROWSER_VERSION != "Unknown":
            browser_version = test_config.BROWSER_VERSION
        
        # Setup monitor position
        setup_monitor_position(driver, test_config)
        
        # Navigate to base URL
        print(f"🌐 Navigating to: {test_config.BASE_URL}")
        driver.get(test_config.BASE_URL)
        
        # Set page zoom
        driver.execute_script(f"document.body.style.zoom='{test_config.PAGE_ZOOM}'")
        
        log_action(
            f"Setup completed - Version: {VERSION}, Browser: {test_config.BROWSER} v{browser_version}, Tester: {test_config.TESTER_NAME}",
            log_file_path=test_config.LOG_FILE_PATH
        )
        print(f"✅ Setup completed successfully")
        print(f"   Browser: {test_config.BROWSER} v{browser_version}\n")
        
        yield driver
        
    finally:
        cleanup_browser(driver, browser_pids, test_config.LOG_FILE_PATH)


# ==========================================
# Helper function to get browser version
# Get the current browser version (for use in HTML reports)
# ==========================================
def get_browser_version():
   
    global browser_version
    return browser_version if browser_version else "Unknown"


# ==========================================
# CRITICAL: AUTO-CAPTURE ALL STDOUT/STDERR
# This fixture automatically captures ALL output
# Automatically capture ALL stdout/stderr for each test.
# This runs for EVERY test and stores output in _current_test_output.
# ==========================================
@pytest.fixture(autouse=True)
def capture_all_test_output(request, capfd):
 
    global _current_test_output
    
    # Clear any previous output for this test
    test_nodeid = request.node.nodeid
    _current_test_output[test_nodeid] = ""
    
    yield  # Test runs here
    
    # After test completes, capture ALL output
    try:
        captured = capfd.readouterr()
        
        all_output = ""
        if captured.out:
            all_output += captured.out
        if captured.err:
            if all_output:
                all_output += "\n"
            all_output += captured.err
        
        # Store captured output for this test
        _current_test_output[test_nodeid] = all_output
        
    except Exception as e:
        print(f"⚠️ Log capture warning: {e}")


@pytest.fixture(scope="session")
def wait(driver, test_config):
    # Provide WebDriverWait instance #
    return WebDriverWait(driver, test_config.DEFAULT_WAIT)

# Provide WebDriverWait instance for function scope (refreshed each test) #
@pytest.fixture(scope="function")
def function_wait(driver, test_config):

    return WebDriverWait(driver, test_config.DEFAULT_WAIT)


# ==========================================
#           PYTEST HOOKS
# ==========================================

# Configure pytest and clean up old reports #
def pytest_configure(config):
 
    report_path = os.path.join(os.getcwd(), "Automation_Test_report.html")
    if os.path.exists(report_path):
        os.remove(report_path)

    screenshots_dir = os.path.join(os.getcwd(), "screenshots")
    if os.path.exists(screenshots_dir):
        shutil.rmtree(screenshots_dir)
    os.makedirs(screenshots_dir, exist_ok=True)

    if not hasattr(config, "_metadata"):
        config._metadata = {}
    
    config._metadata.update({
        "Project": "SCD WEB - BDD Automation",
        "Version": VERSION,
        "Framework": "Pytest-BDD + Selenium",
        "Tester": TESTER_NAME,
        "Test Approach": "Behavior Driven Development (BDD)",
        "Browser": BROWSER,
        "Execution Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# Initialize session start time and print header #
def pytest_sessionstart(session):
    
    global start_time
    start_time = datetime.now()

    print("=" * 70)
    print("OMNIPAY BUSINESS SCD WEB AUTOMATION".center(70))
    print(f"Version {VERSION}".center(70))
    print("=" * 70)
    print()
    print(f"  📋 Project      : Omnipay SCD Web")
    print(f"  🏷️  Version      : {VERSION} (Build: {BUILD_DATE})")
    print(f"  👤 Tester       : {TESTER_NAME}")
    print(f"  🌐 Browser      : {BROWSER}")
    print(f"  🔗 Environment  : {BASE_URL}")
    print(f"  📅 Date         : {datetime.now().strftime('%Y-%m-%d')}")
    print(f"  ⏰ Start Time   : {datetime.now().strftime('%H:%M:%S')}")
    if USE_SECOND_MONITOR:
        print(f"  🖥️  Monitor      : Second Monitor (offset: {MONITOR_OFFSET}px)")
    else:
        print(f"  🖥️  Monitor      : Primary Monitor")
    print()
    print("=" * 70)


# =====================================
# TEST SETUP/TEARDOWN HOOKS
# =====================================

# Log action when test starts #
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    
    global _current_log_file_path
    
    # Get test name
    test_name = item.name
    
    # Handle parametrized tests - extract readable name
    if hasattr(item, 'callspec'):
        params = item.callspec.params
        if 'module_name' in params:
            test_name = params['module_name']
    
    # Log test start
    if _current_log_file_path:
        log_action(f"[START] {test_name} - Test execution started", log_file_path=_current_log_file_path)
    
    print(f"\n{'='*60}")
    print(f"🚀 STARTING: {test_name}")
    print(f"{'='*60}")


# =====================================
# REPORT GENERATION HOOK
# =====================================

# Generate test execution summary report after all tests complete #
def pytest_sessionfinish(session, exitstatus):
    
    global test_results, browser_version, start_time, _current_log_file_path
    
    end_time = datetime.now()
    
    # Calculate execution time
    if start_time is not None:
        total_time = (end_time - start_time).total_seconds()
        hours, remainder = divmod(total_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            duration_str = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
        elif minutes > 0:
            duration_str = f"{int(minutes)}m {int(seconds)}s"
        else:
            duration_str = f"{seconds:.2f}s"
    else:
        duration_str = "N/A"
    
    # Get browser version (ensure it's not None)
    current_browser_version = browser_version if browser_version else "Unknown"
    
    print("\n" + "=" * 70)
    print("📊 TEST EXECUTION SUMMARY".center(70))
    print(f"Version {VERSION}".center(70))
    print("=" * 70)
    
    # Test execution info
    print(f"\n  🏷️  Version      : {VERSION}")
    print(f"  👤 Tester       : {TESTER_NAME}")
    print(f"  🌐 Browser      : {BROWSER} v{current_browser_version}")
    print(f"  🔗 Environment  : {BASE_URL}")
    print(f"  📅 Start Time   : {start_time.strftime('%Y-%m-%d %H:%M:%S') if start_time else 'N/A'}")
    print(f"  📅 End Time     : {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  ⏱️  Duration     : {duration_str}")
    print()
    
    total_tests = len(test_results['passed']) + len(test_results['failed']) + len(test_results['skipped'])
    passed = len(test_results['passed'])
    failed = len(test_results['failed'])
    skipped = len(test_results['skipped'])
    
    print(f"  📈 Total Tests  : {total_tests}")
    print(f"  ✅ Passed       : {passed} ({(passed/total_tests*100) if total_tests > 0 else 0:.1f}%)")
    print(f"  ❌ Failed       : {failed} ({(failed/total_tests*100) if total_tests > 0 else 0:.1f}%)")
    print(f"  ⏭️  Skipped      : {skipped} ({(skipped/total_tests*100) if total_tests > 0 else 0:.1f}%)")
    
    if test_results['passed']:
        print("\n  ✅ Passed Tests:")
        for test in test_results['passed']:
            print(f"     • {test}")
    
    if test_results['failed']:
        print("\n  ❌ Failed Tests:")
        for test in test_results['failed']:
            print(f"     • {test}")
    
    if test_results['skipped']:
        print("\n  ⏭️  Skipped Tests:")
        for test in test_results['skipped']:
            print(f"     • {test}")
    
    print("\n" + "=" * 70)
    print(f"⏱️  Total Execution Time: {duration_str}")
    print("=" * 70 + "\n")
    
    # Log the summary
    if _current_log_file_path:
        log_action("=" * 50, log_file_path=_current_log_file_path)
        log_action("TEST EXECUTION SUMMARY", log_file_path=_current_log_file_path)
        log_action("=" * 50, log_file_path=_current_log_file_path)
        log_action(f"Browser: {BROWSER} v{current_browser_version}", log_file_path=_current_log_file_path)
        log_action(f"Total Tests: {total_tests}", log_file_path=_current_log_file_path)
        log_action(f"Passed: {passed} ({(passed/total_tests*100) if total_tests > 0 else 0:.1f}%)", log_file_path=_current_log_file_path, success=True)
        log_action(f"Failed: {failed} ({(failed/total_tests*100) if total_tests > 0 else 0:.1f}%)", log_file_path=_current_log_file_path)
        log_action(f"Skipped: {skipped} ({(skipped/total_tests*100) if total_tests > 0 else 0:.1f}%)", log_file_path=_current_log_file_path)
        log_action(f"Total Execution Time: {duration_str}", log_file_path=_current_log_file_path)
        log_action("=" * 50, log_file_path=_current_log_file_path)
    
    # Save summary to file
    try:
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        reports_dir = os.path.join(current_file_dir, "Reports")
        os.makedirs(reports_dir, exist_ok=True)
        
        summary_file = os.path.join(reports_dir, f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("TEST EXECUTION SUMMARY\n")
            f.write(f"Version {VERSION}\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Version      : {VERSION}\n")
            f.write(f"Tester       : {TESTER_NAME}\n")
            f.write(f"Browser      : {BROWSER} v{current_browser_version}\n")
            f.write(f"Environment  : {BASE_URL}\n")
            f.write(f"Start Time   : {start_time.strftime('%Y-%m-%d %H:%M:%S') if start_time else 'N/A'}\n")
            f.write(f"End Time     : {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Duration     : {duration_str}\n\n")
            f.write(f"Total Tests  : {total_tests}\n")
            f.write(f"Passed       : {passed} ({(passed/total_tests*100) if total_tests > 0 else 0:.1f}%)\n")
            f.write(f"Failed       : {failed} ({(failed/total_tests*100) if total_tests > 0 else 0:.1f}%)\n")
            f.write(f"Skipped      : {skipped} ({(skipped/total_tests*100) if total_tests > 0 else 0:.1f}%)\n\n")
            f.write(f"Total Execution Time: {duration_str}\n\n")
            
            if test_results['passed']:
                f.write("Passed Tests:\n")
                for test in test_results['passed']:
                    f.write(f"  ✅ {test}\n")
                f.write("\n")
            
            if test_results['failed']:
                f.write("Failed Tests:\n")
                for test in test_results['failed']:
                    f.write(f"  ❌ {test}\n")
                f.write("\n")
            
            if test_results['skipped']:
                f.write("Skipped Tests:\n")
                for test in test_results['skipped']:
                    f.write(f"  ⏭️ {test}\n")
                f.write("\n")
            
            f.write("=" * 70 + "\n")
        
        print(f"📄 Summary report saved: {summary_file}")
        
    except Exception as e:
        print(f"⚠️ Failed to save summary report: {e}")


# ---------------------- HTML REPORT CUSTOMIZATION ----------------------
# Set HTML report title #
def pytest_html_report_title(report):
  
    report.title = "🔄 OmniPay SCD Web Automation Report"

# Customize HTML report summary section #
def pytest_html_results_summary(prefix, summary, postfix):
    
    summary_html = f'''
    <div style="text-align:center; margin:20px 0; padding:20px; background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius:10px; color:white;">
        <h1 style="margin:0; font-size:32px; text-shadow:2px 2px 4px rgba(0,0,0,0.3);">
            🍽️ SCD WEB Test Report
        </h1>
        <p style="margin:5px 0; opacity:0.9;">Automated Testing Results</p>
    </div>
    
    <div style="background:#f8f9fa; padding:20px; border-radius:10px; margin:20px 0; border-left:5px solid #3498db; box-shadow:0 2px 10px rgba(0,0,0,0.1);">
        <h2 style="color:#2c3e50; margin-top:0; border-bottom:2px solid #3498db; padding-bottom:10px;">
            🎯 Test Execution Summary
        </h2>
        <table style="width:100%; border-collapse:collapse; margin:10px 0;">
            <tr style="background:#fff;">
                <td style="padding:10px; border:1px solid #ddd; font-weight:bold;">📦 Project:</td>
                <td style="padding:10px; border:1px solid #ddd;">SCD Web Omnipay Business</td>
            </tr>
            <tr style="background:#f9f9f9;">
                <td style="padding:10px; border:1px solid #ddd; font-weight:bold;">🔖 Version:</td>
                <td style="padding:10px; border:1px solid #ddd;">{VERSION}</td>
            </tr>
            <tr style="background:#fff;">
                <td style="padding:10px; border:1px solid #ddd; font-weight:bold;">🛠️ Framework:</td>
                <td style="padding:10px; border:1px solid #ddd;">Pytest + Selenium WebDriver</td>
            </tr>
            <tr style="background:#f9f9f9;">
                <td style="padding:10px; border:1px solid #ddd; font-weight:bold;">📐 Approach:</td>
                <td style="padding:10px; border:1px solid #ddd;">Behavior Driven Development (BDD)</td>
            </tr>
            <tr style="background:#fff;">
                <td style="padding:10px; border:1px solid #ddd; font-weight:bold;">👤 Tester:</td>
                <td style="padding:10px; border:1px solid #ddd;">{TESTER_NAME}</td>
            </tr>
            <tr style="background:#f9f9f9;">
                <td style="padding:10px; border:1px solid #ddd; font-weight:bold;">📅 Execution Date:</td>
                <td style="padding:10px; border:1px solid #ddd;">{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</td>
            </tr>
        </table>
        <p style="margin-top:15px; padding:10px; background:#d1ecf1; border:1px solid #bee5eb; border-radius:5px; color:#0c5460; font-size:13px;">
            ✅ Report is fully self-contained and can be viewed offline
        </p>
    </div>
    '''
    prefix.append(summary_html)



# ---------------------- TEST RESULT TRACKING & HTML REPORT ----------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Track test results and add logs/screenshots to HTML report"""
    global test_results, _test_logs, _current_log_file_path, _current_test_output
    
    outcome = yield
    report = outcome.get_result()
    
    # Only process 'call' phase (actual test execution)
    if report.when != "call":
        return
    
    # ---- Get test name ----
    test_name = item.name
    
    # Handle parametrized tests - extract readable name
    if hasattr(item, 'callspec'):
        params = item.callspec.params
        if 'module_name' in params:
            test_name = params['module_name']
    
    # ---- Calculate test duration ----
    duration = getattr(report, 'duration', 0)
    duration_str = f"{duration:.2f}s"
    
    # ---- Track test results and log action ----
    if report.passed:
        test_results['passed'].append(test_name)
        if _current_log_file_path:
            log_action(f"[PASSED] {test_name} - Duration: {duration_str}", log_file_path=_current_log_file_path, success=True)
        print(f"✅ {test_name} - PASSED (Duration: {duration_str})")
        
    elif report.failed:
        test_results['failed'].append(test_name)
        error_msg = str(report.longrepr) if report.longrepr else "Unknown error"
        # Truncate error message for log
        short_error = error_msg[:200] + "..." if len(error_msg) > 200 else error_msg
        if _current_log_file_path:
            log_error(f"[FAILED] {test_name} - Duration: {duration_str} - Error: {short_error}", log_file_path=_current_log_file_path)
        print(f"❌ {test_name} - FAILED (Duration: {duration_str})")
        
    elif report.skipped:
        test_results['skipped'].append(test_name)
        if _current_log_file_path:
            log_action(f"[SKIPPED] {test_name}", log_file_path=_current_log_file_path)
        print(f"⏭️ {test_name} - SKIPPED")
    
    # ---- HTML Report extras ----
    try:
        from pytest_html import extras
    except ImportError:
        return
    
    if not hasattr(report, 'extras'):
        report.extras = []
    
    # ============================================
    # CAPTURE ALL STDOUT LOGS - MULTIPLE METHODS
    # ============================================
    captured_logs = ""
    
    # METHOD 1 (MOST RELIABLE): Get from our autouse capfd fixture
    if item.nodeid in _current_test_output and _current_test_output[item.nodeid]:
        captured_logs = _current_test_output[item.nodeid]
    
    # METHOD 2: Get from report.capstdout (pytest-html captures this)
    if not captured_logs and hasattr(report, 'capstdout') and report.capstdout:
        captured_logs = report.capstdout
    
    # METHOD 3: Get from report sections
    if not captured_logs and hasattr(report, 'sections'):
        for section_name, section_content in report.sections:
            if 'stdout' in section_name.lower() or 'captured' in section_name.lower():
                captured_logs += section_content + "\n"
    
    # METHOD 4: Get from longreprtext for output on failure
    if not captured_logs and hasattr(report, 'longreprtext') and report.longreprtext:
        captured_logs = report.longreprtext
    
    # Store logs for this test (for external use if needed)
    _test_logs[item.nodeid] = captured_logs
    
    # ============================================
    # BUILD COMPREHENSIVE LOG CONTENT FOR HTML
    # ============================================
    log_lines = []
    log_lines.append("=" * 70)
    log_lines.append(f"📋 TEST: {test_name}")
    log_lines.append(f"📊 STATUS: {'✅ PASSED' if report.passed else '❌ FAILED' if report.failed else '⏭️ SKIPPED'}")
    log_lines.append(f"⏱️ DURATION: {duration_str}")
    log_lines.append(f"🕐 TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append("=" * 70)
    
    if captured_logs:
        log_lines.append("")
        log_lines.append("─" * 70)
        log_lines.append("📝 CAPTURED OUTPUT / TEST EXECUTION LOG:")
        log_lines.append("─" * 70)
        log_lines.append(captured_logs)
    else:
        log_lines.append("")
        log_lines.append("─" * 70)
        log_lines.append("⚠️ NO LOGS CAPTURED")
        log_lines.append("─" * 70)
        log_lines.append("Tips to capture logs:")
        log_lines.append("  • Use print(..., flush=True) in your test modules")
        log_lines.append("  • Run pytest with -s flag: pytest -s test_file.py")
        log_lines.append("  • Check that log_action() is being called correctly")
    
    if report.failed and report.longrepr:
        log_lines.append("")
        log_lines.append("─" * 70)
        log_lines.append("❌ ERROR DETAILS:")
        log_lines.append("─" * 70)
        log_lines.append(str(report.longrepr))
    
    all_logs = '\n'.join(log_lines)
    
    # ============================================
    # TAKE SCREENSHOT
    # ============================================
    driver_instance = item.funcargs.get("driver")
    screenshot_base64 = ""
    
    if driver_instance:
        try:
            result_folder = "passed" if report.outcome == "passed" else "failed"
            screenshot_dir = os.path.join(os.getcwd(), "screenshots", result_folder)
            os.makedirs(screenshot_dir, exist_ok=True)
            
            # Sanitize test name for filename
            safe_test_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in test_name)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_path = os.path.join(screenshot_dir, f"{safe_test_name}_{timestamp}.png")
            driver_instance.save_screenshot(screenshot_path)
            
            with open(screenshot_path, "rb") as f:
                screenshot_base64 = base64.b64encode(f.read()).decode()
        except Exception as e:
            print(f"⚠️ Screenshot capture failed: {e}")
    
    # ============================================
    # ESCAPE HTML & APPLY SYNTAX HIGHLIGHTING
    # ============================================
    import html as html_module
    import re
    
    escaped_logs = html_module.escape(all_logs)
    
    # Apply color-coded syntax highlighting
    highlighted_logs = escaped_logs
    
    # Highlight PASSED in green
    highlighted_logs = re.sub(
        r'(- PASSED|✅ PASSED|\[PASSED\])',
        r'<span style="color:#28a745;font-weight:bold;">\1</span>',
        highlighted_logs
    )
    
    # Highlight FAILED in red
    highlighted_logs = re.sub(
        r'(- FAILED|❌ FAILED|\[FAILED\]|\[ERROR\])',
        r'<span style="color:#dc3545;font-weight:bold;">\1</span>',
        highlighted_logs
    )
    
    # Highlight INFO in blue
    highlighted_logs = re.sub(
        r'(\[INFO\])',
        r'<span style="color:#17a2b8;font-weight:bold;">\1</span>',
        highlighted_logs
    )
    
    # Highlight WARNING in yellow/orange
    highlighted_logs = re.sub(
        r'(\[WARNING\]|\[WARN\]|⚠️)',
        r'<span style="color:#ffc107;font-weight:bold;">\1</span>',
        highlighted_logs
    )
    
    # Highlight timestamps in gray
    highlighted_logs = re.sub(
        r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]',
        r'<span style="color:#6c757d;">[\1]</span>',
        highlighted_logs
    )
    
    # Highlight TEST headers in blue
    highlighted_logs = re.sub(
        r'(TEST \d+:.*)',
        r'<span style="color:#007bff;font-weight:bold;">\1</span>',
        highlighted_logs
    )
    
    # Highlight Screenshot lines in purple
    highlighted_logs = re.sub(
        r'(Screenshot.*|📸.*)',
        r'<span style="color:#6f42c1;">\1</span>',
        highlighted_logs
    )
    
    # Highlight section separators
    highlighted_logs = highlighted_logs.replace(
        '=' * 70, 
        '<span style="color:#5B8DEF;">' + '=' * 70 + '</span>'
    )
    highlighted_logs = highlighted_logs.replace(
        '─' * 70, 
        '<span style="color:#adb5bd;">' + '─' * 70 + '</span>'
    )
    
    # ============================================
    # CREATE HTML CONTENT WITH STYLING
    # ============================================
    status_color = "#28a745" if report.passed else "#dc3545" if report.failed else "#ffc107"
    status_text = "✅ PASSED" if report.passed else "❌ FAILED" if report.failed else "⏭️ SKIPPED"
    status_bg = "#d4edda" if report.passed else "#f8d7da" if report.failed else "#fff3cd"
    
    # Count log lines for display
    log_line_count = len(captured_logs.splitlines()) if captured_logs else 0
    
    html_content = f'''
    <div style="margin:15px 0; border:1px solid #dee2e6; border-radius:8px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
        <!-- Header with status -->
        <div style="background:{status_bg}; padding:12px 20px; border-bottom:1px solid #dee2e6; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="font-size:18px; font-weight:bold; color:{status_color};">{status_text}</span>
                <span style="margin-left:15px; color:#6c757d;">Duration: {duration_str}</span>
            </div>
            <div style="color:#6c757d; font-size:12px;">
                {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
        
        <!-- Content area -->
        <div style="display:flex; gap:0;">
            <!-- Logs section -->
            <div style="flex:1; min-width:0; border-right:1px solid #dee2e6;">
                <div style="background:#343a40; padding:8px 15px; color:#adb5bd; font-family:monospace; font-size:11px;">
                    📝 Test Execution Log ({log_line_count} lines captured)
                </div>
                <pre style="margin:0; padding:15px; font-family:'Consolas','Monaco','Courier New',monospace; font-size:12px; 
                            line-height:1.5; max-height:600px; overflow-y:auto; background:#1e1e1e; color:#d4d4d4;
                            white-space:pre-wrap; word-wrap:break-word;">{highlighted_logs}</pre>
            </div>
    '''
    
    if screenshot_base64:
        html_content += f'''
            <!-- Screenshot section -->
            <div style="flex:0 0 450px; background:#f8f9fa;">
                <div style="background:#343a40; padding:8px 15px; color:#adb5bd; font-family:monospace; font-size:11px;">
                    📸 Screenshot
                </div>
                <div style="padding:10px;">
                    <img src="data:image/png;base64,{screenshot_base64}" 
                         style="width:100%; height:auto; display:block; border:1px solid #dee2e6; border-radius:4px;"/>
                    <div style="text-align:center; padding:8px; color:#6c757d; font-size:11px;">
                        {test_name}
                    </div>
                </div>
            </div>
        '''
    
    html_content += '''
        </div>
    </div>
    '''
    
    report.extras.append(extras.html(html_content))