import pandas as pd
from gensim.models import Word2Vec
# 이번 작업에서 하는 것 :

review_word = pd.read_csv('./crawling_data/one_sentences.csv')
review_word.info()
cleaned_tokens = []
one_sentence_reviews = list(review_word['reviews'])
for sentence in one_sentence_reviews:
    token = sentence.split()
    cleaned_tokens.append(token)


# 의미적으로 유사한 단어를 찾아서
embedding_model = Word2Vec(cleaned_tokens, vector_size=100, window=4, min_count=20, workers=4, epochs=100, sg=1) # one_의 형식은 리스트(형태소단위로 이루어진) #Word2Vec() :  단어를 벡터(크기와 방향을 가짐)화 해준다. 단어를 벡터로 만든다. 주의! 좌표가 아님 # window = 4 : 컨브레이어 쓰는 커널과 같은 느낌, 커널의 수 # min_count = 20 : 최소 20개단어가 있어야 한다, 20개 단어 미만이면 버림 # workers = 4 : '컨트롤+알트+딜리트'>>작업관리자 >>성능>>논리프로세서 개수 만큼 쓸 수 있음 # sg = 1 : 벡터화하는 학습알고리즘(skip gram)을 지칭(0이면 cbow, 1이면 sg) cbow(c back of words)
embedding_model.save('./models/word2vec_movie_review.model')
print(list(embedding_model.wv.index_to_key))
print(len(embedding_model.wv.index_to_key))
'''
단어의 벡터화 : embedding
ex) 겨울 여름 춥다, 덥다 ....
1. '겨울'이라는 축(겨울차원(의미차원)의 축)을 두고 다른 단어들을 '겨울'의 의미에 가까울수록 큰값, 멀수록 작은 값으로 좌표를 배치
2. 그 상태에서 
3. 1과 2를 반복
4. 모든 차원에 배치가 되면 비슷한 의미를 가진 단어는 가깝게 배치가 된다.
*. 차원이 늘어날 수록 의미의 거리가 멀어져 의미가 희소해진다(차원의 저주)

벡터화를 하게되면 방향을 알 수 있게된다.

말뭉치(코퍼스)속에 들어있는 형태소들을 형태소개수 만큼 의미차원을 만들고 각각 의미에 맞게 배치한다.


ex2)
오늘 날씨가 '겨울'답다
오늘 날씨가 '여름'답다
>> 두 문장을 학습을 하게되면 '겨울'과 '여름'을 비슷한 것으로 학습하게 된다.
>> '겨울'과 '여름'은 온도라는 의미차원에서는 반대이지만, 계절이라는 의미차원에서는 비슷하다
'''