import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
import re
from gensim.models import Word2Vec

def getRecommendation(cosin_sim):
    simScore = list(enumerate(cosin_sim[-1])) # enumerate를 쓰는 이유 : 인덱스와 값을 하나로 묶었기 때문에 순서가 바뀌어도 그 전 인덱스를 유지하게 가져갈 수 있다.
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore[:11]
    movie_idx = [i[0] for i in simScore]
    recMovieList = df_reviews.iloc[movie_idx, 0]
    return recMovieList

df_reviews = pd.read_csv('./crawling_data/one_sentences.csv')
tfidf_matrix = mmread('./models/tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    tfidf = pickle.load(f)
'''------------------------------------------------------------------------------------------------------'''
# 영화제목이용 추천
movie_idx = df_reviews[df_reviews['titles']=='기생충 (PARASITE)'].index[0]
cosin_sim = linear_kernel(tfidf_matrix[movie_idx], tfidf_matrix)
recommendation = getRecommendation(cosin_sim)
print(recommendation[1:11])

#어떤 값들을 특정한 공간에 벡터라이징 함 >> 서로다른 벡터의 코사인값이 1에 가까울 수록 유사하다고 판단(코사인 유사도)
'''--------------------------------------------------------------------------------------------------------'''
# # 키워드 이용 추천
# embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')
# key_word = '크리스마스'
# sim_word = embedding_model.wv.most_similar(key_word, topn=10) # 유사한 단어찾기 x 유사한 문장을 찾는 것
# words = [key_word] * 10 # 의도적으로 반복을 늘림
# for word, _ in sim_word:
#     words.append(word)
# print(words)
#
#
# sentence = []
# count = 10
# for word in words: # tfidf의 반복횟수가 중요함(??) -> 그래서 다음 과정을 하게 됨 = 많이 유사한것들에 조금 더 웨이트(가중치)를 주고 문장을 만드는 과정
#     sentence = sentence + [word] * count
#     count -= 1
# sentence = ' '.join(sentence)
# sentence_vec = tfidf.transform([sentence])
# cosin_sim = linear_kernel(sentence_vec, tfidf_matrix)
# recommendation = getRecommendation(cosin_sim)
# print(recommendation)
'''-----------------------------------------------------------------------------------------------------------'''
## 문장으로 추천
# sentence = '화려한 액션과 소름돋는 반전이 있는 영화'
# review = re.sub('[^가-힣 ]', ' ', sentence)
# okt = Okt()
# token = okt.pos(review, stem = True)
# df_token = pd.DataFrame(token, columns=['word', 'class'])
# df_token = df_token[(df_token['class']=='Noun')|
#                     (df_token['class']=='Verb')|
#                     (df_token['class']=='Adjective')]
# words = []
# for word in df_token.word:
#     if 1 < len(word):
#         words.append(word)
#    #불용어 처리는 귀찮아서 안함
# cleaned_sentence = ' '.join(words)
# print(cleaned_sentence)
# sentence_vec = tfidf.transform([cleaned_sentence])
# cosin_sim = linear_kernel(sentence_vec, tfidf_matrix)
# recommendation = getRecommendation(cosin_sim)
# print(recommendation)