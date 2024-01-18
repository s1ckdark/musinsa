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


# 상세 이미지    

for i in range(0, len(links)):
    driver1.get(links[i])
    productNo = i+1
    details = driver1.find_element(By.CSS_SELECTOR, "#contentProductDetail").find_elements(By.CLASS_NAME, "lazyload") # 상세 이미지 위치
    j=0
    for detail in details:
        j += 1
        driver1.execute_script('arguments[0].scrollIntoView(true);', detail)
        time.sleep(5)
        detail_src = detail.get_attribute("src") # 상세 이미지 
        sql = "INSERT INTO ProductDetail VALUES("+str(productNo)+", '"+detail_src+"', "+str(j)+");"
        cursor.execute(sql)

db.commit()
db.close()