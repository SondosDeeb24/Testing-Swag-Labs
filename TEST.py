import unittest
import random
from selenium import webdriver
import webbrowser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import HtmlTestRunner
import os 

class AutoTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get("https://www.saucedemo.com/")

    def login(self):
        print("🔐 Logging in...")
        self.driver.find_element(By.ID, "user-name").send_keys("standard_user")
        self.driver.find_element(By.ID, "password").send_keys("secret_sauce")
        self.driver.find_element(By.ID, "login-button").click()
        self.wait.until(EC.url_contains("inventory"))
        print("✅ Logged in successfully")

    def select_random_product(self):
        print("🛒 Selecting a random product...")
        products = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
        self.assertGreater(len(products), 0, "No products found on the page")
        product = random.choice(products)
        name = product.find_element(By.CLASS_NAME, "inventory_item_name").text
        product.find_element(By.TAG_NAME, "button").click()
        print(f"✅ Added product: {name}")
        return name

    def test_login_and_add_to_cart(self):
        print("\n=== Test: Login and Add to Cart ===")
        self.login()
        product_name = self.select_random_product()
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

        # Validate product is in the cart
        cart_items = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        names = [item.text for item in cart_items]
        self.assertIn(product_name, names)
        print("✅ Product correctly added to cart")

    def test_checkout_validation(self):
        print("\n=== Test: Checkout Form Validation ===")
        self.login()
        self.select_random_product()
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        self.driver.find_element(By.ID, "checkout").click()

        # Wait for checkout form fields to appear
        self.wait.until(EC.presence_of_element_located((By.ID, "first-name")))
        self.wait.until(EC.presence_of_element_located((By.ID, "last-name")))
        self.wait.until(EC.presence_of_element_located((By.ID, "postal-code")))

        # Submit empty form
        self.driver.find_element(By.ID, "continue").click()

        try:
            error = self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "[data-test='error']"))).text
            self.assertIn("First Name is required", error)
            print("✅ Proper error displayed for empty form")
        except TimeoutException:
            self.fail("❌ Error message did not appear after submitting empty checkout form")

        # Fill out form correctly and continue
        self.driver.find_element(By.ID, "first-name").send_keys("Jane")
        self.driver.find_element(By.ID, "last-name").send_keys("Doe")
        self.driver.find_element(By.ID, "postal-code").send_keys("12345")
        self.driver.find_element(By.ID, "continue").click()

        try:
            self.wait.until(EC.url_contains("checkout-step-two"))
            print("✅ Proceeded to checkout step two")
        except TimeoutException:
            self.fail("❌ Failed to navigate to checkout-step-two after submitting valid data")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(AutoTest)
    runner = HtmlTestRunner.HTMLTestRunner(output="report")
    result = runner.run(suite)
