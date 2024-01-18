from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pymysql
import data_product
import driver_setting

productCode = data_product.code
links = data_product.links

driver1 = driver_setting.driver_setting_iphone()

db = pymysql.connect(
    user='root',
    passwd='duksung',
    host='localhost',
    port=3306,
    db='navatar',
    charset='utf8'
)

cursor = db.cursor()

# productNo, name, mainImage, normalPrice, salePrice, ARFitting, categoryCode

for i in range(0, len(links)):
    driver1.get(links[i])
    productNo = i+1
    name = driver1.find_element(By.CSS_SELECTOR, "#product_order_info > h2").text # 상품명
    normalPrice = driver1.find_element(By.CSS_SELECTOR, "#normal_price").get_attribute("innerHTML") # 가격
    mainImage = driver1.find_element(By.CSS_SELECTOR, "#bigimg_0").get_attribute("src") # 대표 이미지
    sql = "INSERT INTO Product VALUES("+str(productNo)+", '"+name+"', '"+mainImage+"', "+normalPrice+", null, 1, '"+productCode[i]+");"
    cursor.execute(sql)

db.commit()
db.close()