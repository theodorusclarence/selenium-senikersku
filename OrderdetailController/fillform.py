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
        # self.driver.maximize_window()
        self.driver.get("http://localhost:8000/")
        self.printSetup("Setup Testing ...")
        # declare input fields with correct value 
        self.inputFields = {
            "name_input" :{
                "xpath" : '//*[@id="name"]',
                "value" : "Michael Alexander"
            },
            "email_input" :{
                "xpath" : '//*[@id="email"]',
                "value" : "alex@gmail.com"
            },
            "phone_input" :{
                "xpath" : '//*[@id="no_telp"]',
                "value" : "081234567891"
            },
            "address_input" :{
                "xpath" : '//*[@id="alamat"]',
                "value" : "Jl Angkasa 5"
            },
            "postalCode_input" :{
                "xpath" : '//*[@id="kode_pos"]',
                "value" : "60111"
            },
        }

    
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

    def  goToCheckoutForm(self):
        # select one item on landing page 
        shoes = self.findElement('//*[@id="slider-3"]/div/div[1]/div[1]/a', 'Shoes', 'There are no Shoes found')
        shoes.click()

        # select size and checkout
        self.findElement('//*[@id="radio_0"]', "Size input", "There are no size input found")
        label = self.driver.find_element_by_xpath('/html/body/div/form/div/div[2]/label')
        label.click()
        
        submitBtn = self.findElement('/html/body/div/form/div/button', "Checkout button", "Checkout button found")
        submitBtn.click()

        # go to checkout form 
        checkoutBtn = self.findElement('/html/body/div[2]/div[2]/div/div/div[3]/form/button', "Go to Checkout button", "Go to Checkout button found")
        checkoutBtn.click()

    def fillInputCheckoutForm(self, inputs):
        for input_field in inputs:
            boxInput = self.findElement(inputs[input_field]["xpath"])
            boxInput.send_keys(inputs[input_field]["value"])

    def checkValueField(self, inputs, field, value, errorMsg):
        tempInputs = copy.deepcopy(inputs)
        tempInputs[field]["value"] = value
        self.fillInputCheckoutForm(tempInputs)
        
        orderBtn = self.findElement("/html/body/div[2]/div[2]/div/form/ul/div[2]/button")
        orderBtn.click()
        self.assertFalse("payment" in self.driver.current_url, '\x1b[6;30;41m' + errorMsg + '\x1b[0m')

    def navigate_checkout_form(self):
        print("")
        self.printSetup("Sign in process ...")
        self.signin()

        print("")
        self.printSetup("Go to checkout form ...")
        self.goToCheckoutForm()

        print("")
        self.printSetup("Testing checkout form ...")

    def test_empty_value(self):
        # navigating to checkout form 
        self.navigate_checkout_form()

        # test if there is empty value
        self.printSetup("Test empty value")
        for input_field in self.inputFields:
            self.checkValueField(self.inputFields, input_field, "", "Test empty field failed")

        assert True

    def test_name_value(self):
        # navigating to checkout form 
        self.navigate_checkout_form()

        # test field with forbidden value
        print("")
        self.printSetup("Test name value")
        self.checkValueField(self.inputFields, "name_input", "&864", "Test name field failed : input can contain symbols and number")
        assert True

    def test_email_value(self):
        # navigating to checkout form 
        self.navigate_checkout_form()

        # test field with forbidden value
        print("")
        self.printSetup("Test email value")
        self.checkValueField(self.inputFields, "email_input", "Erki Kadhafi", "Test email field failed : input can contain not valid email format")
        assert True

    def test_phone_value(self):
        # navigating to checkout form 
        self.navigate_checkout_form()

        # test field with forbidden value
        print("")
        self.printSetup("Test phone value")
        self.checkValueField(self.inputFields, "phone_input", "qwertyuiop&87q2", "Test phone field failed : input can non numeric value")
        assert True
        
    def test_postalCode_value(self):
        # navigating to checkout form 
        self.navigate_checkout_form()

        # test field with forbidden value
        print("")
        self.printSetup("Test postalCode value")
        self.checkValueField(self.inputFields, "postalCode_input", "askasc@!@!234", "Test postalCode field failed : input can contain non numeric value")
        assert True

    def tearDown(self):
        self.printSetup("Closing Testing ...")
        time.sleep(5)
        self.driver.close()

if __name__ == "__main__":
    unittest.main()