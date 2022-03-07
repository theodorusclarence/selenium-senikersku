import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


class Cart(unittest.TestCase):
    def setUp(self):
        # create a chrome session
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument('--log-level=3')

        self.driver = webdriver.Chrome(
            executable_path="chromedriver", options=options)
        self.driver.maximize_window()
        self.driver.get("http://localhost:8000/")
        self.printSetup("Setup Testing ...")

    def printSuccess(self, word):
        print('\x1b[6;30;42m' + word + '\x1b[0m')

    def printSetup(self, word):
        print('\x1b[6;30;43m' + word + '\x1b[0m')

    def printError(self, word):
        print('\x1b[6;30;41m' + word + '\x1b[0m')

    def findElement(self, xpath, elementName="Element", errorMsg="The element is not found"):
        self.driver.find_element(By.XPATH, xpath)

    def assertElement(self, xpath, elementName="Element", errorMsg="The element is not found"):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            self.printSuccess(elementName + " element found ...")
            return self.driver.find_element(By.XPATH, xpath)
        except:
            self.printError(errorMsg)
            self.driver.close()

    def resetState(self):
        # Remove Item to Reset
        removeButton = self.driver.find_element(
            By.CSS_SELECTOR, '.w-5')
        removeButton.submit()

    def signin(self):
        # clear cookies
        self.driver.delete_all_cookies()

        # go to sign in page
        self.driver.get("http://localhost:8000/signin")

        # fill email input
        inputEmail = self.driver.find_element(By.XPATH, '//*[@id="email"]')
        inputEmail.send_keys("frank@gmail.com")

        # fill password input
        inputPassword = self.driver.find_element(
            By.XPATH, '//*[@id="password"]')
        inputPassword.send_keys("password")

        # sign in
        signInBtn = self.driver.find_element(
            By.XPATH, '/html/body/form/div/div[1]/div[5]/div/button')
        signInBtn.click()

        # go to landing page
        self.driver.get("http://localhost:8000")

    def test_2_add_to_cart(self):
        self.printSetup("Sign in ...")
        self.signin()

        self.printSetup("Adding a new item to the cart...")
        # go to Jordan Baru
        self.driver.get('http://localhost:8000/detailbarang/1')

        self.driver.find_element(By.CSS_SELECTOR, ".p-4").click()

        # Add to cart
        self.driver.find_element(By.CSS_SELECTOR, ".rounded-full").click()

        itemName = self.driver.find_element(
            By.XPATH, '/html/body/div[2]/div[1]/div/div/ul/li[2]')
        print(itemName.text)
        self.assertEqual(itemName.text, "Jordan baru")

    def test_3_add_amount(self):
        self.printSetup("Adding amount of item in the cart...")
        self.signin()

        self.driver.get('http://localhost:8000/cart')

        self.driver.find_element(
            By.CSS_SELECTOR, 'form > .px-2').click()

        amount = self.driver.find_element(
            By.ID, 'amount0')
        self.assertEqual(amount.text, "2")

    def test_4_min_amount(self):
        self.printSetup("Removing amount of item in the cart...")
        self.signin()

        self.driver.get('http://localhost:8000/cart')

        self.driver.find_element(
            By.CSS_SELECTOR, '.px-2\.5:nth-child(3)').click()

        amount = self.driver.find_element(
            By.ID, 'amount0')
        self.assertEqual(amount.text, "1")

    def test_5_min_amount_to_0_should_remove_them(self):
        self.printSetup("Removing amount of item in the cart...")
        self.signin()

        self.driver.get('http://localhost:8000/cart')

        self.driver.find_element(
            By.CSS_SELECTOR, '.px-2\.5:nth-child(3)').click()

        itemName = self.driver.find_element(
            By.XPATH, '/html/body/div[2]/div[1]/div/div/ul/li[2]')

        self.assertNotEqual(itemName.text, "Jordan baru")

        self.resetState()

    def tearDown(self):
        self.printSetup("Closing Testing ...")
        # time.sleep(5)

        self.driver.close()


if __name__ == "__main__":
    unittest.main()
