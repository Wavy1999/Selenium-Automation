from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def verify_login_success(driver, username, timeout=10):
    
    try:
        # Wait for the page to load after login
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        
        # Method 1: Check if dashboard/home page loaded
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.ID, "dashboard"))
            )
            print(f"✓ Dashboard loaded successfully")
        except TimeoutException:
            # Try alternative success indicators
            pass
        
        # Method 2: Check URL changed from login page
        current_url = driver.current_url.lower()
        if "login" in current_url:
            raise AssertionError(f"Still on login page: {current_url}")
        print(f"✓ URL redirected from login page")
        
        # Method 3: Check for error messages (should NOT exist)
        error_selectors = [
            (By.CLASS_NAME, "error-message"),
            (By.CLASS_NAME, "alert-danger"),
            (By.XPATH, "//*[contains(text(), 'Invalid')]"),
            (By.XPATH, "//*[contains(text(), 'incorrect')]"),
            (By.XPATH, "//*[contains(text(), 'failed')]")
        ]
        
        for by, selector in error_selectors:
            error_elements = driver.find_elements(by, selector)
            if error_elements and error_elements[0].is_displayed():
                error_text = error_elements[0].text
                raise AssertionError(f"Login error message found: {error_text}")
        print(f"✓ No error messages detected")
        
        # Method 4: Check for user-specific elements
        user_indicators = [
            (By.ID, "user-profile"),
            (By.CLASS_NAME, "user-menu"),
            (By.XPATH, "//span[contains(@class, 'username')]"),
            (By.XPATH, f"//*[contains(text(), '{username}')]")
        ]
        
        user_found = False
        for by, selector in user_indicators:
            try:
                element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((by, selector))
                )
                if element.is_displayed():
                    user_found = True
                    print(f"✓ User element found: {selector}")
                    break
            except TimeoutException:
                continue
        
        if not user_found:
            print("⚠ Warning: User-specific element not found, but other checks passed")
        
        # Method 5: Check for navigation menu (indicates successful login)
        try:
            nav_menu = driver.find_element(By.TAG_NAME, "nav")
            if nav_menu.is_displayed():
                print(f"✓ Navigation menu visible")
        except NoSuchElementException:
            pass
        
        print(f"✓ Login verification PASSED for user: {username}")
        return True
        
    except AssertionError as e:
        print(f"✗ Login verification FAILED: {str(e)}")
        raise
    except Exception as e:
        print(f"✗ Login verification ERROR: {str(e)}")
        raise AssertionError(f"Login verification failed: {str(e)}")


def verify_login_failure(driver, expected_error_message=None, timeout=5):
  
    try:
        # Should still be on login page
        current_url = driver.current_url.lower()
        assert "login" in current_url, f"Not on login page: {current_url}"
        
        # Error message should be present
        error_element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "error-message"))
        )
        
        error_text = error_element.text
        print(f"✓ Error message found: {error_text}")
        
        # Verify specific error message if provided
        if expected_error_message:
            assert expected_error_message.lower() in error_text.lower(), \
                f"Expected '{expected_error_message}', got '{error_text}'"
            print(f"✓ Error message matches expected")
        
        # Dashboard should NOT be present
        dashboard_elements = driver.find_elements(By.ID, "dashboard")
        assert len(dashboard_elements) == 0, "Dashboard found - login should have failed"
        
        print(f"✓ Login failure verified successfully")
        return True
        
    except TimeoutException:
        raise AssertionError("Expected login error message not found - login may have succeeded")
    except AssertionError:
        raise
    except Exception as e:
        raise AssertionError(f"Login failure verification error: {str(e)}")