import requests
from bs4 import BeautifulSoup

def getReview(html_data):
    soup = BeautifulSoup(html_data, 'html.parser')
    # Extract the reviewer spec
    result = []
    reviewers = soup.select('.review-list')
    for i in range(0, len(reviewers)):
        if(reviewers[i].select_one('.review-profile__body_information')):
            review_spec = reviewers[i].select_one('.review-profile__body_information').get_text()
            split_review_spec = review_spec.split(' · ')
            if(len(split_review_spec) == 3):
                review_gender = split_review_spec[0]
                review_height = split_review_spec[1]
                review_weight = split_review_spec[2]
            else:
                review_gender = None
                review_height = None
                review_weight = None
        else:
            review_gender = None
            review_height = None
            review_weight = None
        review_text = reviewers[i].select_one('.review-contents__text').text.strip()
        review_rating = int(reviewers[i].select_one('.review-list__rating__active')['style'].split(':')[1].replace('%','').strip())

        # reviewer image        
        # if(reviewers[i].select_one('.review-content-photo__item img')):
        #     review_image_url = reviewers[i].select_one('.review-content-photo__item img')['src']
        # else:
        #     review_image_url = None

        tmp = {
            'review_gender':review_gender,
            'review_height':review_height,
            'review_weight':review_weight,
            'review_text':review_text,
            'review_rating':review_rating,
            # 'review_image_url':review_image_url
        }
        result.append(tmp)
    return result

def calculate_pagination(total_item, item_per_page):
    if(total_item <= 0):
        return None
    tmp = total_item % item_per_page

    if(tmp == 0):
        total_pages = total_item / item_per_page
    else: 
        total_pages = total_item / item_per_page + 1

    # Join the digits to form a single string
    return int(total_pages)


# if __name__ == "__main__":
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
#     }
#     # for page in range(value):
#     url = "https://goods.musinsa.com/api/goods/v2/review/style/list?sort=up_cnt_desc&selectedSimilarNo=2086653&page=1&goodsNo=2086653"
#     response = requests.get(url, headers=headers)
        
#     if response.status_code == 200:
#         data = response.text
#         # print(getReview(data))
#         print(getSatisfaction(data))
    
#     else:
#         print(f"Failed to fetch data for page {page}. Status code: {response.status_code}")
