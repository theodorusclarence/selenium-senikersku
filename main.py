from selenium import webdriver
import time


# Main Function
if __name__ == '__main__':

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--log-level=3')

    # Provide the path of chromedriver present on your system.
    driver = webdriver.Chrome(executable_path="chromedriver", options=options)
    driver.set_window_size(1920, 1080)

    # region Sign in
    driver.get('http://localhost:8000/signin')
    driver.find_element_by_id('email').send_keys('theodorusclarence@gmail.com')
    driver.find_element_by_id('password').send_keys('ttT^Nq^9qzVc^Z8E')
    driver.find_element_by_xpath(
        '/html/body/form/div/div[1]/div[5]/div/button').click()
    # endregion

    # Send a get request to the url
    driver.get('http://localhost:8000')

    # Go to Jordan Baru
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/div/div[1]/div[1]/a').click()

    # select size
    driver.find_element_by_xpath(
        '/html/body/div/form/div/div[2]/label').click()

    # Add to cart
    driver.find_element_by_xpath('/html/body/div/form/div/button').click()

    time.sleep(2)
    driver.quit()
    print("Done")
