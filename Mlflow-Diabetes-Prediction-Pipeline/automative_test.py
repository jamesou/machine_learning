import unittest
import time
from html_reporter import HTMLTestRunner
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
# unittest with Selenium test webpages
class PredictionDiabetesTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
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
        time.sleep(1)
        password.send_keys(Keys.RETURN)
        #login failed
        loginError = driver.find_element(By.ID,'loginError')
        time.sleep(2)
        self.assertEqual("user name or password incorrect",loginError.text,"Got the incorrect prompt on the webpage")
        assert self.login_url == driver.current_url
        print("test_login_failed passed")
        pass

    def test_login_sucess(self):
        driver = self.driver
        driver.get(self.login_url)
        self.assertEqual(self.index_title, driver.title,self.title_msg)
        username = driver.find_element(By.NAME,"username")
        password = driver.find_element(By.NAME,"password")
        username.send_keys("admin")
        password.send_keys("admin")
        time.sleep(1)
        password.send_keys(Keys.RETURN)
        #login success
        prediction_result = driver.find_element(By.ID,"prediction_result")
        time.sleep(2)
        self.assertEqual("click predict button to get result",prediction_result.text,"This webpage isn't a home page")
        assert self.home_url == driver.current_url
        print("test_login_sucess passed")
        pass

    def test_prediction_no_risk(self):
        print("start to run test_prediction_no_risk")
        #login first
        self.login() 
        driver = self.driver
        prediction_button = driver.find_element(By.ID,"prediction_button")
        time.sleep(2)
        prediction_button.click()
        prediction_result = driver.find_element(By.ID,"prediction_result")
        time.sleep(1)
        self.assertIn("congratulations! No diabetes risk",prediction_result.text,"Didn't got the no risk prompt")
        print("test_prediction_no_risk passed")
        pass

    def test_prediction_risk(self):
        print("start to run test_prediction_risk")
        #login first
        self.login()
        driver = self.driver
        #adjust the HbA1c_level parameter
        HbA1c_level_Span = driver.find_element(By.ID,'HbA1c_level')
        #Find the hidden input field inside the <span> element
        input_hidden = HbA1c_level_Span.find_element(By.TAG_NAME,'input')
        #Get the value from the <input> element
        input_value = input_hidden.get_attribute('value')
        # print("oldvalue:"+input_value)
        # Create an ActionChains object
        action_chains = ActionChains(driver)
        offset = -45
        # Calculate the x_offset
        x_offset = float(input_value)+float(offset)
        # print(f"x_offset:",x_offset)
        # Perform the mouse drag operation to adjust the Slider's value
        action_chains.move_to_element(HbA1c_level_Span).click_and_hold().move_by_offset(x_offset, 0).perform()
        # Release the mouse button
        action_chains.release().perform()
        # Get new value
        input_value = input_hidden.get_attribute('value')
        # print("newvalue:"+input_value)
        prediction_button = driver.find_element(By.ID,"prediction_button")
        time.sleep(2)
        prediction_button.click()
        time.sleep(1)
        prediction_result = driver.find_element(By.ID,"prediction_result")
        self.assertIn("It's crucial to be mindful of the risk of diabetes",prediction_result.text,"Didn't got the risk prompt")
        print("test_prediction_risk passed")
        pass

    def login(self):
        print("start to login system")
        self.driver.get(self.login_url)
        username = self.driver.find_element(By.NAME,"username")
        password = self.driver.find_element(By.NAME,"password")
        username.send_keys("admin")
        password.send_keys("admin")
        time.sleep(1)
        password.send_keys(Keys.RETURN)
        
    def tearDown(self):
        self.driver.close()

from testbook import testbook
import pytest
# testbook test model testcase
@pytest.fixture(scope='module')
def tb():
    with testbook('./diabetes_prediction.ipynb', execute=True) as tb:
        yield tb

# class ModelUnitTest(unittest.TestCase):
def test_dual_coding(tb):
    get_dual_code_test_result = tb.ref("get_dual_code_test_result")
    #"The program should select the best performance one instead of None"
    assert get_dual_code_test_result() is not None
    #"We expected algo is the Random Forest"
    assert get_dual_code_test_result() == "Random_Forest"
    get_max_fscore_result = tb.ref("get_max_fscore_result")
    #"fscore should be greater than 0.85"
    assert get_max_fscore_result() > 0.85
    pass

def test_metamorphic(tb):
    get_metamorphic_test_result = tb.ref("get_metamorphic_test_result")
    #"Metamorphic test passed"
    assert get_metamorphic_test_result() == True
    pass

#Use pytest to integrate all test case, So dispose the html_report
#Command Line:pytest automative_test.py --html=./test_reports/model_and_web_test_report.html
# if __name__ == "__main__":
    # file_path="./test_reports/html_report.html"
    # test_classes_to_run = [PredictionDiabetesTest]
    # suites_list = []
    # loader = unittest.TestLoader()
    # for test_class in test_classes_to_run:
    #     suite = loader.loadTestsFromTestCase(test_class)
    #     suites_list.append(suite)
    # big_suite = unittest.TestSuite(suites_list)
    # runner = HTMLTestRunner(report_filepath=file_path,title='Prediction Diabetes Test report',description='This is a test report for predction diabetes')
    # results = runner.run(big_suite)
    # print(results)