# SCD WEB TEST SUITE with pytest framework and Allure report generation
# test_scd_web.py
# Based on Admin.py automation structure

import os
import sys
import time
import pytest
import traceback
from datetime import datetime
from typing import Optional

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

# Path configuration
from path_config import LOGIN_PATHS

# Login and Navigation
from Login.Login import login_class_c, login_admin, login_s2
from Branch.Branch_Terminal import branch_selection
from Logout.Logout import Logout

# Utility Files
from Utility import log_action, clear_terminal, clear_folder, log_error

# === SCD Web Modules ===
# Main Dashboard
from Omnipay_Business.Main_Dashboard.Dashboard import Main_Dashboard

# Seller Center
from Omnipay_Business.Seller_Center.Seller_Dashboard.SDashboard import SDashboard
from Omnipay_Business.Seller_Center.Create_Order.COrder_View import COrderview
from Omnipay_Business.Seller_Center.Order_Management.COrder import COrder
from Omnipay_Business.Seller_Center.Order_Management.MOrder import MOrder
from Omnipay_Business.Seller_Center.Order_Management.OMQR import OMQR
from Omnipay_Business.Seller_Center.Product_Management.CNProduct import CNProduct
from Omnipay_Business.Seller_Center.Product_Management.MProduct import MProduct
from Omnipay_Business.Seller_Center.Product_Management.CNProducts_Bulk import Bulk
from Omnipay_Business.Seller_Center.Inventory_Management.IManagement import Inventory_Management

# Service Center
from Omnipay_Business.Service_Center.Booking_Appointments.Booking import SCDBookings
from Omnipay_Business.Service_Center.Create_Service_Order.CSOrder_View import CSOrder_View
from Omnipay_Business.Service_Center.Service_Order_Management.MSOrder import MSOrder
from Omnipay_Business.Service_Center.Service_Order_Management.CSOrder import CSOrder
from Omnipay_Business.Service_Center.Service_Management.CNService import CNService
from Omnipay_Business.Service_Center.Service_Management.MService import MService
from Omnipay_Business.Service_Center.Service_Management.CService_Bulk import CService_Bulk

# Business Hub
from Omnipay_Business.Business_Hub.Cash_Management.Cash_management import CashManagement
from Omnipay_Business.Business_Hub.Shop_Management.Branch import Branches
from Omnipay_Business.Business_Hub.Shop_Management.WHouse import WHouse
from Omnipay_Business.Business_Hub.Employee_Management.AEmployee import NEmployee
from Omnipay_Business.Business_Hub.Employee_Management.EList import EList
from Omnipay_Business.Business_Hub.Client_Directory.ANClient import ANClient
from Omnipay_Business.Business_Hub.Client_Directory.CList import CList

# Send Money
from Omnipay_Business.Send_Money.OmniPayAcc import OmniPayAcc
from Omnipay_Business.Send_Money.AnotherBank import AnotherBank
from Omnipay_Business.Send_Money.MultipleAcc import MultipleAcc
from Omnipay_Business.Send_Money.TelegraphicTransfer import TelegraphicTransfer
from Omnipay_Business.Send_Money.PayBills import PayBills

# Profile and Audit
from Omnipay_Business.My_Profile.Profile import Profile
from Omnipay_Business.Audit.AuditLogs import AuditLogs
from Omnipay_Business.QR.QR import QR

# ==========================================
#           VERSION INFORMATION
# ==========================================
VERSION = "1.2.2.R0001B"
BUILD_DATE = "2026-1-22"

# ==========================================
#           CONFIGURATION SECTION
# ==========================================
class TestConfig:
    """Test configuration settings"""
    # Environment configuration
    BASE_URL = "http://vm-app-dev01:9001/"
    LOGIN_TYPE = "s1"  # Options: "admin", "s1", "s2"
    
    # Tester configuration
    TESTER_NAME = "Christian"
    BROWSER = "Chrome"
    
    # Monitor configuration
    USE_SECOND_MONITOR = True
    MONITOR_OFFSET = 1920
    
    # Timeout settings
    DEFAULT_WAIT = 15
    PAGE_LOAD_TIMEOUT = 30
    
    # Paths
    SCREENSHOTS_DIR = None
    REPORTS_DIR = None
    LOG_FILE_PATH = None


# ==========================================
#           HELPER FUNCTIONS
# ==========================================

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


def setup_directories() -> tuple:
    """Setup log and screenshot directories"""
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(current_file_dir, "Reports")
    screenshots_dir = os.path.join(current_file_dir, "Screenshots")
    
    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(screenshots_dir, exist_ok=True)
    clear_folder(screenshots_dir)
    
    log_filename = f"test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    log_file_path = os.path.join(reports_dir, log_filename)
    
    return reports_dir, screenshots_dir, log_file_path


# ==========================================
#           PYTEST FIXTURES
# ==========================================

@pytest.fixture(scope="session")
def test_config():
    """Provide test configuration"""
    config = TestConfig()
    config.REPORTS_DIR, config.SCREENSHOTS_DIR, config.LOG_FILE_PATH = setup_directories()
    return config


@pytest.fixture(scope="session")
def log_file_path(test_config):
    """Provide log file path"""
    return test_config.LOG_FILE_PATH


@pytest.fixture(scope="session")
def screenshots_dir(test_config):
    """Provide screenshots directory"""
    return test_config.SCREENSHOTS_DIR


@pytest.fixture(scope="session")
def driver(test_config):
    """Setup and teardown Chrome WebDriver with advanced configuration"""
    clear_terminal()
    print_header(test_config)
    
    driver = None
    service_pid = None
    browser_pids = []
    
    try:
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
        try:
            service_pid = service.process.pid
            service_proc = psutil.Process(service_pid)
            browser_pids = [service_proc.pid] + [c.pid for c in service_proc.children(recursive=True)]
            print(f"📌 Tracking {len(browser_pids)} browser process(es) for cleanup")
        except Exception:
            pass
        
        # Get browser version
        browser_version = driver.capabilities.get('browserVersion', 'Unknown')
        print(f"✅ {test_config.BROWSER} v{browser_version} initialized")
        
        # Multi-monitor support
        if test_config.USE_SECOND_MONITOR:
            try:
                monitors = screeninfo.get_monitors()
                if len(monitors) >= 2:
                    m = monitors[1]
                    print(f"🖥️  Moving browser to second monitor: {m.name} ({m.width}x{m.height})")
                    driver.set_window_size(m.width, m.height)
                    driver.set_window_position(m.x, m.y)
                else:
                    print(f"⚠️ Only one monitor detected, using offset method")
                    driver.set_window_position(test_config.MONITOR_OFFSET, 0)
                driver.maximize_window()
            except Exception as e:
                print(f"⚠️ Monitor detection failed: {e}")
                try:
                    driver.set_window_position(test_config.MONITOR_OFFSET, 0)
                    driver.maximize_window()
                except Exception:
                    pass
        else:
            driver.maximize_window()
        
        # Navigate to base URL
        print(f"🌐 Navigating to: {test_config.BASE_URL}")
        driver.get(test_config.BASE_URL)
        
        # Set page zoom to 75%
        driver.execute_script("document.body.style.zoom='75%'")
        
        log_action(
            f"Setup completed - Version: {VERSION}, Browser: {test_config.BROWSER} v{browser_version}, Tester: {test_config.TESTER_NAME}",
            log_file_path=test_config.LOG_FILE_PATH
        )
        print("✅ Setup completed successfully\n")
        
        yield driver
        
    finally:
        # Cleanup
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
        
        if test_config.LOG_FILE_PATH:
            log_action("Browser closed and session ended", log_file_path=test_config.LOG_FILE_PATH)


@pytest.fixture(scope="session")
def wait(driver, test_config):
    """Provide WebDriverWait instance"""
    return WebDriverWait(driver, test_config.DEFAULT_WAIT)


# ==========================================
#           TEST CASES
# ==========================================

# ---- Login Test ----
@pytest.mark.order(1)
@allure.feature("Authentication")
@allure.story("Login")
@allure.title("Login as Class C User")
def test_login(driver, wait, log_file_path, screenshots_dir, test_config):
    """Test login functionality"""
    print("\n" + "-" * 70)
    print("🔐 LOGIN PHASE".center(70))
    print("-" * 70)
    
    with allure.step("Logging in as Class C user"):
        log_action("Starting login test...", log_file_path=log_file_path)
        
        try:
            capture_screenshot(driver, "login_page", screenshots_dir)
            
            # Map login types to configurations
            login_map = {
                "admin": {"key": "Admin", "func": login_admin},
                "s1": {"key": "Class_C", "func": login_class_c},
                "s2": {"key": "S2", "func": login_s2},
            }
            
            login_type = test_config.LOGIN_TYPE
            if login_type not in login_map:
                raise ValueError(f"Invalid login type: {login_type}")
            
            config_key = login_map[login_type]["key"]
            login_func = login_map[login_type]["func"]
            
            cfg = LOGIN_PATHS.get(config_key)
            if not cfg:
                raise ValueError(f"LOGIN_PATHS missing key '{config_key}'")
            
            excel_path = cfg.get('excel_path')
            if not excel_path:
                raise ValueError(f"No excel_path configured for login type: {login_type}")
            
            username, password = login_func(driver, excel_path)
            
            log_action(f"Login successful with {login_type}", log_file_path=log_file_path)
            print(f"✅ Login successful as: {username}\n")
            
            capture_screenshot(driver, "login_success", screenshots_dir)
            
        except Exception as e:
            log_error(f"Login failed: {str(e)}", log_file_path=log_file_path)
            capture_screenshot(driver, "login_failed", screenshots_dir)
            allure.attach(traceback.format_exc(), name="Login Error", attachment_type=AttachmentType.TEXT)
            print(f"❌ Login failed: {str(e)}")
            pytest.fail(f"Login failed: {str(e)}")


# ---- Branch Selection Test ----
@pytest.mark.order(2)
@allure.feature("Navigation")
@allure.story("Branch Selection")
@allure.title("Select Branch and Terminal")
def test_branch_selection(driver, wait, log_file_path, screenshots_dir):
    """Test branch and terminal selection"""
    print("\n" + "-" * 70)
    print("🏢 BRANCH SELECTION PHASE".center(70))
    print("-" * 70)
    
    with allure.step("Selecting branch and terminal"):
        log_action("Starting branch selection...", log_file_path=log_file_path)
        
        try:
            branch_selection(driver, wait, log_file_path)
            time.sleep(3)
            
            log_action("Branch selection completed", log_file_path=log_file_path)
            print("✅ Branch selection completed\n")
            
            capture_screenshot(driver, "branch_selected", screenshots_dir)
            
        except Exception as e:
            log_error(f"Branch selection failed: {str(e)}", log_file_path=log_file_path)
            capture_screenshot(driver, "branch_selection_failed", screenshots_dir)
            allure.attach(traceback.format_exc(), name="Branch Selection Error", attachment_type=AttachmentType.TEXT)
            print(f"❌ Branch selection failed: {str(e)}")
            pytest.fail(f"Branch selection failed: {str(e)}")


# ---- Main Dashboard Test ----
@pytest.mark.order(3)
@allure.feature("Main Dashboard")
@allure.story("Dashboard View")
@allure.title("Main Dashboard Module")
def test_main_dashboard(driver, wait, log_file_path, screenshots_dir):
    """Test Main Dashboard module"""
    print("\n" + "-" * 70)
    print("📊 MAIN DASHBOARD MODULE".center(70))
    print("-" * 70)
    
    with allure.step("Testing Main Dashboard"):
        log_action("Starting Main Dashboard test...", log_file_path=log_file_path)
        
        try:
            start_time = time.time()
            Main_Dashboard(driver, wait)
            elapsed_time = time.time() - start_time
            
            log_action(f"Main Dashboard - PASSED (Duration: {elapsed_time:.2f}s)", log_file_path=log_file_path)
            print(f"✅ Main Dashboard - PASSED (Duration: {elapsed_time:.2f}s)")
            
            capture_screenshot(driver, "main_dashboard_completed", screenshots_dir)
            
        except Exception as e:
            log_error(f"Main Dashboard failed: {str(e)}", log_file_path=log_file_path)
            capture_screenshot(driver, "main_dashboard_failed", screenshots_dir)
            allure.attach(traceback.format_exc(), name="Main Dashboard Error", attachment_type=AttachmentType.TEXT)
            print(f"❌ Main Dashboard failed: {str(e)}")
            pytest.fail(f"Main Dashboard failed: {str(e)}")


# ---- Seller Center Tests ----
@pytest.mark.order(4)
@allure.feature("Seller Center")
@allure.story("Seller Dashboard")
@allure.title("Seller Dashboard Module")
def test_seller_dashboard(driver, wait, log_file_path, screenshots_dir):
    """Test Seller Dashboard module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Seller Dashboard", SDashboard)


@pytest.mark.order(5)
@allure.feature("Seller Center")
@allure.story("Create Order")
@allure.title("Create Order View Only Module")
def test_create_order_view(driver, wait, log_file_path, screenshots_dir):
    """Test Create Order View Only module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Create Order View Only", COrderview)


@pytest.mark.order(6)
@allure.feature("Seller Center")
@allure.story("Order Management")
@allure.title("Create Single Order Module")
def test_create_order(driver, wait, log_file_path, screenshots_dir):
    """Test Create Single Order module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Create Single Order", COrder)


@pytest.mark.order(7)
@allure.feature("Seller Center")
@allure.story("Order Management")
@allure.title("Manage Order Module")
def test_manage_order(driver, wait, log_file_path, screenshots_dir):
    """Test Manage Order module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Manage Order", MOrder)


@pytest.mark.order(8)
@allure.feature("Seller Center")
@allure.story("Order Management")
@allure.title("Generate QR Module")
def test_order_qr(driver, wait, log_file_path, screenshots_dir):
    """Test Generate QR module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Generate QR", OMQR)


# ---- Product Management Tests ----
@pytest.mark.order(9)
@allure.feature("Seller Center")
@allure.story("Product Management")
@allure.title("Create New Product Module")
def test_create_product(driver, wait, log_file_path, screenshots_dir):
    """Test Create New Product module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Create New Product", CNProduct)


@pytest.mark.order(10)
@allure.feature("Seller Center")
@allure.story("Product Management")
@allure.title("Manage Product Module")
def test_manage_product(driver, wait, log_file_path, screenshots_dir):
    """Test Manage Product module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Manage Product", MProduct)


@pytest.mark.order(11)
@allure.feature("Seller Center")
@allure.story("Product Management")
@allure.title("Create New Product Bulk Module")
def test_create_product_bulk(driver, wait, log_file_path, screenshots_dir):
    """Test Create New Product Bulk module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Create New Product - Bulk", Bulk)


# ---- Inventory Management Test ----
@pytest.mark.order(12)
@allure.feature("Seller Center")
@allure.story("Inventory Management")
@allure.title("Inventory Management Module")
def test_inventory_management(driver, wait, log_file_path, screenshots_dir):
    """Test Inventory Management module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Inventory Management", Inventory_Management)


# ---- Service Center Tests ----
@pytest.mark.order(13)
@allure.feature("Service Center")
@allure.story("Booking and Appointments")
@allure.title("Booking and Appointments Module")
def test_bookings(driver, wait, log_file_path, screenshots_dir):
    """Test Booking and Appointments module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Booking and Appointments", SCDBookings)


@pytest.mark.order(14)
@allure.feature("Service Center")
@allure.story("Service Order")
@allure.title("Create Service Order Module")
def test_create_service_order(driver, wait, log_file_path, screenshots_dir):
    """Test Create Service Order module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Create Service Order", CSOrder_View)


@pytest.mark.order(15)
@allure.feature("Service Center")
@allure.story("Service Order")
@allure.title("Create Service Order View Only Module")
def test_create_service_order_view(driver, wait, log_file_path, screenshots_dir):
    """Test Create Service Order View Only module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Create Service Order View Only", CSOrder)


@pytest.mark.order(16)
@allure.feature("Service Center")
@allure.story("Service Order Management")
@allure.title("Manage Service Order Module")
def test_manage_service_order(driver, wait, log_file_path, screenshots_dir):
    """Test Manage Service Order module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Manage Service Order", MSOrder)


# ---- Service Management Tests ----
@pytest.mark.order(17)
@allure.feature("Service Center")
@allure.story("Service Management")
@allure.title("Create New Service Module")
def test_create_service(driver, wait, log_file_path, screenshots_dir):
    """Test Create New Service module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Create New Service", CNService)


@pytest.mark.order(18)
@allure.feature("Service Center")
@allure.story("Service Management")
@allure.title("Manage Service Module")
def test_manage_service(driver, wait, log_file_path, screenshots_dir):
    """Test Manage Service module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Manage Service", MService)


@pytest.mark.order(19)
@allure.feature("Service Center")
@allure.story("Service Management")
@allure.title("Create Service Bulk Module")
def test_create_service_bulk(driver, wait, log_file_path, screenshots_dir):
    """Test Create Service Bulk module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Create Service Bulk", CService_Bulk)


# ---- Business Hub Tests ----
@pytest.mark.order(20)
@allure.feature("Business Hub")
@allure.story("Cash Management")
@allure.title("Cash Management Module")
def test_cash_management(driver, wait, log_file_path, screenshots_dir):
    """Test Cash Management module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Cash Management", CashManagement)


@pytest.mark.order(21)
@allure.feature("Business Hub")
@allure.story("Shop Management")
@allure.title("Branches Module")
def test_branches(driver, wait, log_file_path, screenshots_dir):
    """Test Branches module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Branches", Branches)


@pytest.mark.order(22)
@allure.feature("Business Hub")
@allure.story("Shop Management")
@allure.title("Warehouse Module")
def test_warehouse(driver, wait, log_file_path, screenshots_dir):
    """Test Warehouse module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Warehouse", WHouse)


@pytest.mark.order(23)
@allure.feature("Business Hub")
@allure.story("Employee Management")
@allure.title("Add New Employee Module")
def test_add_employee(driver, wait, log_file_path, screenshots_dir):
    """Test Add New Employee module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Add New Employee", NEmployee)


@pytest.mark.order(24)
@allure.feature("Business Hub")
@allure.story("Employee Management")
@allure.title("Employee List Module")
def test_employee_list(driver, wait, log_file_path, screenshots_dir):
    """Test Employee List module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Employee List", EList)


@pytest.mark.order(25)
@allure.feature("Business Hub")
@allure.story("Client Directory")
@allure.title("Add New Client Module")
def test_add_client(driver, wait, log_file_path, screenshots_dir):
    """Test Add New Client module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Add New Client", ANClient)


@pytest.mark.order(26)
@allure.feature("Business Hub")
@allure.story("Client Directory")
@allure.title("Client List Module")
def test_client_list(driver, wait, log_file_path, screenshots_dir):
    """Test Client List module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Client List", CList)


# ---- Send Money Tests ----
# @pytest.mark.order(27)
# @allure.feature("Send Money")
# @allure.story("Transfer")
# @allure.title("To Another OmniPay Account Module")
# def test_send_omnipay(driver, wait, log_file_path, screenshots_dir):
#     """Test Send to OmniPay Account module"""
#     _run_module_test(driver, wait, log_file_path, screenshots_dir, "To Another OmniPay Account", OmniPayAcc)


@pytest.mark.order(27)
@allure.feature("Send Money")
@allure.story("Transfer")
@allure.title("To Another Bank Module")
def test_send_another_bank(driver, wait, log_file_path, screenshots_dir):
    """Test Send to Another Bank module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "To Another Bank", AnotherBank)


# @pytest.mark.order(29)
# @allure.feature("Send Money")
# @allure.story("Transfer")
# @allure.title("To Multiple Accounts Module")
# def test_send_multiple(driver, wait, log_file_path, screenshots_dir):
#     """Test Send to Multiple Accounts module"""
#     _run_module_test(driver, wait, log_file_path, screenshots_dir, "To Multiple Accounts", MultipleAcc)


# @pytest.mark.order(29)
# @allure.feature("Send Money")
# @allure.story("Transfer")
# @allure.title("Request Telegraphic Transfer Module")
# def test_telegraphic_transfer(driver, wait, log_file_path, screenshots_dir):
#     """Test Telegraphic Transfer module"""
#     _run_module_test(driver, wait, log_file_path, screenshots_dir, "Request Telegraphic Transfer", TelegraphicTransfer)


# @pytest.mark.order(31)
# @allure.feature("Send Money")
# @allure.story("Bills Payment")
# @allure.title("Pay Bills Module")
# def test_pay_bills(driver, wait, log_file_path, screenshots_dir):
#     """Test Pay Bills module"""
#     _run_module_test(driver, wait, log_file_path, screenshots_dir, "Pay Bills", PayBills)


# ---- Profile Test ----
@pytest.mark.order(28)
@allure.feature("Profile")
@allure.story("User Profile")
@allure.title("My Profile Module")
def test_profile(driver, wait, log_file_path, screenshots_dir):
    """Test My Profile module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "My Profile", Profile)


# ---- Audit Logs Test ----
@pytest.mark.order(29)
@allure.feature("Audit")
@allure.story("Audit Logs")
@allure.title("Audit Logs Module")
def test_audit_logs(driver, wait, log_file_path, screenshots_dir):
    """Test Audit Logs module"""
    _run_module_test(driver, wait, log_file_path, screenshots_dir, "Audit Logs", AuditLogs)


# ---- Logout Test ----
@pytest.mark.order(30)
@allure.feature("Authentication")
@allure.story("Logout")
@allure.title("Logout")
def test_logout(driver, wait, log_file_path, screenshots_dir):
    """Test logout functionality"""
    print("\n" + "-" * 70)
    print("🚪 LOGOUT PHASE".center(70))
    print("-" * 70)
    
    with allure.step("Logging out"):
        log_action("Starting logout...", log_file_path=log_file_path)
        
        try:
            Logout(driver, wait)
            time.sleep(3)
            
            log_action("Logout completed", log_file_path=log_file_path)
            print("✅ Logout completed\n")
            
            capture_screenshot(driver, "logout_success", screenshots_dir)
            
        except Exception as e:
            log_error(f"Logout failed: {str(e)}", log_file_path=log_file_path)
            capture_screenshot(driver, "logout_failed", screenshots_dir)
            allure.attach(traceback.format_exc(), name="Logout Error", attachment_type=AttachmentType.TEXT)
            print(f"❌ Logout failed: {str(e)}")
            pytest.fail(f"Logout failed: {str(e)}")


# ==========================================
#           HELPER TEST FUNCTION
# ==========================================

def _run_module_test(driver, wait, log_file_path, screenshots_dir, module_name: str, module_func):
    """Generic helper function to run module tests"""
    print(f"\n🔹 Testing: {module_name}")
    print("-" * 50)
    
    with allure.step(f"Testing {module_name}"):
        log_action(f"Starting {module_name} test...", log_file_path=log_file_path)
        
        try:
            start_time = time.time()
            module_func(driver, wait)
            
            # Wait for page to fully load
            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            elapsed_time = time.time() - start_time
            
            log_action(f"{module_name} - PASSED (Duration: {elapsed_time:.2f}s)", log_file_path=log_file_path)
            print(f"✅ {module_name} - PASSED (Duration: {elapsed_time:.2f}s)")
            
            capture_screenshot(driver, f"{module_name.lower().replace(' ', '_').replace('-', '_')}_completed", screenshots_dir)
            
        except Exception as e:
            log_error(f"{module_name} failed: {str(e)}", log_file_path=log_file_path)
            capture_screenshot(driver, f"{module_name.lower().replace(' ', '_').replace('-', '_')}_failed", screenshots_dir)
            allure.attach(traceback.format_exc(), name=f"{module_name} Error", attachment_type=AttachmentType.TEXT)
            print(f"❌ {module_name} - FAILED")
            print(f"   Error: {str(e)}")
            pytest.fail(f"{module_name} failed: {str(e)}")


# ==========================================
#           PYTEST HOOKS
# ==========================================

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "order: mark test to run in a specific order")


def pytest_sessionstart(session):
    """Called after the Session object has been created"""
    print("\n" + "=" * 80)
    print("STARTING TEST SESSION")
    print("=" * 80 + "\n")


def pytest_sessionfinish(session, exitstatus):
    """Generate summary after all tests complete"""
    print("\n" + "=" * 80)
    print("📊 TEST EXECUTION SUMMARY".center(80))
    print(f"Version {VERSION}".center(80))
    print("=" * 80)
    print(f"\n  📅 End Time     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  🏁 Exit Status  : {exitstatus}")
    
    # Get test results from session
    passed = session.testscollected - session.testsfailed - getattr(session, 'testsskipped', 0)
    failed = session.testsfailed
    total = session.testscollected
    
    print(f"\n  📈 Total Tests  : {total}")
    print(f"  ✅ Passed       : {passed} ({(passed/total*100) if total > 0 else 0:.1f}%)")
    print(f"  ❌ Failed       : {failed} ({(failed/total*100) if total > 0 else 0:.1f}%)")
    
    print("\n" + "=" * 80)
    print("ALL TESTS COMPLETED")
    print("=" * 80 + "\n")


# ==========================================
#           MAIN ENTRY POINT
# ==========================================

if __name__ == "__main__":
    # Run pytest with Allure reporting
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        f"--alluredir=./allure-results",
        "-p", "no:warnings"
    ])