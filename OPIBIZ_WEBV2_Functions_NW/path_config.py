import os

# ==========================================
# Choose ACTIVE System at runtime
# Options: "SCD", "REST", "ALL"
# ==========================================
ACTIVE_SYSTEM = "SCD"    # <-- your test runner will override this

# ==========================================
# Base Paths
# ==========================================
current_file_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_file_dir)

base_files_path = os.path.join(parent_dir, 'Files')
base_logs_path = os.path.join(base_files_path, 'logs')
base_screenshot_path = os.path.join(base_files_path, 'screenshots')

login_credentials_path = os.path.join(base_files_path, 'Testdata', 'login_credentials.xlsx')

# ==========================================
# Folder Groups
# ==========================================
scd_logs = os.path.join(base_logs_path, "SCD")
scd_screens = os.path.join(base_screenshot_path, "SCD")

rest_logs = os.path.join(base_logs_path, "REST")
rest_screens = os.path.join(base_screenshot_path, "REST")

# ==========================================
# Helper
# ==========================================
def mod(name: str, log_folder: str, ss_folder: str):
    return {
        "log": os.path.join(log_folder, f"{name}.txt"),
        "screenshots": os.path.join(ss_folder, name)
    }

# ==========================================
# SCD MODULES
# ==========================================
SCD_MODULE_PATHS = {

    # Select Branch
    "BranchSelect": mod("BranchSelect", scd_logs, scd_screens),

    # Main Dashboard
    "Dashboard": mod("Dashboard", scd_logs, scd_screens),

    # Seller Center
    "SDashboard": mod("SDashboard", scd_logs, scd_screens),
    "COrder": mod("COrder", scd_logs, scd_screens),
    "COrder_View": mod("COrder_View", scd_logs, scd_screens),
    "MOrder": mod("MOrder", scd_logs, scd_screens),
    "OMQR": mod("OMQR", scd_logs, scd_screens),

    "CNProduct": mod("CNProduct", scd_logs, scd_screens),
    "MProduct": mod("MProduct", scd_logs, scd_screens),
    "CNProducts_Bulk": mod("CNProducts_Bulk", scd_logs, scd_screens),

    "IManagement": mod("IManagement", scd_logs, scd_screens),

    # Service Center
    "SCDBooking": mod("SCDBooking", scd_logs, scd_screens),
    "SCDBooking_Bulk": mod("SCDBooking_Bulk", scd_logs, scd_screens),
    "CSOrder": mod("CSOrder", scd_logs, scd_screens),
    "CSOrder_View": mod("CSOrder_View", scd_logs, scd_screens),
    "MSOrder": mod("MSOrder", scd_logs, scd_screens),

    "CNService": mod("CNService", scd_logs, scd_screens),
    "MService": mod("MService", scd_logs, scd_screens),
    "CService_Bulk": mod("CService_Bulk", scd_logs, scd_screens),

    # Business Hub
    "CashManagement": mod("CashManagement", scd_logs, scd_screens),
    "Branches": mod("Branches", scd_logs, scd_screens),
    "WHouse": mod("WHouse", scd_logs, scd_screens),
    "WHouse_Bulk": mod("WHouse_Bulk", scd_logs, scd_screens),
    "NEmployee": mod("NEmployee", scd_logs, scd_screens),
    "Employee_Bulk": mod("Employee_Bulk", scd_logs, scd_screens),
    "EList": mod("EList", scd_logs, scd_screens),
    "ANClient": mod("ANClient", scd_logs, scd_screens),
    "CList": mod("CList", scd_logs, scd_screens),
    "Client_Bulk": mod("Client_Bulk", scd_logs, scd_screens),

    # Send Money
    "OmniPayAcc": mod("OmniPayAcc", scd_logs, scd_screens),
    "AnotherBank": mod("AnotherBank", scd_logs, scd_screens),
    "MultipleAcc": mod("MultipleAcc", scd_logs, scd_screens),
    "TelegraphicTransfer": mod("TelegraphicTransfer", scd_logs, scd_screens),
    "PayBills": mod("PayBills", scd_logs, scd_screens),

    # Profile & Audit
    "Profile": mod("Profile", scd_logs, scd_screens),
    "AuditLogs": mod("AuditLogs", scd_logs, scd_screens),

    # Generate QR
    "QR": mod("QR", scd_logs, scd_screens),
    
}

# ==========================================
# RESTAURANT CENTER MODULES
# ==========================================
REST_MODULE_PATHS = {
    "Home": mod("Home", rest_logs, rest_screens),
    "Orders": mod("Orders", rest_logs, rest_screens),
    "Manage_Orders": mod("Manage_Orders", rest_logs, rest_screens),
    "Bookings": mod("Bookings", rest_logs, rest_screens),
    "Tables": mod("Tables", rest_logs, rest_screens),
    "Menu": mod("Menu", rest_logs, rest_screens),
    "Printer_Setting": mod("Printer_Setting", rest_logs, rest_screens),
    "Invoice_Settings": mod("Invoice_Settings", rest_logs, rest_screens),
}

# ==========================================
# LOGIN PATHS (always created)
# ==========================================
LOGIN_PATHS = {
    role: {
        "log": os.path.join(base_logs_path, "Login", f"{role}.txt"),
        "screenshots": os.path.join(base_screenshot_path, "Login", role),
        "excel_path": login_credentials_path,
    }
    for role in ["Admin", "S1", "S2", "Logistics", "SecAd", "Class_C"]
}

# logout
LOGIN_PATHS["Logout"] = {
    "log": os.path.join(base_logs_path, "Logout", "Logout.txt"),
    "screenshots": os.path.join(base_screenshot_path, "Logout")
}

# ==========================================
# Conditional Folder Creation
# ==========================================

def create_folders():
    if ACTIVE_SYSTEM in ("SCD", "ALL"):
        for cfg in SCD_MODULE_PATHS.values():
            os.makedirs(cfg["screenshots"], exist_ok=True)
            os.makedirs(os.path.dirname(cfg["log"]), exist_ok=True)

    if ACTIVE_SYSTEM in ("REST", "ALL"):
        for cfg in REST_MODULE_PATHS.values():
            os.makedirs(cfg["screenshots"], exist_ok=True)
            os.makedirs(os.path.dirname(cfg["log"]), exist_ok=True)

    # Login folders always created
    for login in LOGIN_PATHS.values():
        os.makedirs(login["screenshots"], exist_ok=True)
        os.makedirs(os.path.dirname(login["log"]), exist_ok=True)

    print(f"📁 Folder creation completed for: {ACTIVE_SYSTEM}")


# Run on import
create_folders()
