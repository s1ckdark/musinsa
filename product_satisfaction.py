from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pymysql
import data_product

links = data_product.links
satisfaction_list = {'"작음"':1,  '"큼"':2, '"적당함"':3}
mobileEmulation = {"deviceName" : "iPhone X"}
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("mobileEmulation", mobileEmulation)

driver1 = webdriver.Chrome(options=chromeOptions)

# 팝업 체크 함수
def popup(str):
    print(str)
    popu = driver1.find_element(By.CSS_SELECTOR, str)
    if popu:
        popu.click()

db = pymysql.connect(
    user='root',
    passwd='duksung',
    host='localhost',
    port=3306,
    db='navatar',
    charset='utf8'
)

cursor = db.cursor()

pk = 6488

# 팝업 체크
# #apoc
# driver1.get(links[0])
# time.sleep(0.5)
# popup("#divpop_goods_apoc_7725 > form > button.btn.btn-today")

# #roman
# driver1.get(links[46])
# time.sleep(0.5)
# popup("#divpop_goods_romanticcrown_7995 > form > button.btn.btn-today")

# #lee
# driver1.get(links[217])
# time.sleep(0.5)
# popup("#divpop_goods_lee_8138 > form > button.btn.btn-today")

# #luv
# driver1.get(links[163])
# time.sleep(0.5)
# popup("#divpop_goods_luvistrue_7845 > form > button.btn.btn-today")

driver1.get(links[4])
time.sleep(0.3)

for i in range(0, len(links)):
    try:
        driver1.get(links[i])
        productNo = i+1

        # 만족도 부분으로 이동
        time.sleep(1)
        detail = driver1.find_element(By.CSS_SELECTOR, "#contentProductDetail").find_element(By.CLASS_NAME, "lazyload") # 상세 이미지 위치
        driver1.execute_script('arguments[0].scrollIntoView(true);', detail)
        time.sleep(0.5)
        driver1.find_element(By.CSS_SELECTOR, "#floating-detail-tab > button:nth-child(2)").click()
        time.sleep(1.5)
        driver1.find_element(By.CSS_SELECTOR,"#tab_size_recommend").click() 
        lis = driver1.find_elements(By.CSS_SELECTOR, "#recommend-comment-list > li")

        #만족도
        # pk, Product_productNo, weight, height, satisfaction, size
        for li in lis:
            pk += 1
            hw = li.find_element(By.CSS_SELECTOR, "div:nth-child(1) > p").text.split("\n • \n")
            height = int(hw[1][:-2])
            weight = int(hw[2][:-2])
            s = li.find_element(By.CSS_SELECTOR, "div:nth-child(2) > ul > li > span").text
            satisfaction = satisfaction_list[s]
            size = li.find_element(By.CSS_SELECTOR, "div:nth-child(1) > h4").text
            sql = "INSERT INTO Satisfaction VALUES("+str(pk)+", "+str(productNo)+", "+str(weight)+", "+str(height)+", "+str(satisfaction)+", '"+size[:9]+"', NULL, NULL);"
            
            cursor.execute(sql)
    except:
        print(i+", except") # 리뷰 없는 제품
        continue

db.commit()
db.close()