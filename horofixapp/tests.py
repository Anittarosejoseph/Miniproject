import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class LoginTest(unittest.TestCase):
    def setUp(self):
        # Start the Selenium WebDriver
        self.driver = webdriver.Chrome()  # Adjust based on your WebDriver configuration
        self.driver.get("http://127.0.0.1:8000/login")  # Replace with the actual URL of your login page

    def test_login_successful(self):
        # Find the username, password, and login button elements
        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")
        login_button = self.driver.find_element(By.XPATH, "//button[text()='LOGIN']")

        # Enter valid credentials
        username_input.send_keys("anitta")
        password_input.send_keys("Ammu@123")

        # Click the login button
        login_button.click()

        # Wait for a while to see the result (you can adjust this based on your application's response time)
        time.sleep(200)

        # Check if the login was successful (you may need to adapt this based on your application)
        self.assertIn("dashboard", self.driver.current_url.lower())

    
    def tearDown(self):
        # Close the browser window
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
