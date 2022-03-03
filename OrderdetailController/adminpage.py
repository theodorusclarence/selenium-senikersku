import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import copy

class FillFormCheckout(unittest.TestCase):
    def setUp(self):
        #create a chrome session
        self.driver = webdriver.Chrome("./OrderDetailController/chromedriver.exe")
        self.driver.maximize_window()
        self.driver.get("http://localhost:8000/")
        self.printSetup("Setup Testing ...")
    
    def printSuccess(self, word):
        print('\x1b[6;30;42m' + word + '\x1b[0m')
    
    def printSetup(self, word):
        print('\x1b[6;30;43m' + word + '\x1b[0m')
    
    def printError(self, word):
        print('\x1b[6;30;41m' + word + '\x1b[0m')
    
    def findElement(self, xpath, elementName = "Element", errorMsg = "The element is not found"):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            self.printSuccess(elementName + " element found ...")
            return self.driver.find_element_by_xpath(xpath)
        except:
            self.printError(errorMsg)
            self.driver.close()

    def signin(self):
        #go to sign in page
        self.driver.get("http://localhost:8000/signin")

        # fill email input 
        inputEmail = self.findElement('//*[@id="email"]', 'Input email', 'There are no input email found')
        inputEmail.send_keys("frank@gmail.com")

        # fill password input 
        inputPassword = self.findElement('//*[@id="password"]', 'Input password', 'There are no input password found')
        inputPassword.send_keys("password")

        # sign in 
        signInBtn = self.findElement('/html/body/form/div/div[1]/div[5]/div/button', 'SignIn Button', 'There are no SignIn Button found')
        signInBtn.click()

        #go to landing page
        self.driver.get("http://localhost:8000")

    def test_1_access_without_signin(self):
        # check if we can access admin page without proper permission for admin
        self.driver.get("http://localhost:8000/admin")
        self.assertFalse("Admin" in self.driver.page_source, '\x1b[6;30;41m' + "Error : can access admin page without login" + '\x1b[0m')
    
    def test_2_access_with_regular_account(self):
        # sign in regular account
        print("")
        self.printSetup("Sign in process ...")
        self.signin()

        # check if we can access admin page without proper permission for admin
        self.driver.get("http://localhost:8000/admin")
        self.assertFalse("Admin" in self.driver.page_source, '\x1b[6;30;41m' + "Error : can access admin page without admin account" + '\x1b[0m')

    def tearDown(self):
        self.printSetup("Closing Testing ...")
        # time.sleep(5)
        self.driver.close()

if __name__ == "__main__":
    unittest.main()