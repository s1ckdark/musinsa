from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pymysql
import data_product
import driver_setting
links = data_product.links
satis = {'"작음"':1, '"적당함"':2, '"큼"':3}

driver1 = driver_setting.driver_setting()

db = pymysql.connect(
    user='root',
    passwd='duksung',
    host='localhost',
    port=3306,
    db='navatar',
    charset='utf8'
)

cursor = db.cursor()
pk = 0
for i in range(0, len(links)):
    driver1.get(links[i])
    productNo = i+i
    time.sleep(0.3)
    sizes = driver1.find_elements(By.CSS_SELECTOR, "#size_table > tbody > tr")
    for i in range(3, len(sizes)+1):
        size = driver1.find_element(By.CSS_SELECTOR, "#size_table > tbody > tr:nth-child("+str(i)+") > th").text
        print("size"+size)
        sql = "INSERT INTO ProductSize VALUES("+str(productNo)+", '"+size+"');"
        cursor.execute(sql)

db.commit()
db.close()