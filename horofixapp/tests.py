import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        time.sleep(2)
        self.assertEqual(self.driver.current_url, 'http://127.0.0.1:8000/')
    
    def tearDown(self):
        # Close the browser window
        self.driver.close()

if __name__ == "__main__":
    unittest.main()


# Initialize the Chrome browser
driver = webdriver.Chrome()

# Open the URL
url = "http://127.0.0.1:8000/add_product/"
driver.get(url)

try:
    # Interact with form elements
    category_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'category'))
    )
    category_dropdown.send_keys('Men')

    product_name_input = driver.find_element(By.ID, 'productName')
    product_name_input.send_keys('horofix34')

    product_price_input = driver.find_element(By.ID, 'productPrice')
    product_price_input.send_keys('10000.00')

    discount_input = driver.find_element(By.ID, 'discount')
    discount_input.send_keys('75')

    watch_description_input = driver.find_element(By.ID, 'watchDescription')
    watch_description_input.send_keys('High Quantity')

    stock_input = driver.find_element(By.ID, 'stock')
    stock_input.send_keys('10')
    image_input = driver.find_element(By.ID, 'watchImage')
    image_path = 'C:\\Users\\Anitta Rose Joseph\\Desktop\\mini\\media\\watch_images\\a-1_-_Copy_Yk4ZVMG.jpg'
    image_input.send_keys(image_path)

    # Image upload can be more complex; adjust as per your application

    # Submit the form
    submit_button = driver.find_element(By.XPATH, '//input[@type="submit"]')
    submit_button.click()
    time.sleep(20)


    # Wait for redirection (adjust URL as per your application)
    WebDriverWait(driver, 10).until(
        EC.url_to_be("http://127.0.0.1:8000/view_products/")
    )

    # You can add additional assertions here if needed

except Exception as e:
    print(f"An error occurred: {str(e)}")


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the Chrome WebDriver
driver = webdriver.Chrome()

# Open the URL
url = "http://127.0.0.1:8000/login/?next=/customer_products/"  # Replace with the actual URL
driver.get(url)

try:
    # Example: Test the search functionality
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'search_name'))
    )
    search_input.send_keys("Product Name")  # Enter a sample search term
    search_input.send_keys(Keys.RETURN)

    # Example: Test the category filter functionality
    category_filter = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="category" and @value="Men"]'))
    )
    category_filter.click()

    # Example: Test the sorting functionality
    sort_option = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="sort_option" and @value="asc"]'))
    )
    sort_option.click()

    # Wait for the results to load (adjust the time based on your application's response time)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="product-card"]'))
    )

    # Additional test scenarios can be added based on your application's features

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    # Close the browser
    driver.quit()
