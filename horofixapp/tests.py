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
        username_input.send_keys("admin")
        password_input.send_keys("God@07")

        # Click the login button
        login_button.click()

        time.sleep(2)
        self.assertEqual(self.driver.current_url, 'http://127.0.0.1:8000/adminpanel/')
    
    def tearDown(self):
        # Close the browser window
        self.driver.close()

if __name__ == "__main__":
    unittest.main()




# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time

# class Hosttest(unittest.TestCase):

#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.implicitly_wait(10)
#         self.live_server_url = 'http://127.0.0.1:8000/'

#     def tearDown(self):
#         self.driver.quit()

#     def test_complete_shopping_flow(self):
#         driver = self.driver
#         driver.get(self.live_server_url)
#         driver.maximize_window()
#         time.sleep(1)

#         # Login
#         login = driver.find_element(By.CSS_SELECTOR, "a[href='/login/'] > i.fa.fa-sign-in[aria-hidden='true']")
#         login.click()
#         time.sleep(2)

#         username= driver.find_element(By.CSS_SELECTOR, "input[name='username'][type='text'][placeholder='USERNAME'][required]")
#         username.send_keys("anitta")
#         password = driver.find_element(By.CSS_SELECTOR, "input[type='password'][placeholder='PASSWORD'][name='password'][required=''][onchange='validatePassword(this)']")
#         password.send_keys("Ammu@123")
        
#         submit = driver.find_element(By.ID, "test_id")
#         submit.click()
#         time.sleep(2)

#         product_button=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/customer_products/']")
#         product_button.click()
#         time.sleep(7)
#         search_input = driver.find_element(By.CSS_SELECTOR, "input#search_name.form-control")
#         search_input.send_keys("Boltt")
#         search_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
#         search_button.click()
#         time.sleep(2)        

# if __name__ == '__main__':
#     unittest.main()

# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time

# class edittestt(unittest.TestCase):

#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.implicitly_wait(10)
#         self.live_server_url = 'http://127.0.0.1:8000/'

#     def tearDown(self):
#         self.driver.quit()

#     def test_complete_shopping_flow(self):
#         driver = self.driver
#         driver.get(self.live_server_url)
#         driver.maximize_window()
#         time.sleep(1)

#         # Login
#         login = driver.find_element(By.CSS_SELECTOR, "a[href='/login/'] > i.fa.fa-sign-in[aria-hidden='true']")
#         login.click()
#         time.sleep(2)

#         username= driver.find_element(By.CSS_SELECTOR, "input[name='username'][type='text'][placeholder='USERNAME'][required]")
#         username.send_keys("admin")
#         password = driver.find_element(By.CSS_SELECTOR, "input[type='password'][placeholder='PASSWORD'][name='password'][required=''][onchange='validatePassword(this)']")
#         password.send_keys("God@07")
        
#         submit = driver.find_element(By.ID, "test_id")
#         submit.click()
#         time.sleep(2)
#         view_products_link = driver.find_element(By.CSS_SELECTOR, "a[href='/view_products/']")
#         view_products_link.click()
#         time.sleep(2)
#         edit_button = driver.find_element(By.CSS_SELECTOR, "a[href='/edit_product/1/'].btn.btn-primary")
#         edit_button.click()
#         time.sleep(2)
#         product_name_input = driver.find_element(By.CSS_SELECTOR, "input#product_name.form-control")
#         product_name_input.clear()
#         product_name_input.send_keys("Seikko")
      
#         product_price_input = driver.find_element(By.CSS_SELECTOR, "input#product_price.form-control")
#         product_price_input.clear()
#         product_price_input.send_keys("1500.00")  
#         product_sale_price_input = driver.find_element(By.CSS_SELECTOR, "input#product_sale_price.form-control")
#         product_sale_price_input.clear()
#         product_sale_price_input.send_keys("1200.00")  
#         discount_input = driver.find_element(By.CSS_SELECTOR, "input#discount.form-control")
#         discount_input.clear()
#         discount_input.send_keys("20.00")  
#         watch_description_input = driver.find_element(By.CSS_SELECTOR, "textarea#watch_description.form-control")
#         watch_description_input.clear()
#         watch_description_input.send_keys("Combining durability, precision and functionality..")
#         save_changes_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
#         save_changes_button.click()
#         time.sleep(2)

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

class ShoppingFlowTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/'

    def tearDown(self):
        self.driver.quit()

    def test_complete_shopping_flow(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(1)

        # Login
        login = driver.find_element(By.CSS_SELECTOR, "a[href='/login/'] > i.fa.fa-sign-in[aria-hidden='true']")
        login.click()
        time.sleep(2)

        # Enter username and password
        username = driver.find_element(By.CSS_SELECTOR, "input[name='username'][type='text'][placeholder='USERNAME'][required]")
        username.send_keys("admin")
        password = driver.find_element(By.CSS_SELECTOR, "input[type='password'][placeholder='PASSWORD'][name='password'][required=''][onchange='validatePassword(this)']")
        password.send_keys("God@07")

        # Submit login form
        submit = driver.find_element(By.ID, "test_id")  # Replace 'test_id' with the actual ID of the submit button
        submit.click()
        time.sleep(2)

        # Navigate to the "Add Product" page using the link
        add_product_link = driver.find_element(By.XPATH, "//a[@href='/add_product/']")
        add_product_link.click()
        time.sleep(2)

        # Fill out the form on the "Add Product" page
        category_dropdown = Select(driver.find_element(By.ID, "category"))
        category_dropdown.select_by_value("Women")  # Assuming 'Women' is the desired category

        product_name = driver.find_element(By.ID, "productName")
        product_name.send_keys("Horofix3")

        product_price = driver.find_element(By.ID, "productPrice")
        product_price.send_keys("5000")

        discount = driver.find_element(By.ID, "discount")
        discount.send_keys("10")

        watch_description = driver.find_element(By.ID, "watchDescription")
        watch_description.send_keys("Luxury,High quanlity.")

        stock = driver.find_element(By.ID, "stock")
        stock.send_keys("10")

        watch_image = driver.find_element(By.ID, "watchImage")
        watch_image.send_keys("C:/Users/Anitta Rose Joseph/Desktop/mini/media/watch_images/a-1_-_Copy_NtnqRH1.jpg")

        # Submit the form
        submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()

        # Wait for redirection or check for success message

        time.sleep(2)  # Adding a short delay to visually inspect the result

if __name__ == "__main__":
    unittest.main()
