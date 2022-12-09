import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./crawling_data/review_2016-2022_team_future.csv')
df.info()
print(df.head())

df_stopwords = pd.read_csv('./stopwords.csv', index_col=0)
stopwords = list(df_stopwords['stopword'])
stopwords = stopwords + ['안나', '제니퍼', '미국', '중국', '영화', '감독', '라뷰', '연출', '장면', '주인공', '되어다', '출연', '싶다', '올해', '엘사'] # 추천하는데 도움이 안되는 단어들

okt = Okt()
df['clean_reviews'] = None
count = 0
for idx, review in enumerate(df.reviews):
    count += 1
    if count % 10 == 0:
        print('.', end='')
    if count % 1000 == 0:
        print()
    review = re.sub('[^가-힣 ]', ' ', review)
    df.loc[idx, 'clean_reviews'] = review
    token = okt.pos(review, stem=True)
    df_token = pd.DataFrame(token, columns=['word', 'class'])
    df_token = df_token[(df_token['class']=='Noun') |
                        (df_token['class']=='verb') |
                        (df_token['class']=='Abjective')]
    words = []
    for word in df_token.word:
        if len(word) > 1:
            if word not in list(df_stopwords.stopword): # 질문 : df_stopwords.stopword대신 df_stopwords['stopword']으로 써도 가능한가?
                words.append(word)
    cleaned_sentence = ' '.join(words)
    df.loc[idx, 'clean_reviews'] = cleaned_sentence
print(df.head(30))
df.dropna(inplace=True)
df.to_csv('./crawling_data/cleaned_reviews_2016-2022_team_future.csv')

#불용어 제거 : 한글자짜리 형태소?를 빼는 이유 : 한글은 한자의 영향권 때문에 동음이의어가 많아서 한글자로는 의미파악이 힘들다

# token = okt.pos(df.clean_reviews[0], stem = True) # stem = True : 용언의 기본형으로 변환 ; stem = True가 없으면 의미차원이 많아져 안좋다, 따라서 stem = True는 의미차원을 줄여주는 역할을 함
# print(token)
# morphs : 형태소로 다 나눠줌
# pos : 형태소와 품사를 다 남겨서 줌 ; 각 품사를 태깅하는 역할을 한다. 품사를 태깅한다는 것은 주어진 텍스트를 형태소 단위로 나누고, 나눠진 각 형태소를 그에 해당하는 품사와 함께 리스트화하는 것을 의미한다. 옵션으로 norm, stem, join이 있는데 join은 나눠진 형태소와 품사를 ‘형태소/품사’ 형태로 같이 붙여서 리스트화한다.
# konlpy 플랫폼 개발팀 기술 블로그       :     https://team-platform.tistory.com/46