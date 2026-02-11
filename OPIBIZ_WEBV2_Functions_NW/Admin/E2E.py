# END-TO-END TESTING 
import traceback
import sys
import os
import time
import screeninfo
from datetime import datetime
from typing import Tuple, Optional

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Add paths to custom modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'OPIBIZ_WEBV2_Functions_NW')))

# Import centralized path configuration
from path_config import MODULE_PATHS, LOGIN_PATHS, chromedriver_path, base_files_path,login_credentials_path

# Login Module
from Login.Login import login_admin, login_s2, login_class_c

# Branch Selection Module
from Branch.Branch_Terminal import branch_selection

# Logout Module
from Logout.Logout import Logout

# Utility Files 
from Utility import log_action, clear_terminal, clear_folder, log_error

# Admin and Profile
from My_Profile.Profile import Profile

# QR Module


#---- SCD Web Modules ----#
from Main_Dashboard.Dashboard import Main_Dashboard
from Seller_Center.Seller_Dashboard.SDashboard import SDashboard
from Seller_Center.Create_Order.COrder_View import COrderview
from Seller_Center.Order_Management.COrder import COrder
from Seller_Center.Order_Management.MOrder import MOrder
from Seller_Center.Order_Management.OMQR import OMQR
from Seller_Center.Product_Management.CNProduct import CNProduct
from Seller_Center.Product_Management.MProduct import MProduct
from Seller_Center.Product_Management.CNProducts_Bulk import Bulk
from Seller_Center.Inventory_Management.IManagement import Inventory_Management
from Service_Center.Booking_Appointments.Booking import SCDBookings
from OPIBIZ_WEBV2_Functions_NW.Service_Center.Create_Service_Order.CSOrder_View import CSOrder
from Service_Center.Service_Order_Management.CSOrder_View import CSOrder_View
from Service_Center.Service_Order_Management.MSOrder import MSOrder
from Service_Center.Service_Management.CNService import Create_New_Service
from Service_Center.Service_Management.MService import MService
from Service_Center.Service_Management.CService_Bulk import CService_Bulk
from Business_Hub.Cash_Management.Cash_management import CashManagement
from Business_Hub.Shop_Management.Branch import Branches
from Business_Hub.Shop_Management.WHouse import WHouse
from Business_Hub.Employee_Management.AEmployee import NEmployee
from Business_Hub.Employee_Management.EList import EList
from Business_Hub.Employee_Management.ANewEmployeeBulk import Bulk_Employee
from Business_Hub.Client_Directory.ANClient import ANClient
from Business_Hub.Client_Directory.CList import CList
from Send_Money.OmniPayAcc import OmniPayAcc
from Send_Money.AnotherBank import AnotherBank
from Send_Money.MultipleAcc import MultipleAcc
from Send_Money.TelegraphicTransfer import TelegraphicTransfer
from Send_Money.PayBills import PayBills
from My_Profile.Profile import Profile
from Audit.AuditLogs import AuditLogs


#=========================================================
#                MAIN AUTOMATION CLASS
#=========================================================
class SCDWebAutomation:
    def __init__(self, base_url: str = "http://vm-app-dev01:9001/", browser: str = "chrome"):
        self.base_url = base_url
        self.browser = browser.lower() 
        self.driver = None
        self.wait = None
        self.log_file_path = LOGIN_PATHS['Class_C']['log']
        self.screenshots_folder = LOGIN_PATHS['Class_C']['screenshots']
        self.test_results = {
            'passed': [],
            'failed': [],
            'skipped': []
        }
    
    #-----------------------------------------------------
    # Initialize browser based on selection
    #-----------------------------------------------------
    def _initialize_chrome(self):
      # Make sure to: pip install screeninfo
    
        chrome_options = ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        
        try:
            # === AUTO-DETECT 2ND MONITOR ===
            screens = screeninfo.get_monitors()
            if len(screens) >= 2:
                # Use 2nd monitor (index 1)
                second_monitor = screens[1]
              
            
                # Position window on 2nd monitor (let it maximize naturally)
                chrome_options.add_argument("--start-maximized")
            else:
                print("⚠️ Only 1 monitor detected, using primary monitor")
                chrome_options.add_argument("--start-maximized")
                
        except Exception as e:
            print(f"⚠️ Could not detect monitors: {e}")
            print("Using default window positioning")
            chrome_options.add_argument("--start-maximized")
        
        # === OTHER OPTIONS ===
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.page_load_strategy = 'normal'

        # Disable Chrome autofill & password prompts
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "autofill.profile_enabled": False,
            "autofill.credit_card_enabled": False,
            "autofill.address_enabled": False,
            "autofill.enabled": False
        }
        chrome_options.add_experimental_option("prefs", prefs)

        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    #-----------------------------------------------------
    # Setup the test environment
    #-----------------------------------------------------
    def setup(self) -> bool:
        try:
            clear_terminal()
            print("=" * 70)
            print("OMNIPAY BUSINESS SCD WEB AUTOMATION".center(70))
            print("=" * 70)
            print(f"🌐 Browser: {self.browser.upper()}".center(70))
            print("=" * 70)

            # Ensure directories exist
            os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)
            os.makedirs(self.screenshots_folder, exist_ok=True)

            # Clear old screenshots
            clear_folder(screenshots_folder=self.screenshots_folder)

            # Initialize driver based on browser selection
            print(f"\n🔧 Initializing {self.browser.upper()} WebDriver...")

            if self.browser == "chrome":
                self.driver = self._initialize_chrome()
            elif self.browser == "firefox":
                self.driver = self._initialize_firefox()
            elif self.browser == "edge":
                self.driver = self._initialize_edge()
            else:
                raise ValueError(f"Unsupported browser: {self.browser}. Use 'chrome', 'firefox', or 'edge'")

            self.wait = WebDriverWait(self.driver, 15)

            # Navigate to base URL
            print(f"🌐 Navigating to: {self.base_url}")
            self.driver.get(self.base_url)
            self.driver.execute_script("document.body.style.zoom='75%'")

            log_action(f"Setup completed successfully with {self.browser}", log_file_path=self.log_file_path)
            print(f"✅ Setup completed successfully with {self.browser.upper()}\n")
            return True

        except Exception as e:
            print(f"❌ Setup failed: {str(e)}")
            log_error(f"Setup failed: {str(e)}", log_file_path=self.log_file_path)
            traceback.print_exc()
            return False
    #-----------------------------------------------------
    # Login phase
    #-----------------------------------------------------
    def login(self, login_type: str = "class_c") -> Tuple[Optional[str], Optional[str]]:
        try:
            print("-" * 70)
            print("🔐 LOGIN PHASE".center(70))
            print("-" * 70)

            # DEFINE excel_path FIRST - before using it!
            base_files_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Files"))
            excel_path = os.path.join(base_files_path, "Testdata", "login_credentials.xlsx")

            # # NOW print debug info
            # print(f"\n🔍 DEBUG INFO:")
            # print(f"   base_files_path: {base_files_path}")
            # print(f"   Excel path: {excel_path}")
            # print(f"   File exists: {os.path.exists(excel_path)}")

            # # Check parent directory
            # parent_files = os.path.join(os.path.dirname(base_files_path), 'Files', 'Testdata', 'login_credentials.xlsx')
            # print(f"   Checking parent: {parent_files}")
            # print(f"   Parent exists: {os.path.exists(parent_files)}")

            print(f"🔍 Attempting login as: {login_type}")
            
            if login_type == "admin":
                print("   Calling login_admin...")
                username, password = login_admin(self.driver, excel_path)
            elif login_type == "s2":
                print("   Calling login_s2...")
                username, password = login_s2(self.driver, excel_path)
            elif login_type == "class_c":
                print("   Calling login_class_c...")
                username, password = login_class_c(self.driver, excel_path)
            else:
                raise ValueError(f"Invalid login type: {login_type}")

            log_action(f"Login successful with {login_type}", log_file_path=self.log_file_path)
            print(f"✅ Login successful as: {username}\n")
            return username, password

        except Exception as e:
            print(f" Login failed: {str(e)}")
            print(f"   Error type: {type(e).__name__}")
            log_error(f"Login failed: {str(e)}", log_file_path=self.log_file_path)
            self.capture_screenshot("login_failed")
            traceback.print_exc()
            return None, None

        except Exception as e:
            print(f" Login failed: {str(e)}")
            print(f"   Error type: {type(e).__name__}")
            log_error(f"Login failed: {str(e)}", log_file_path=self.log_file_path)
            self.capture_screenshot("login_failed")
            traceback.print_exc()  # This will show the full stack trace
            return None, None

    #-----------------------------------------------------
    # Branch selection
    #-----------------------------------------------------
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
            print(f" Branch selection failed: {str(e)}")
            log_error(f"Branch selection failed: {str(e)}", log_file_path=self.log_file_path)
            self.capture_screenshot("branch_selection_failed")
            return False
    #-----------------------------------------------------
    # Run all SCD Web test modules
    #-----------------------------------------------------
    def run_scdweb_tests(self) -> dict:
    
        print("=" * 70)
        print("🚀 SCD WEB TESTING PHASE".center(70))
        print("=" * 70)
        print()

        # ALL MODULES
        module_groups = {
            "Main Dashboard": [
                ("Main Dashboard", Main_Dashboard)
            ],
            "Seller Center": [
                ("Seller Center Dashboard", SDashboard),
                ("Create Order View Only", COrderview),
                ("Create Single Order", COrder),
                ("Manage Order", MOrder),
                ("Generate QR", OMQR),
                ("Create New Product", CNProduct),
                ("Manage Product", MProduct),
                ("Create New Product - Bulk", Bulk),
                ("Inventory Management", Inventory_Management),
            ],
            "Service Center": [
                # ("Booking and Appointments", SCDBookings),
                ("Create Service Order", CSOrder),
                ("Create Service Order View Only", CSOrder_View),
                ("Manage Service Order", MSOrder),
                ("Create New Service", Create_New_Service),
                ("Manage Service", MService),
                ("Create Service Bulk", CService_Bulk),
            ],
            "Business Hub": [
                ("Cash Management", CashManagement),
                ("Branches", Branches),
                ("Warehouse", WHouse),
                ("Added New Employee", NEmployee),
                ("Employee List", EList),
                ("Add New Client", ANClient),
                ("Client List", CList),
            ],
            "Send Money": [
                ("To Another OmniPay Account", OmniPayAcc),
                ("To Another Bank", AnotherBank),
                ("To Multiple Accounts", MultipleAcc),
                ("Request Telegraphic Transfer", TelegraphicTransfer),
                ("Pay Bills", PayBills),
            ],
            "Profile": [
                ("My Profile", Profile)
            ],
            "Audit Logs": [
                ("Audit Logs", AuditLogs)
            ]
        }

        self.test_results = {"passed": [], "failed": []}
        module_index = 1
        total_modules = sum(len(v) for v in module_groups.values())

        for group_name, modules in module_groups.items():
            print(f"\n📂 Running Group: {group_name}\n{'-' * 70}")
            for name, func in modules:
                try:
                    print(f"[{module_index}/{total_modules}] 🔹 Testing: {name}")
                    start_time = time.time()

                    func(self.driver, self.wait)

                    elapsed_time = time.time() - start_time
                    log_action(f"{name} - PASSED ({elapsed_time:.2f}s)", log_file_path=self.log_file_path)
                    self.test_results['passed'].append(name)
                    print(f"✅ {name} - PASSED ({elapsed_time:.2f}s)\n")

                    time.sleep(2)

                except Exception as e:
                    error_msg = f"{name} - FAILED: {str(e)}"
                    log_error(error_msg, log_file_path=self.log_file_path)
                    self.test_results['failed'].append(name)
                    self.capture_screenshot(f"{name.replace(' ', '_')}_failed")
                    print(f"❌ {name} - FAILED\n   Error: {str(e)}\n")

                module_index += 1

        # Print summary
        print("=" * 70)
        print("📝 TEST SUMMARY".center(70))
        print("=" * 70)
        for name, status in [("PASSED", self.test_results['passed']), ("FAILED", self.test_results['failed'])]:
            print(f"\n{name}:")
            for module_name in status:
                print(f" - {module_name}")

        return self.test_results

    #-----------------------------------------------------
    # Logout
    #-----------------------------------------------------
    def logout(self) -> bool:
        try:
            print("\n" + "-" * 70)
            print("🚪 LOGOUT PHASE".center(70))
            print("-" * 70)

            Logout(self.driver, self.wait)
            log_action("Logout completed", log_file_path=self.log_file_path)
            print("✅ Logout completed\n")
            return True

        except Exception as e:
            print(f" Logout failed: {str(e)}")
            log_error(f"Logout failed: {str(e)}", log_file_path=self.log_file_path)
            return False

    #-----------------------------------------------------
    # Screenshot capture
    #-----------------------------------------------------
    def capture_screenshot(self, name: str):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_file = os.path.join(self.screenshots_folder, f"{name}_{timestamp}.png")
        try:
            self.driver.save_screenshot(screenshot_file)
        except Exception:
            pass

    #-----------------------------------------------------
    # Clean up resources
    #-----------------------------------------------------
    def cleanup(self):
        try:
            print("\n🧹 Cleaning up...")
            time.sleep(2)
            if self.driver:
                self.driver.quit()
                log_action("Browser closed", log_file_path=self.log_file_path)
                print("✅ Browser closed successfully")
        except Exception as e:
            print(f"⚠️ Cleanup warning: {str(e)}")

    #-----------------------------------------------------
    # Main execution
    #-----------------------------------------------------
    def run(self, login_type="class_c") -> bool:
        try:
            start_time = time.time()

            if not self.setup():
                return False
            username, password = self.login(login_type)
            if not username:
                return False
            if not self.select_branch():
                return False

            self.run_scdweb_tests()
            self.logout()

            total_time = time.time() - start_time
            mins, secs = divmod(total_time, 60)
            print(f"\n⏱️ Total Execution Time: {int(mins)}m {int(secs)}s")

            log_action(f"Automation completed in {int(mins)}m {int(secs)}s", log_file_path=self.log_file_path)
            return True

        except Exception as e:
            print(f"\n Critical error: {str(e)}")
            log_error(f"Critical error: {str(e)}", log_file_path=self.log_file_path)
            traceback.print_exc()
            return False

        finally:
            self.cleanup()


#=========================================================
# Entry Point
#=========================================================
def main():
    BASE_URL = "http://vm-app-dev01:9001/"
    LOGIN_TYPE = "class_c"
    BROWSER = "chrome"

    automation = SCDWebAutomation(base_url=BASE_URL, browser=BROWSER)
    success = automation.run(login_type=LOGIN_TYPE)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
