# 이번 작업에서 하는 것 : 영화제목 하나당 리뷰(리뷰문서:영화의 모든 리뷰를 하나의 문서로 만든 것) 하나씩 >> 데이터프레임 >> csv파일로 저장

import pandas as pd

df = pd.read_csv('./crawling_data/cleaned_reviews_2016-2022_team_future.csv') # 경로찾기때 ./가 없으면 현재경로부터 찾는다. 하지만 가독성을 생각해서라도 현재경로부터 찾을땐 ./을 붙여주도록 하자
df.dropna(inplace=True)
df.info()
one_sentences = []
for title in df['titles'].unique():
    temp = df[df['titles'] == title]
    if len(temp) > 30:
        temp = temp.iloc[:30, :]
    one_sentence = ' '.join(temp['clean_reviews'])
    one_sentences.append(one_sentence)
df_one = pd.DataFrame({'titles':df['titles'].unique(), 'reviews':one_sentences})
print(df_one.head())
df_one.to_csv('./crawling_data/one_sentences.csv', index=False)
