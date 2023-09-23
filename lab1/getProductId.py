import selenium
from selenium import webdriver as wd
import time
import requests
import csv
import re
import pandas as pd 
from getReview import *
from bs4 import BeautifulSoup as bs

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
}

def getProduct(_id):
    #카테고리,제품명,브랜드,품번,성별,누적판매수,구매후기수,사이즈,총장,어깨너비,가슴단면,소매길이,핏,촉감,계절감,신축성,비침,두꼐,계절,소재,인기구매연령대,셩별
    #컬러옵션,
    #구매자키,몸무게,사이즈 커요, 사이즈 작아요
    product_url = f"https://www.musinsa.com/app/goods/{_id}"
    row = {}
    rows = []
    product_html = requests.get(product_url, headers=headers)
    if product_html.status_code == 200:
        soup = bs(product_html.content, 'html.parser')
        row['category'] = soup.find('p', class_="item_categories").find('a').text
        row['product_title'] = soup.select_one('.product_title > em').get_text()
        product_info_section = soup.find('div', class_='explan_product product_info_section')
        row['brand'] = product_info_section.find('p', class_='product_article_contents').find('a').text
        brand_pattern = re.escape(row['brand']) + r'\s*\/\s*(\S+)'
        row['goodscode'] = re.search(brand_pattern, product_info_section.find('p', class_='product_article_contents').find('strong').text).group(1)
        row['gender'] = product_info_section.find('span', class_='txt_gender').text.strip()
        row['rating'] = product_info_section.find('span', class_='prd-score__rating').text
        review_pattern = r'\d{1,3}(?:,\d{3})*'
        review_matches = re.findall(review_pattern, product_info_section.find('span', class_='prd-score__review-count').text)
        row['reviews_count'] = review_matches[0].replace(',','')
        
        # Extract tags
        tags = product_info_section.find('li', class_='article-tag-list list')
        if tags:
            tag_items = tags.find_all('a', class_='listItem')
            row['Tags'] = [tag.text for tag in tag_items]

        # option -> color

        # material
        row['material'] = soup.select_one(".product_info_table > table tr > td").get_text()
        # size
        product_size = soup.select('table#size_table tbody tr')
        product_size_header_row = soup.select_one('table#size_table thead tr')
        product_size_headers = [header.text.strip() for header in product_size_header_row.find_all('th')]
        for item in product_size[2:]:  # Skip the first two items
            columns = item.find_all('td')
            size_name = item.select_one('th').get_text()
        
            for i, header in enumerate(product_size_headers[1:]):  # Start from the second header
                key = f"{size_name}_{header}"
                value = float(columns[i].text.strip())
                row[key] = value

        # guide
        product_guide = soup.select('.box_material table.table-simple tbody tr')
        for item in product_guide:
            columns = item.find_all('td')
            header = item.find('th').text.strip()
            if len(columns) > 1:
                values = [col.text.strip() for col in columns if "active" in col.get("class", [])]
                row[header] = ",".join(values)



        # # selinium
        driver = wd.Chrome('/usr/local/bin/chromedriver')
        driver.get(product_url)
        sel=driver.page_source
        sel=bs(sel, 'lxml')

        
        view=sel.find_all("strong", {"id":"pageview_1m"})[0].get_text()
        sales=sel.find_all("strong", {"id":"sales_1y_qty"})[0].get_text()
        like=sel.find_all("span", {"class": "prd_like_cnt"})[0].get_text()
        row['views']=view
        row['sales']=sales
        row['like']=like

        #rating
        age_rows = sel.select('.bar_wrap li')
        for item in age_rows:
            age_label = item.select_one('.bar_name').text.strip()
            age_percentage = item.select_one('.bar_num').text.strip()
            row[age_label] = age_percentage

        #Extract column values for 성별 (Gender)
        gender_labels = sel.select('#graph_doughnut_label .label_info_name')
        gender_values = sel.select('#graph_doughnut_label .label_info_value')
        for label, value in zip(gender_labels, gender_values):
            gender_label = label.text.strip()
            gender_percentage = value.text.strip()
            row[gender_label] = gender_percentage

        # per type count
        review_url = "https://goods.musinsa.com/api/goods/v2/review"
        reviewType = sel.find_all('li', class_='btnReviewTypeTab')
        for item in reviewType:
            key = item.get('data-type')
            value = int(item.get('data-review-count'))
            row['review_count'] = value
            row['review_type']=key
            pages = calculate_pagination(value, 10)
            for page in range(1, pages):
                url = f"{review_url}/{key}/list?sort=up_cnt_desc&selectedSimilarNo={_id}&page={page}&goodsNo={_id}"
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    data = response.text
                    reviewData = getReview(data)

                else:
                    print(f"Failed to fetch data for page {page}. Status code: {response.status_code}")

                for review in reviewData:
                    tmp = review | row
                    rows.append(tmp)
 
                df=pd.json_normalize(rows)
                save_to_csv(df,"musinsa.csv")
                print(f"complete to save that product_id:{_id} save:{page} url:{url} rows:{len(rows)}")
        driver.close()



    # for key, value in row.items():
        # print(f"{key}: {value}")
        # price = product.find(class_="price").text.strip()
        # id = product.find(class_='member_price').get('id').split('_')[-1]
        # img = product.find('img').get('data-original')

        # product_url = product.find(class_='list_info').find('a').get('href')
        # # product_seller_url = product.find(class_='item_title').find('a').get('href')

        # # Create a list to store the cells of each row
        # # row = [img, title, info, price, product_seller_url, product_url]
        # row = [img, title, info, price, product_url]
        # reivew_list_url = f'https://goods.musinsa.com/api/goods/v2/review/style/list?similarNo=3200524&sort=new&selectedSimilarNo={id}&page=1&goodsNo={id}'
        # review_html = requests.get(reivew_list_url, headers=headers)
        # review_soup = bs(review_html.content, 'html.parser')

        # reviews = []
        # for review in review_soup.find_all(class_='review-contents__text'):
        #     reviews.append(review.text.strip())

        # # Add the reviews as a string to the row
        # row.append("<br/> - ".join(reviews))
        # # Append the row to the table_rows list
        # table_rows.append(row)
   
    # return rows;

def save_to_csv(df, csvFilePath, sep=",", encoding='utf-8-sig'):
    import os
    if not os.path.isfile(csvFilePath):
        df.to_csv(csvFilePath, mode='a', index=False, sep=sep)
    elif len(df.columns) != len(pd.read_csv(csvFilePath, nrows=1, sep=sep).columns):
        raise Exception("Columns do not match!! Dataframe has " + str(len(df.columns)) + " columns. CSV file has " + str(len(pd.read_csv(csvFilePath, nrows=1, sep=sep).columns)) + " columns.")
    elif not (df.columns == pd.read_csv(csvFilePath, nrows=1, sep=sep).columns).all():
        raise Exception("Columns and column order of dataframe and csv file do not match!!")
    else:
        df.to_csv(csvFilePath, mode='a', index=False, sep=sep, header=False)

def getTotalPage(): 
    product_list_url = f'https://www.musinsa.com/categories/item/001?d_ct_cd=001&brand=&list_kind=small&sort=sale_high&sub_sort=1y&page=1&display_cnt=90&group_sale=&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&plusDeliveryYn=&kids=&color=&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure='
    product_html = requests.get(product_list_url, headers=headers)
    product_soup = bs(product_html.content, 'html.parser')
    total_page = product_soup.find(class_='totalPagingNum').text
    return int(total_page)

def getAllProduct(_page_number):
    product_list_url = f'https://www.musinsa.com/categories/item/001?d_ct_cd=001&brand=&list_kind=small&sort=sale_high&sub_sort=1y&page={_page_number}&display_cnt=90&group_sale=&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&plusDeliveryYn=&kids=&color=&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure='
    product_html = requests.get(product_list_url, headers=headers)
    product_soup = bs(product_html.content, 'html.parser')
    product_list = product_soup.find(class_="snap-article-list boxed-article-list article-list center list goods_small_media8")
    product_id = []
    total_page = product_soup.find(class_='totalPagingNum')

    for product in product_list.find_all(class_="li_box"):
        id = product.find(class_="list_info").find('a').get('href').split('/')[5]
        getProduct(id)

    return product_id

def sizing_map (df_col) :
    SIZE_LABEL_MAP = {
        # 1. FREE SIZE
        "옵션없음": "FREE",
        "SIZE": "FREE",
        "단품": "FREE"
    } 
    df_col = df_col.replace(SIZE_LABEL_MAP)
    return df_col


if __name__ == "__main__":
    total_page = getTotalPage()
    if(total_page > 400):
        total_page = 400
    for i in range(total_page):
        print(getAllProduct(i))

    # for page_number in range(1, total_page + 1):

        # save_csv(getAllProduct(page_number), output)

    # product_id = []
    # api_url = "https://api.zigzag.kr/api/2/graphql/GetProductReviewList"
    # total = 71321
    # output = 'transformed_data.csv'
    # total = 100
    # per = 999
    # count = total % per
    # if count == 0:
    #   call_count = total / per
    # else:
    #   call_count = math.trunc(total / per) + 1

    # print("amount of apoch %d, per %d" %(call_count, per))
    # result = []
    # for i in range(0,int(call_count)):
    #   skip = per*i
    #   payload = {
    #     "query": "query GetProductReviewList( $product_id: ID $limit_count: Int $skip_count: Int $has_attachment: Boolean $order: ProductReviewListOrderType ) { product_review_list( product_id: $product_id limit_count: $limit_count skip_count: $skip_count has_attachment: $has_attachment order: $order ) { total_count item_list { id status contents date_created date_updated rating product_type country country_name attachment_list { type original_url thumbnail_url status } attribute_list { question { label value category } answer { label value } } reviewer { masked_email body_text } order_item { product_info { options option_detail_list { name value } } } } } }",
    #     "variables": {
    #       "order": "BEST_SCORE_DESC",
    #       "limit_count": per,
    #       "product_id": "113041967",
    #       "skip_count": skip
    #     }
    #   }

    #   json_data = get_json_from_api(api_url, payload, int(i))
    #   save_csv(json_data, output)
    #   time.sleep(10)

# for page_number in range(1, 20):
    # Construct the URL for the current page
    # url = product_luist_url.format(page_number)
    # print(url)
    # # Send a GET request to the URL
    # response = requests.get(url)

    # if response.status_code == 200:
    #     # Parse the HTML content of the page
    #     soup = bs(response.content, 'html.parser')

    #     # Extract item_ids (You will need to inspect the HTML structure to get the correct selector)
    #     item_id_elements = soup.select('your_selector_here')

    #     # Extract and print item_ids
    #     for item_id_element in item_id_elements:
    #         item_id = item_id_element.get('data-item-id')
    #         if item_id:
    #             print("Item ID:", item_id)
    # else:
    #     print(f"Failed to fetch page {page_number}. Status code: {response.status_code}")

# You may want to add some delay between requests to avoid overloading the server
# time.sleep(1)  # Uncomment this line if needed
# 