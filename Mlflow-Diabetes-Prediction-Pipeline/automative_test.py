import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class PredictionDiabetes(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
    login_url = "http://localhost:3000/login/"
    home_url = "http://localhost:3000/"
    index_title = "Prediction Diabetes"
    title_msg = "Maybe you access the wrong webpage"
    def test_login_failed(self):
        driver = self.driver
        driver.get(self.login_url)
        self.assertEqual(self.index_title, driver.title,self.title_msg)
        username = driver.find_element(By.NAME,"username")
        password = driver.find_element(By.NAME,"password")
        username.send_keys("admin")
        password.send_keys("error_password")
        time.sleep(2)
        password.send_keys(Keys.RETURN)
        #login failed
        loginError = driver.find_element(By.ID,'loginError')
        time.sleep(2)
        self.assertEqual("user name or password incorrect",loginError.text,"Got the incorrect prompt on the webpage")
        assert self.login_url == driver.current_url

    def test_login_sucess(self):
        driver = self.driver
        driver.get(self.login_url)
        self.assertEqual(self.index_title, driver.title,self.title_msg)
        username = driver.find_element(By.NAME,"username")
        password = driver.find_element(By.NAME,"password")
        username.send_keys("admin")
        password.send_keys("admin")
        time.sleep(2)
        password.send_keys(Keys.RETURN)
        #login success
        prediction_result = driver.find_element(By.ID,"prediction_result")
        time.sleep(2)
        self.assertEqual("click predict button to get result",prediction_result.text,"This webpage isn't a home page")
        assert self.home_url == driver.current_url
        
    def test_prediction_no_risk(self):
        #login first
        self.login() 
        driver = self.driver
        prediction_button = driver.find_element(By.ID,"prediction_button")
        prediction_button.click()
        prediction_result = driver.find_element(By.ID,"prediction_result")
        time.sleep(2)
        self.assertIn("congratulations! No diabetes risk",prediction_result.text,"Didn't got the no risk prompt")

    def test_prediction_risk(self):
        #login first
        self.login()
        driver = self.driver
        #adjust the HbA1c_level parameter
        HbA1c_level_Span = driver.find_element(By.ID,'HbA1c_level')
        #input label hidden in span label
        input_hidden = HbA1c_level_Span.find_element(By.TAG_NAME,'input')
        #Get the value from the <input> element
        input_value = input_hidden.get_attribute('value')
        #set the new value
        input_value = 7.0
        prediction_button = driver.find_element(By.ID,"prediction_button")
        prediction_button.click()
        time.sleep(2)
        prediction_result = driver.find_element(By.ID,"prediction_result")
        self.assertIn("congratulations! No diabetes risk",prediction_result.text,"Didn't got the risk prompt")
    
    def login(self):
        self.driver.get(self.login_url)
        username = self.driver.find_element(By.NAME,"username")
        password = self.driver.find_element(By.NAME,"password")
        username.send_keys("admin")
        password.send_keys("admin")
        time.sleep(2)
        password.send_keys(Keys.RETURN)
        
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()