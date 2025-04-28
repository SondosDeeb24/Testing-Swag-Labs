# ## =============================================================================================================================
# ##? Importing the needed libraries and modules
# ## =============================================================================================================================
import unittest # to create and run unit test
from selenium import webdriver ## create chrome browser instance to control aumated testing
from selenium.webdriver.common.by import By ## help to find element

import HtmlTestRunner ## to generate report for the test


# ## =============================================================================================================================
# ##? Class to test login functionality 
# ## =============================================================================================================================

class Test_SwagLab(unittest.TestCase):

    ## ===========================================================================================================================
    # This method runs before each test
    ## ============================================================================================================================
    def setUp(self):
        self.driver = webdriver.Chrome() ## this line open new browser chrome
        self.driver.get("https://www.saucedemo.com/")
        self.driver.maximize_window() ## let the window to be full-screen size

    ## ===========================================================================================================================
    #? Test 1 = login using valid credential 
    ## ============================================================================================================================
    def test_valid_login(self):
        driver = self.driver
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        # check if the was able to get it, by checking the url (if it contain "invetory" it means we are in the systerm )
        self.assertIn("inventory", driver.current_url)

    ## ===========================================================================================================================
    #? Test 2 = login using invalid credential 
    ## ============================================================================================================================
    def test_invalid_login(self):
        driver = self.driver
        driver.find_element(By.ID, "user-name").send_keys("wrong_user")
        driver.find_element(By.ID, "password").send_keys("wrong_pass")
        driver.find_element(By.ID, "login-button").click()
        
        error_message = driver.find_element(By.CSS_SELECTOR, 'h3[data-test="error"]').text ## find the error message
        self.assertIn("Epic sadface", error_message)  ## check if the error message contain "Epic sadface" word
    
    


    ## ===========================================================================================================================
    #? Test 3 = Add one item to cart after login
    ## ============================================================================================================================
    def test_add_item_to_cart(self):
        driver = self.driver

        # 1- login 
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()


        # 2- click on "Add to cart" for one product
        add_to_cart_button = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
        add_to_cart_button.click()

        # 3-  verify the cart icon shows '1' item
        cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        self.assertEqual(cart_badge, "1")


    ## ============================================================================================================================
    # This method runs after each test to close the browser 
    ## ============================================================================================================================
    def tearDown(self):
        self.driver.quit()

## ============================================================================================================================
if __name__ == "__main__":
    runner = HtmlTestRunner.HTMLTestRunner( ## create html test report 
        output='reports',
        open_in_browser=True,
        report_name = "Test_Report_for_Swag_Lab"
    )
    # run the test
    unittest.main(testRunner=runner)