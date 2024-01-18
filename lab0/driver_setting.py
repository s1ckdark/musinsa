from selenium import webdriver
# from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def driver_setting_iphone():
    mobileEmulation = {"deviceName" : "iPhone X"}
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("mobileEmulation", mobileEmulation)
    return webdriver.Chrome(ChromeDriverManager().install(), options=chromeOptions)

def driver_setting():
    return webdriver.Chrome(ChromeDriverManager().install())