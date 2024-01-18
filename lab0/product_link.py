import driver_setting
from selenium.webdriver.common.by import By
import time

brand_name = ["apoc", "romanticcrown", "mahagrid", "luvistrue", "lee"]
brand_code = ['AP', 'RO', 'MA', 'LU', 'LE']
cloth_type = {"001": ["001001","001010","001011","001002","001003", "001005", "001004", "001006", "001008"],
 "003": ["003002","003007","003008", "003004", "003009", "003006"],
  "022": ["022001", "022002", "022003"]}

cloth_type_link_list = [] # categoryCode
cloth_link_list = [] # product_link (상품 상세 페이지 링크)


def driver_get_product_links():
    for i in range(len(brand_name)):
        for cloth in cloth_type.keys():
            for j in range(len(cloth_type[cloth])):
                count=0 # 상품 개수
                driver1.get("https://www.musinsa.com/brands/"+brand_name[i]+"?category1DepthCode="+cloth+"&category2DepthCodes="+cloth_type[cloth][j]+"&category3DepthCodes=&colorCodes=&startPrice=&endPrice=&exclusiveYn=&includeSoldOut=&timeSale=&includeKeywords=&saleGoods=&groupSale=&sortCode=1y&tags=&page=1&size=60&campaignCode=&listViewType=small&outletGoods=false&boutiqueGoods=")
                products = driver1.find_elements(By.CSS_SELECTOR, "#listProducts")
                for product in products:
                    if count>2:
                        break
                    count += 1
                    cloth_type_link_list.append(brand_code[i]+cloth_type[cloth][j])
                    cloth_link_list.append(product.find_element(By.CSS_SELECTOR, "li:nth-child(1) > div.brandshop-product__thumbnail > figure > a").get_attribute("href"))
            
driver1 = driver_setting.driver_setting_iphone() # 드라이버 세팅

driver_get_product_links()

print("--------------------------")
print(cloth_link_list)
print("--------------------------")
print(cloth_type_link_list)
print("--------------------------")
print(len(cloth_type_link_list), len(cloth_link_list))
print("--------------------------")

