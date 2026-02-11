import os
from selenium.webdriver.support.events import AbstractEventListener
from datetime import datetime

# Global screenshot map { test_name: [list_of_screenshot_paths] }
screenshot_map = {}

class ClickScreenshotListener(AbstractEventListener):
    def after_click(self, element, driver):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        folder = os.path.join(os.getcwd(), "screenshots")
        os.makedirs(folder, exist_ok=True)

        file_name = f"click_{timestamp}.png"
        path = os.path.join(folder, file_name)
        driver.save_screenshot(path)

        # Identify test name (pytest test node id)
        test_name = getattr(driver, "_current_test_name", "unknown_test")

        # Save into global screenshot map
        if test_name not in screenshot_map:
            screenshot_map[test_name] = []
        screenshot_map[test_name].append(path)

        print(f"[ClickScreenshotListener] Saved: {path}")
