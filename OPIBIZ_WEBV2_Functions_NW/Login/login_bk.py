import pandas as pd
from selenium.webdriver.common.by import By
from Utility import log_action,clear_folder
from Path import login_admin_log, login_s1_log, login_s2_log, login_logistics_log, login_secad_log
import os

from path_config import MODULE_PATHS

def login_admin(driver, excel_path):
    data = pd.read_excel(excel_path, sheet_name='Admin')
    row = data.sample(n=1).iloc[0]
    username, password = row['Username'], row['Password']

    driver.find_element(By.ID, "username").send_keys("C.r001.OBiz.masteradmin")
    log_action("Enter username login_admin", log_file_path=login_admin_log)

    driver.find_element(By.ID, "password").send_keys(":UOqNEzRvS0B")
    log_action("Enter password login_admin", log_file_path=login_admin_log)

    driver.find_element(By.NAME, "submit").click()
    log_action("Click submit login_admin", log_file_path=login_admin_log)

    return username, password

def login_s1(driver, excel_path):
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(current_file_dir, '..', '..', 'Files', 'logs', 'Login', 'Login.txt')
    screenshots_folder = os.path.join(current_file_dir, '..', '..', 'Files', 'screenshots', 'Login')

    # Clear old files before test run  
    clear_folder(screenshots_folder=screenshots_folder)


    data = pd.read_excel(excel_path, sheet_name='S1')
    row = data.sample(n=1).iloc[0]
    username, password = row['Username'], row['Password']
    driver.find_element(By.ID, "username").send_keys("B.R004.OBiz.branchopstaff")
    log_action("Enter username login_s1", log_file_path=login_s1_log)
    driver.find_element(By.ID, "password").send_keys("MRgC04H323221G30")
    log_action("Enter password login_s1", log_file_path=login_s1_log)
    driver.save_screenshot(os.path.join(screenshots_folder, 'Login.png'))
    driver.find_element(By.NAME, "submit").click()
    log_action("Click submit login_s1", log_file_path=login_s1_log)
    return username, password


def login_s2(driver, excel_path):
    data = pd.read_excel(excel_path, sheet_name='S2')
    row = data.sample(n=1).iloc[0]
    username, password = row['Username'], row['Password']

    driver.find_element(By.ID, "username").send_keys("B.R004.OBiz.branchopstaff")
    log_action("Enter username login_s2", log_file_path=login_s2_log)

    driver.find_element(By.ID, "password").send_keys("MRgC04H21G30")
    log_action("Enter password login_s2", log_file_path=login_s2_log)

    driver.find_element(By.NAME, "submit").click()
    log_action("Click submit login_s2", log_file_path=login_s2_log)

    return username, password


def login_logistics(driver, excel_path):
    data = pd.read_excel(excel_path, sheet_name='Logistics')
    row = data.sample(n=1).iloc[0]
    username, password = row['Username'], row['Password']

    driver.find_element(By.ID, "username").send_keys(username)
    log_action("Enter username login_logistics", log_file_path=login_logistics_log)

    driver.find_element(By.ID, "password").send_keys(password)
    log_action("Enter password login_logistics", log_file_path=login_logistics_log)

    driver.find_element(By.NAME, "submit").click()
    log_action("Click submit login_logistics", log_file_path=login_logistics_log)

    return username, password


def login_secad(driver, excel_path):
    data = pd.read_excel(excel_path, sheet_name='SecAd')
    row = data.sample(n=1).iloc[0]
    username, password = row['Username'], row['Password']

    driver.find_element(By.ID, "username").send_keys(username)
    log_action("Enter username login_secad", log_file_path=login_secad_log)

    driver.find_element(By.ID, "password").send_keys(password)
    log_action("Enter password login_secad", log_file_path=login_secad_log)

    driver.find_element(By.NAME, "submit").click()
    log_action("Click submit login_secad", log_file_path=login_secad_log)

    return username, password
