# debug_driver.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

print("1. Setting up Chrome Driver...")
try:
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Keep this commented out to see the browser
    
    print("2. Starting Browser...")
    driver = webdriver.Chrome(service=service, options=options)
    
    print("3. Navigating to Google...")
    driver.get("https://www.google.com")
    
    print("4. Success! Browser opened. Closing in 3 seconds...")
    time.sleep(3)
    driver.quit()
except Exception as e:
    print(f"\nFAILED: {e}")