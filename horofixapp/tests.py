import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# class Logintest(unittest.TestCase):

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

     
#         loginid = driver.find_element(By.CSS_SELECTOR, "a[href='/login/'] > i.fa.fa-sign-in[aria-hidden='true']")
#         loginid.click()
#         time.sleep(2)


#         username= driver.find_element(By.CSS_SELECTOR, "input[name='username'][type='text'][placeholder='USERNAME'][required]")
#         username.send_keys("anitta")
#         password = driver.find_element(By.CSS_SELECTOR, "input[type='password'][placeholder='PASSWORD'][name='password'][required=''][onchange='validatePassword(this)']")
#         password.send_keys("Ammu@123")
        
#         submit1 = driver.find_element(By.ID, "test_id")
#         submit1.click()
#         time.sleep(2)
        
#         logout = driver.find_element(By.CSS_SELECTOR, "a[href='/logout/'] i.fa.fa-sign-out")
#         logout.click()
#         time.sleep(2)



class Service(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(1)
        self.live_server_url = 'http://127.0.0.1:8000/'

    def tearDown(self):
        self.driver.quit()

    def test_complete_shopping_flow(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(1)

     
        loginid = driver.find_element(By.CSS_SELECTOR, "a[href='/login/'] > i.fa.fa-sign-in[aria-hidden='true']")
        loginid.click()
        time.sleep(2)


        username= driver.find_element(By.CSS_SELECTOR, "input[name='username'][type='text'][placeholder='USERNAME'][required]")
        username.send_keys("anitta")
        password = driver.find_element(By.CSS_SELECTOR, "input[type='password'][placeholder='PASSWORD'][name='password'][required=''][onchange='validatePassword(this)']")
        password.send_keys("Ammu@123")
        
        submit1 = driver.find_element(By.ID, "test_id")
        submit1.click()
        time.sleep(2)
        service = driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/service/']")
        service.click()
        time.sleep(2)
        repair = driver.find_element(By.CSS_SELECTOR, "a.repair-section[href='/repairing/']")
        repair.click()
        time.sleep(2)
        rep = driver.find_element(By.ID, "watch")
        rep.click()
        time.sleep(2)
        su = driver.find_element(By.ID, "watchName")
        su.click()
        time.sleep(2)
        ani=driver.find_element(By.CSS_SELECTOR,"option[value='horofix 3']")
        ani.click()
        time.sleep(2)