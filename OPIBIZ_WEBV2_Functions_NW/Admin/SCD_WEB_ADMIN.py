import traceback
import sys
import os
import time
from datetime import datetime
from typing import Tuple, Optional

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait

# Process and monitor management
import psutil
import screeninfo


# Add paths to custom modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'OPIBIZ_WEBV2_Functions_NW')))

# Path configuration
from path_config import LOGIN_PATHS

# Login
from Login.Login import login_class_c, login_admin, login_s2
from Branch.Branch_Terminal import branch_selection
from Logout.Logout import Logout

# Utility Files 
from Utility import log_action, clear_terminal, clear_folder, log_error


#---- SCD Web Modules ----#
# Import all modules
from Omnipay_Business.Main_Dashboard.Dashboard import Main_Dashboard
from Omnipay_Business.Seller_Center.Seller_Dashboard.SDashboard import SDashboard
from Omnipay_Business.Seller_Center.Create_Order.COrder_View import COrderview
from Omnipay_Business.Seller_Center.Order_Management.COrder import COrder
from Omnipay_Business.Seller_Center.Order_Management.MOrder import MOrder
from Omnipay_Business.Seller_Center.Order_Management.OMQR import OMQR
from Omnipay_Business.Seller_Center.Product_Management.CNProduct import CNProduct
from Omnipay_Business.Seller_Center.Product_Management.MProduct import MProduct
from Omnipay_Business.Seller_Center.Product_Management.CNProducts_Bulk import Bulk
from Omnipay_Business.Seller_Center.Inventory_Management.IManagement import Inventory_Management
from Omnipay_Business.Service_Center.Booking_Appointments.Booking import SCDBookings
from Omnipay_Business.Service_Center.Booking_Appointments.Booking_Bulk import SCDBooking_Bulk
from Omnipay_Business.Service_Center.Create_Service_Order.CSOrder_View import CSOrder_View 
from Omnipay_Business.Service_Center.Service_Order_Management.MSOrder import MSOrder
from Omnipay_Business.Service_Center.Service_Order_Management.CSOrder import CSOrder
from Omnipay_Business.Service_Center.Service_Management.CNService import CNService
from Omnipay_Business.Service_Center.Service_Management.MService import MService
from Omnipay_Business.Service_Center.Service_Management.CService_Bulk import CService_Bulk
from Omnipay_Business.Business_Hub.Cash_Management.Cash_management import CashManagement
from Omnipay_Business.Business_Hub.Shop_Management.Branch import Branches
from Omnipay_Business.Business_Hub.Shop_Management.WHouse import WHouse
from Omnipay_Business.Business_Hub.Shop_Management.Bulk_WHouse import Bulk_Whouse
from Omnipay_Business.Business_Hub.Employee_Management.AEmployee import NEmployee
from Omnipay_Business.Business_Hub.Employee_Management.EList import EList
from Omnipay_Business.Business_Hub.Employee_Management.NEmployee_Bulk import Bulk_Employee
from Omnipay_Business.Business_Hub.Client_Directory.ANClient import ANClient
from Omnipay_Business.Business_Hub.Client_Directory.CList import CList
from Omnipay_Business.Business_Hub.Client_Directory.Client_Bulk import Bulk_Client
from Omnipay_Business.Send_Money.OmniPayAcc import OmniPayAcc
from Omnipay_Business.Send_Money.AnotherBank import AnotherBank
from Omnipay_Business.Send_Money.MultipleAcc import MultipleAcc
from Omnipay_Business.Send_Money.TelegraphicTransfer import TelegraphicTransfer
from Omnipay_Business.Send_Money.PayBills import PayBills
from Omnipay_Business.My_Profile.Profile import Profile
from Omnipay_Business.Audit.AuditLogs import AuditLogs
from Omnipay_Business.QR.QR import QR


# ==========================================
#           VERSION INFORMATION
# ==========================================
VERSION = "1.2.2.R0003B"
BUILD_DATE = "2026-2-06"


#---- Main automation class for SCD Web testing ----#
class SCDWebAutomation: 
    def __init__(self, base_url: str = "http://beta-opibizscd.paybps.ovpn/", use_second_monitor: bool = False, monitor_offset: int = 1920, tester_name: str = "QA Tester", browser: str = "Chrome"):
        self.base_url = base_url
        self.driver = None
        self.wait = None
        self.log_file_path = None
        self.screenshots_folder = None
        self.use_second_monitor = use_second_monitor
        self.monitor_offset = monitor_offset  # X offset for second monitor (typically primary monitor width)
        self.tester_name = tester_name
        self.browser = browser
        self.browser_version = None  # Will be set after driver initialization
        self.service_pid = None  # Track ChromeDriver service PID
        self.browser_pids = []  # Track all browser-related PIDs for cleanup
        self.test_results = {
            'passed': [],
            'failed': [],
            'skipped': []
        }

    #---- Print test execution header ----#
    def _print_header(self) -> None:      
        print("=" * 70)
        print("OMNIPAY BUSINESS SCD WEB AUTOMATION".center(70))
        print(f"Version {VERSION}".center(70))
        print("=" * 70)
        print()
        print(f"  📋 Project      : Omnipay SCD Web")
        print(f"  🏷️  Version     : {VERSION} (Build: {BUILD_DATE})")
        print(f"  👤 Tester       : {self.tester_name}")
        print(f"  🌐 Browser      : {self.browser}")
        print(f"  🔗 Environment  : {self.base_url}")
        print(f"  📅 Date         : {datetime.now().strftime('%Y-%m-%d')}")
        print(f"  ⏰ Start Time   : {datetime.now().strftime('%H:%M:%S')}")
        if self.use_second_monitor:
            print(f"  🖥️  Monitor      : Second Monitor (offset: {self.monitor_offset}px)")
        else:
            print(f"  🖥️  Monitor      : Primary Monitor")
        print()
        print("=" * 70)

    #---- Setup the test environment ----#    
    def setup(self) -> bool:
        try:
            clear_terminal()
            self._print_header()
            
            # Setup file paths
            current_file_dir = os.path.dirname(os.path.abspath(__file__))
            self.log_file_path = os.path.join(current_file_dir, '..', '..', 'Files', 'logs', 'Admin', 'Admin.txt')
            self.screenshots_folder = os.path.join(current_file_dir, '..', '..', 'Files', 'screenshots', 'Admin')
            
            # Ensure directories exist
            os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)
            os.makedirs(self.screenshots_folder, exist_ok=True)
            
            # Clear old screenshots
            clear_folder(screenshots_folder=self.screenshots_folder)
            
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
           
            # CRITICAL: Set page load strategy to 'normal' (waits for everything)
            chrome_options.page_load_strategy = 'normal' 

            # --- Disable Chrome save dialogs and autofill ---
            prefs = {
                "credentials_enable_service": False,       # disable password save prompt
                "profile.password_manager_enabled": False,
                "autofill.profile_enabled": False,         # disable address autofill
                "autofill.credit_card_enabled": False,     # disable card autofill
                "autofill.address_enabled": False,
                "autofill.enabled": False,
                "safebrowsing.enabled": False  # Disable download warnings
            }
            chrome_options.add_experimental_option("prefs", prefs)

            # Initialize ChromeDriver
            print("\n🔧 Initializing Chrome WebDriver...")
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Track PIDs for cleanup
            try:
                self.service_pid = service.process.pid
                service_proc = psutil.Process(self.service_pid)
                self.browser_pids = [service_proc.pid] + [c.pid for c in service_proc.children(recursive=True)]
                print(f"📌 Tracking {len(self.browser_pids)} browser process(es) for cleanup")
            except Exception:
                pass
            
            # Get browser version
            self.browser_version = self.driver.capabilities.get('browserVersion', 'Unknown')
            print(f"✅ {self.browser} v{self.browser_version} initialized")
            
            # Setup wait
            self.wait = WebDriverWait(self.driver, 15)
            
            # Multi-monitor support
            if self.use_second_monitor:
                try:
                    monitors = screeninfo.get_monitors()
                    if len(monitors) >= 2:
                        m = monitors[1]  # Get second monitor
                        print(f"🖥️  Moving browser to second monitor: {m.name} ({m.width}x{m.height})")
                        self.driver.set_window_size(m.width, m.height)
                        self.driver.set_window_position(m.x, m.y)
                    else:
                        print(f"⚠️ Only one monitor detected, using offset method")
                        self.driver.set_window_position(self.monitor_offset, 0)
                    self.driver.maximize_window()
                except Exception as e:
                    print(f"⚠️ Monitor detection failed: {e}")
                    try:
                        self.driver.set_window_position(self.monitor_offset, 0)
                        self.driver.maximize_window()
                    except Exception:
                        pass
            else:
                self.driver.maximize_window()
            
            # Navigate to base URL
            print(f"🌐 Navigating to: {self.base_url}")
            self.driver.get(self.base_url)
            
            # Set page zoom to 75%
            self.driver.execute_script("document.body.style.zoom='75%'")
            
            log_action(f"Setup completed - Version: {VERSION}, Browser: {self.browser} v{self.browser_version}, Tester: {self.tester_name}", log_file_path=self.log_file_path)
            print("✅ Setup completed successfully\n")
            return True
            
        except Exception as e:
            print(f"❌ Setup failed: {str(e)}")
            log_error(f"Setup failed: {str(e)}", log_file_path=self.log_file_path)
            traceback.print_exc()
            return False
    
    #---- Capture screenshot for debugging ----#
    def capture_screenshot(self, name: str) -> None:
        try:
            if self.driver and self.screenshots_folder:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{name}_{timestamp}.png"
                filepath = os.path.join(self.screenshots_folder, filename)
                self.driver.save_screenshot(filepath)
                log_action(f"Screenshot saved: {filename}", log_file_path=self.log_file_path)
                print(f"📸 Screenshot saved: {filename}")
        except Exception as e:
            print(f"⚠️ Failed to capture screenshot: {str(e)}")
    
    #---- Perform login based on type ----#
    def login(self, login_type: str = "s1") -> Tuple[Optional[str], Optional[str]]:
        try:
            print("-" * 70)
            print("🔐 LOGIN PHASE".center(70))
            print("-" * 70)

            # Map user-friendly login types to LOGIN_PATHS keys and login functions
            login_map = {
                "admin": {"key": "Admin", "func": login_admin},
                "s1": {"key": "Class_C", "func": login_class_c},
                "s2": {"key": "S2", "func": login_s2},
            }

            if login_type not in login_map:
                raise ValueError(f"Invalid login type: {login_type}. Valid options: {list(login_map.keys())}")

            config_key = login_map[login_type]["key"]
            login_func = login_map[login_type]["func"]

            # Get config using the correct key
            cfg = LOGIN_PATHS.get(config_key)
            if not cfg:
                raise ValueError(f"LOGIN_PATHS missing key '{config_key}' for login type '{login_type}'")

            excel_path = cfg.get('excel_path')
            if not excel_path:
                raise ValueError(f"No excel_path configured for login type: {login_type}")

            # Call the appropriate login function
            username, password = login_func(self.driver, excel_path)

            log_action(f"Login successful with {login_type}", log_file_path=self.log_file_path)
            print(f"✅ Login successful as: {username}\n")
            return username, password

        except Exception as e:
            print(f"❌ Login failed: {str(e)}")
            log_error(f"Login failed: {str(e)}", log_file_path=self.log_file_path)
            self.capture_screenshot("login_failed")
            return None, None

    #---- Select branch/terminal ----#
    def select_branch(self) -> bool:
        try:
            print("-" * 70)
            print("🏢 BRANCH SELECTION PHASE".center(70))
            print("-" * 70)
            
            branch_selection(self.driver, self.wait, self.log_file_path)
            time.sleep(3)
            
            log_action("Branch selection completed", log_file_path=self.log_file_path)
            print("✅ Branch selection completed\n")
            return True
            
        except Exception as e:
            print(f"❌ Branch selection failed: {str(e)}")
            log_error(f"Branch selection failed: {str(e)}", log_file_path=self.log_file_path)
            self.capture_screenshot("branch_selection_failed")
            return False
    
    #---- Execute all Restaurant Center test modules ----#
    def run_scdweb_tests(self) -> dict:
        print("=" * 70)
        print("🚀 SCD WEB TESTING PHASE".center(70))
        print("=" * 70)
        print()
        
        # Define test modules with their functions
        modules = [
                ("Main Dashboard", Main_Dashboard),
                ("Seller Center Dashboard", SDashboard),
                ("Create Order View Only", COrderview),
                ("Create Single Order", COrder),
                ("Manage Order", MOrder),
                ("Generate QR", OMQR),
                ("Create New Product", CNProduct),
                ("Manage Product", MProduct),
                ("Create New Product - Bulk", Bulk),
                ("Inventory Management", Inventory_Management),
                ("Booking and Appointments", SCDBookings),
                ("Bulk Appointment", SCDBooking_Bulk),
                ("Create Service Order View Only", CSOrder_View),
                ("Create Service Order", CSOrder),
                ("Manage Service Order", MSOrder),
                ("Create New Service", CNService),
                ("Manage Service", MService),
                ("Create Service Bulk", CService_Bulk),
                ("Cash Management", CashManagement),
                ("Branches", Branches),
                ("Warehouse", WHouse),
                ("Warehouse-Bulk", Bulk_Whouse),
                ("Added New Employee", NEmployee),
                ("Employee List", EList),
                ("Employee Bulk", Bulk_Employee),
                ("Add New Client", ANClient),
                ("Client List", CList),
                 ("Client Bulk", Bulk_Client),
                # ("To Another OmniPay Account", OmniPayAcc),
                ("To Another Bank", AnotherBank),
                # ("To Multiple Accounts", MultipleAcc),
                # ("Request Telegraphic Transfer", TelegraphicTransfer),
                # ("Pay Bills", PayBills),
                ("My Profile", Profile),
                ("Audit Logs", AuditLogs),
                ("Generate QR",QR),
            ]
        
        total_modules = len(modules)
        
        for index, (name, func) in enumerate(modules, 1):
            try:
                print(f"\n[{index}/{total_modules}] 🔹 Testing: {name}")
                print("-" * 50)
                
                start_time = time.time()
                
                # Execute the module
                func(self.driver, self.wait)
                
                # Wait for page to fully load
                WebDriverWait(self.driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
                elapsed_time = time.time() - start_time
                
                # Log success
                log_action(f"{name} - PASSED (Duration: {elapsed_time:.2f}s)", log_file_path=self.log_file_path)
                self.test_results['passed'].append(name)
                print(f"✅ {name} - PASSED (Duration: {elapsed_time:.2f}s)")
                
            except Exception as e:
                # Log failure
                error_msg = f"{name} - FAILED: {str(e)}"
                log_error(error_msg, log_file_path=self.log_file_path)
                self.test_results['failed'].append(name)
                print(f"❌ {name} - FAILED")
                print(f"   Error: {str(e)}")
                
                # Capture screenshot for debugging
                self.capture_screenshot(f"{name.replace(' ', '_')}_failed")
                
                # Print detailed traceback
                if '--verbose' in sys.argv:
                    traceback.print_exc()
                
                # Continue to next module
                continue
        
        return self.test_results
    
    #---- Perform logout ----#
    def logout(self) -> bool:
        try:
            print("\n" + "-" * 70)
            print("🚪 LOGOUT PHASE".center(70))
            print("-" * 70)
            
            Logout(self.driver, self.wait)
            time.sleep(3)
            
            log_action("Logout completed", log_file_path=self.log_file_path)
            print("✅ Logout completed\n")
            return True
            
        except Exception as e:
            print(f"❌ Logout failed: {str(e)}")
            log_error(f"Logout failed: {str(e)}", log_file_path=self.log_file_path)
            self.capture_screenshot("logout_failed")
            return False
    
    #---- Generate test execution summary report ----#
    def generate_report(self) -> None:
        print("\n" + "=" * 70)
        print("📊 TEST EXECUTION SUMMARY".center(70))
        print(f"Version {VERSION}".center(70))
        print("=" * 70)
        
        # Test execution info
        print(f"\n  🏷️  Version   : {VERSION}")
        print(f"  👤 Tester       : {self.tester_name}")
        print(f"  🌐 Browser      : {self.browser} v{self.browser_version}")
        print(f"  🔗 Environment  : {self.base_url}")
        print(f"  📅 End Time     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        total_tests = len(self.test_results['passed']) + len(self.test_results['failed']) + len(self.test_results['skipped'])
        passed = len(self.test_results['passed'])
        failed = len(self.test_results['failed'])
        skipped = len(self.test_results['skipped'])
        
        print(f"  📈 Total Tests  : {total_tests}")
        print(f"  ✅ Passed       : {passed} ({(passed/total_tests*100) if total_tests > 0 else 0:.1f}%)")
        print(f"  ❌ Failed       : {failed} ({(failed/total_tests*100) if total_tests > 0 else 0:.1f}%)")
        print(f"  ⏭️  Skipped      : {skipped} ({(skipped/total_tests*100) if total_tests > 0 else 0:.1f}%)")
        
        if self.test_results['passed']:
            print("\n  ✅ Passed Tests:")
            for test in self.test_results['passed']:
                print(f"     • {test}")
        
        if self.test_results['failed']:
            print("\n  ❌ Failed Tests:")
            for test in self.test_results['failed']:
                print(f"     • {test}")
        
        if self.test_results['skipped']:
            print("\n  ⏭️  Skipped Tests:")
            for test in self.test_results['skipped']:
                print(f"     • {test}")
        
        print("\n" + "=" * 70)
        
        # Log the summary
        summary = f"Test Summary - Tester: {self.tester_name}, Browser: {self.browser} v{self.browser_version}, Total: {total_tests}, Passed: {passed}, Failed: {failed}, Skipped: {skipped}"
        log_action(summary, log_file_path=self.log_file_path)
    
    #---- Clean up resources ----#
    def cleanup(self) -> None:
        try:
            print("\n🧹 Cleaning up...")
            time.sleep(3)
            
            # First try to quit driver gracefully
            if self.driver:
                try:
                    self.driver.quit()
                    print("✅ Browser closed successfully")
                except Exception as e:
                    print(f"⚠️ Driver quit warning: {str(e)}")
            
            # Force kill any remaining browser processes using tracked PIDs
            if self.browser_pids:
                killed_count = 0
                for pid in self.browser_pids:
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
            
            if self.log_file_path:
                log_action("Browser closed and session ended", log_file_path=self.log_file_path)
            
        except Exception as e:
            print(f"⚠️ Cleanup warning: {str(e)}")
    
    #---- Main execution flow ----#
    def run(self, login_type: str = "s1") -> bool:
        try:
            start_time = time.time()
            
            # Setup
            if not self.setup():
                return False
            
            # Login
            username, password = self.login(login_type)
            if not username:
                return False
            
            # Branch Selection
            if not self.select_branch():
                return False
            
            # Run Restaurant Center Tests
            self.run_scdweb_tests()
            
            # Logout
            self.logout()
            
            # Generate Report
            self.generate_report()
            
            # Calculate total execution time
            total_time = time.time() - start_time
            minutes, seconds = divmod(total_time, 60)
            
            print(f"\n⏱️  Total Execution Time: {int(minutes)}m {int(seconds)}s")
            log_action(f"All automation completed in {int(minutes)}m {int(seconds)}s", log_file_path=self.log_file_path)
            
            return True
            
        except KeyboardInterrupt:
            print("\n\n⚠️ Automation interrupted by user")
            if self.log_file_path:
                log_action("Automation interrupted by user", log_file_path=self.log_file_path)
            return False
            
        except Exception as e:
            print(f"\n❌ Critical error in automation: {str(e)}")
            if self.log_file_path:
                log_error(f"Critical error: {str(e)}", log_file_path=self.log_file_path)
            traceback.print_exc()
            return False
            
        finally:
            self.cleanup()


#---- Entry point for the automation script ----#
def main():
    # ==========================================
    #           CONFIGURATION SECTION
    # ==========================================
    
    # Environment configuration
    BASE_URL = "http://beta-opibizscd.paybps.ovpn/ "
    LOGIN_TYPE = "s1"  # Options: "admin", "s1", "s2"
    
    # Tester configuration
    TESTER_NAME = "Christian"  # Enter your name here
    BROWSER = "Chrome"          # Browser being used
    
    # Monitor configuration
    USE_SECOND_MONITOR = True   # Set to True to open browser on second monitor
    MONITOR_OFFSET = 1920       # X offset (typically your primary monitor's width in pixels)
                           
    
    # ==========================================
    #           RUN AUTOMATION
    # ==========================================
    
    # Create and run automation
    automation = SCDWebAutomation(
        base_url=BASE_URL,
        use_second_monitor=USE_SECOND_MONITOR,
        monitor_offset=MONITOR_OFFSET,
        tester_name=TESTER_NAME,
        browser=BROWSER
    )
    success = automation.run(login_type=LOGIN_TYPE)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()