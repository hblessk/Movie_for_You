# crawling 작업

# crawling은 각자 진행해보고 빨리 완성되는 코드로 연도를 나눠서 작업하겠습니다.
# 일단 2022년 개봉작만 크롤링해주세요.
# 나머지는 연도별로 나눠서 작업하겠습니다.
# 컬럼명은 ['titles', 'reviews']로 통일해주세요.
# 파일명은 'reviews_{}.csv'.format(연도)로 해주세요.
# crawling 코드 완성되는대로 PR해주세요.


from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

# 네이버영화에서 리뷰를 보면 비슷한 리뷰를 가진 영화를 추천하는 모델
options = webdriver.ChromeOptions()

options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver.exe', options=options)

review_button_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a'              # xpath가 고정인 경우에 for문 안에서 계속 변수생성할 필요가 없으므로 for문밖으로 빼줌
review_num_path = '//*[@id="reviewTab"]/div/div/div[2]/span/em'         # xpath가 고정인 경우에 for문 안에서 계속 변수생성할 필요가 없으므로 for문밖으로 빼줌
review_xpath = '//*[@id="content"]/div[1]/div[4]/div[1]/div[4]'     # xpath가 고정인 경우에 for문 안에서 계속 변수생성할 필요가 없으므로 for문밖으로 빼줌

your_year = 2022
for page in range(1, 32): # page
    url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={}&page={}'.format(your_year, page)
    titles = []
    reviews = []
    try:
        for movie_title_num in range(1, 21): # 영화 게시글
            driver.get(url)
            time.sleep(0.1)
            movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(movie_title_num)
            title = driver.find_element('xpath', movie_title_xpath).text
            print('title', title)
            driver.find_element('xpath', movie_title_xpath).click()
            time.sleep(0.1)
            try:
                driver.find_element('xpath', review_button_xpath).click()
                time.sleep(0.1)
                review_num = driver.find_element('xpath', review_num_path).text
                review_num = review_num.replace(',', '') # 리뷰가 1000개가 넘어가면 단위표시 ,가 같이 긁어와져 int로 변환이 안됨 >> ,를 제거해야 함
                review_range = (int(review_num) - 1) // 10 + 1 # 리뷰개수가 0개면 1페이지가 됨
                if review_range > 3:
                    review_range = 3
                for review_page in range(1, review_range + 1):
                    review_page_button_xpath = '//*[@id="pagerTagAnchor{}"]/span'.format(review_page)
                    driver.find_element('xpath', review_page_button_xpath).click()
                    time.sleep(0.1)
                    for review_title_num in range(1, 11): # 리뷰 게시글
                        review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a/strong'.format(review_title_num)
                        driver.find_element('xpath', review_title_xpath).click()
                        time.sleep(0.1)
                        try:
                            review = driver.find_element('xpath', review_xpath).text
                            titles.append(title)
                            reviews.append(review)
                            driver.back()
                        except:
                            print('review', page, movie_title_num, review_title_num)
            except:
                driver.back()
                print('review button', page, movie_title_num)
        df = pd.DataFrame({'titles':titles, 'reviews':reviews})
        df.to_csv('./crawling_data/reviews_{}_{}page.csv'.format(your_year, page), index=False)
    except:
        print('error', page, movie_title_num)