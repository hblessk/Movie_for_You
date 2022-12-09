import pandas as pd
from gensim.models import Word2Vec

review_word = pd.read_csv('./crawling_data/one_sentences.csv')
review_word.info()
cleaned_tokens = []
one_sentence_reviews = list(review_word['reviews'])
for sentence in one_sentence_reviews:
    token = sentence.split()
    cleaned_tokens.append(token)


embedding_model = Word2Vec(cleaned_tokens, vector_size=100, window=4, min_count=20, workers=4, epochs=100, sg=1)
embedding_model.save('./models/word2vec_movie_review.model')
print(list(embedding_model.wv.index_to_key))
print(len(embedding_model.wv.index_to_key))
