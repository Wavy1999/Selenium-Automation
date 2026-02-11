# Run tests across multiple browsers
import sys
from Cross_Browsing import SCDWebAutomation

def run_cross_browser_tests():
    BASE_URL = "http://beta-opibizscd.paybps.ovpn/"
    LOGIN_TYPE = "class_c"
    BROWSERS = ["chrome", "firefox", "edge"]
    
    results = {}
    
    for browser in BROWSERS:
        print(f"\n{'='*70}")
        print(f"STARTING TESTS ON {browser.upper()}".center(70))
        print(f"{'='*70}\n")
        
        automation = SCDWebAutomation(base_url=BASE_URL, browser=browser)
        success = automation.run(login_type=LOGIN_TYPE)
        
        results[browser] = {
            'success': success,
            'test_results': automation.test_results
        }
        
        print(f"\n{'='*70}")
        print(f"{browser.upper()} TESTS COMPLETED".center(70))
        print(f"{'='*70}\n")
    
    # Print summary
    print("\n" + "="*70)
    print("CROSS-BROWSER TEST SUMMARY".center(70))
    print("="*70)
    
    for browser, result in results.items():
        status = "✅ PASSED" if result['success'] else "❌ FAILED"
        print(f"\n{browser.upper()}: {status}")
        print(f"  Passed: {len(result['test_results']['passed'])}")
        print(f"  Failed: {len(result['test_results']['failed'])}")
        print(f"  Skipped: {len(result['test_results']['skipped'])}")

if __name__ == "__main__":
    run_cross_browser_tests()