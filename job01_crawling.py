from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

# 네이버영화에서 리뷰를 보면 비슷한 리뷰를 가진 영화를 추천하는 모델
options = webdriver.ChromeOptions()

options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver.exe',)

url = 'https://movie.naver.com/movie/sdb/browsing/bmovie_open.naver?open=2022&page=1'