# ## =============================================================================================================================
# ##? Importing the needed libraries and modules; 
# ## =============================================================================================================================
import unittest # to create and run unit test

from selenium import webdriver ## create chrome browser instance to control aumated testing
from selenium.webdriver.common.by import By ## help to find element

import HtmlTestRunner ## to generate report for the test
from selenium.common.exceptions import NoSuchElementException


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

    ## ===========================================================================================================================
    #? Test 4 = Logout Functionality
    ## ============================================================================================================================
    def test_logout_functionality(self):
        driver = self.driver

        # 1 - Login
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

         # 2 - Open the menu
        driver.find_element(By.ID, "react-burger-menu-btn").click()

        # 3 - Click the logout link
        driver.implicitly_wait(2)  # Give time for the menu animation
        driver.find_element(By.ID, "logout_sidebar_link").click()

        # 4 - Verify that we are back on the login page
        self.assertIn("saucedemo", driver.current_url)
        self.assertTrue(driver.find_element(By.ID, "login-button").is_displayed())

    ## ===========================================================================================================================
    #? Test 5 = Direct URL access to inventory without login
    ## ============================================================================================================================
    def test_direct_access_to_inventory_without_login(self):
        driver = self.driver

         # Try to access the protected inventory page directly
        driver.get("https://www.saucedemo.com/inventory.html")

        # Check if redirected to login page
        current_url = driver.current_url
        self.assertIn("saucedemo.com", current_url)
        self.assertTrue("inventory" not in current_url)
        self.assertTrue(driver.find_element(By.ID, "login-button").is_displayed())

   
    ## ===========================================================================================================================
    #? Test 6 = Sorting Items by Price(Low to High)
    ## ============================================================================================================================
    def test_sort_items_by_price_low_to_high(self):
       driver = self.driver

        # 1 - Login
       driver.find_element(By.ID, "user-name").send_keys("standard_user")
       driver.find_element(By.ID, "password").send_keys("secret_sauce")
       driver.find_element(By.ID, "login-button").click()

       # 2 - Select 'Price (low to high)' from the dropdown
       sort_dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
       sort_dropdown.click()
       sort_dropdown.find_element(By.CSS_SELECTOR, "option[value='lohi']").click()

       # 3 - Get all prices, convert them to float, and check sort order
       prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
       price_values = [float(price.text.replace("$", "")) for price in prices]

       self.assertEqual(price_values, sorted(price_values))


    # ## ===========================================================================================================================
    #? Test 7 = Sorting Items by Price (High to Low)
    # ## ===========================================================================================================================
    def test_sort_items_by_price_high_to_low(self):
        driver = self.driver

        # 1 - Login
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # 2 - Select 'Price (high to low)' from the dropdown
        sort_dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
        sort_dropdown.click()
        sort_dropdown.find_element(By.CSS_SELECTOR, "option[value='hilo']").click()

        # 3 - Get all prices, convert to float, and check sort order
        prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        price_values = [float(price.text.replace("$", "")) for price in prices]

        self.assertEqual(price_values, sorted(price_values, reverse=True))

    # ## ===========================================================================================================================
    #? Test 8 = Sorting Items by Name (A to Z)
    # ## ===========================================================================================================================
    def test_sort_items_by_name_a_to_z(self):
        driver = self.driver

        # 1 - Login
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # 2 - Select 'Name (A to Z)' from the dropdown
        sort_dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
        sort_dropdown.click()
        sort_dropdown.find_element(By.CSS_SELECTOR, "option[value='az']").click()

        # 3 - Get all product names and check alphabetical order
        product_names = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        name_list = [name.text for name in product_names]

        self.assertEqual(name_list, sorted(name_list))

    # ## ===========================================================================================================================
    #? Test 9= Sorting Items by Name (Z to A)
    # ## ===========================================================================================================================
    def test_sort_items_by_name_z_to_a(self):
        driver = self.driver

        # 1 - Login
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # 2 - Select 'Name (Z to A)' from the dropdown
        sort_dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
        sort_dropdown.click()
        sort_dropdown.find_element(By.CSS_SELECTOR, "option[value='za']").click()

        # 3 - Get all product names and check reverse alphabetical order
        product_names = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        name_list = [name.text for name in product_names]

        self.assertEqual(name_list, sorted(name_list, reverse=True))
    ## ===========================================================================================================================
    #? Test 10 = Remove Item from Cart
    ## ===========================================================================================================================
    def test_remove_item_from_cart(self):
        driver = self.driver

        # 1 - Login
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # 2 - Add item to cart
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

        # 3 - Navigate to cart
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

        # 4 - Remove item from cart
        driver.find_element(By.ID, "remove-sauce-labs-backpack").click()

        # 5 - Verify cart is empty
        try:
            cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
            self.fail("Cart badge should not exist after removing item.")
        except NoSuchElementException:
            pass  # No cart badge means cart is empty, test passes
    ## ===========================================================================================================================
    #? Test 11 = Cancel Checkout
    ## ===========================================================================================================================
    def test_cancel_checkout(self):
        driver = self.driver

        # 1 - Login
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # 2 - Add item to cart
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

        # 3 - Navigate to cart
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

        # 4 - Proceed to checkout
        driver.find_element(By.ID, "checkout").click()

        # 5 - Cancel checkout
        driver.find_element(By.ID, "cancel").click()

        # 6 - Verify return to cart page
        self.assertIn("cart.html", driver.current_url)   
    ## ===========================================================================================================================
    #? Test 12 = Add Multiple Items to Cart
    ## ===========================================================================================================================
    def test_add_multiple_items_to_cart(self):
        driver = self.driver

        # 1 - Login
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # 2 - Add first item to cart (Sauce Labs Backpack)
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

        # 3 - Add second item to cart (Sauce Labs Bike Light)
        driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()

        # 4 - Verify cart badge shows '2'
        cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        self.assertEqual(cart_badge, "2")

    ## ===========================================================================================================================
    #? Test 13 = Testing social media urls in the inventory main page
    ## ============================================================================================================================
    def test_social_media_links(self):
        driver = self.driver

        # 1- login 
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # 2 -  validate that every social media link matches the url the user is expecting
        twitter_button = driver.find_element(By.CSS_SELECTOR, "[data-test='social-twitter']")
        assert twitter_button.get_attribute("href") == "https://twitter.com/saucelabs"
        
        facebook_button = driver.find_element(By.CSS_SELECTOR, "[data-test='social-facebook']")
        assert facebook_button.get_attribute("href") == "https://www.facebook.com/saucelabs"

        linkedin_button = driver.find_element(By.CSS_SELECTOR, "[data-test='social-linkedin']")
        assert linkedin_button.get_attribute("href") == "https://www.linkedin.com/company/sauce-labs/"


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
