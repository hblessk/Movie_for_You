import sys          # sys : 파이썬 기본 라이브러리,
from PyQt5.QtWidgets import *           # pyQt5 라이브러리 안의 모든 것을 import 하는 법
from PyQt5 import uic
import pandas as pd
from PyQt5.QtCore import QStringListModel
from scipy.io import mmread
import pickle
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import linear_kernel
import re
from konlpy.tag import Okt

form_window = uic.loadUiType('./movie_recommendation_app.ui')[0]      #ui를 class로 만들어줌   # 파일은 designer에서 만들어 프로젝트파일 안에 넣는다.

class Exam(QWidget, form_window):           # 다중상속받음
    def __init__(self):                     #
        super().__init__()
        self.setupUi(self)                  # ui 초기화

        #
        self.tfidf_matrix = mmread('./models/tfidf_movie_review.mtx').tocsr() # tocsr() : 매트릭스의 형태를
        with open('./models/tfidf.pickle', 'rb') as f:
            self.tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')

        self.df_reviews = pd.read_csv('./crawling_data/one_sentences.csv')
        self.titles = self.df_reviews['titles']
        self.titles = sorted(self.titles)
        for title in self.titles:
            self.combo_box.addItem(title)

        model = QStringListModel()# 자동완성 기능
        model.setStringList(self.titles)
        completer = QCompleter()
        completer.setModel(model)
        self.line_edit.setCompleter(completer)

        self.combo_box.currentIndexChanged.connect(self.combobox_slot) #
        self.btn_recommend.clicked.connect(self.btn_slot)

    def recommendation_by_movie_title(self, title):
        movie_idx = self.df_reviews[self.df_reviews['titles'] == title].index[0]
        cosin_sim = linear_kernel(self.tfidf_matrix[movie_idx], self.tfidf_matrix)
        recommendation = self.getRecommendation(cosin_sim)
        recommendation = '\n'.join(list(recommendation[1:]))  # 문자열로 바꾸는 코드
        self.lbl_recommend.setText(recommendation)

    def recommendation_by_key_word(self, key_word):
        sim_word = self.embedding_model.wv.most_similar(key_word, topn=10)  # 유사한 단어찾기 x 유사한 문장을 찾는 것
        words = [key_word]
        for word, _ in sim_word:
            words.append(word)
        print(words)
        sentence = []
        count = 11
        for word in words:  # tfidf의 반복횟수가 중요함(??) -> 그래서 다음 과정을 하게 됨 = 많이 유사한것들에 조금 더 웨이트(가중치)를 주고 문장을 만드는 과정
            sentence = sentence + [word] * count
            count -= 1
        sentence = ' '.join(sentence)
        sentence_vec = self.tfidf.transform([sentence])
        cosin_sim = linear_kernel(sentence_vec, self.tfidf_matrix)
        recommendation = self.getRecommendation(cosin_sim)
        recommendation = '\n'.join(list(recommendation[1:]))
        self.lbl_recommend.setText(recommendation)

    def recommendation_by_sentence(self, key_word):
        review = re.sub('[^가-힣 ]', ' ', key_word)
        okt = Okt()
        token = okt.pos(review, stem = True)
        df_token = pd.DataFrame(token, columns=['word', 'class'])
        df_token = df_token[(df_token['class']=='Noun')|
                            (df_token['class']=='Verb')|
                            (df_token['class']=='Adjective')]
        words = []
        for word in df_token.word:
            if 1 < len(word):
                words.append(word)
           #불용어 처리는 귀찮아서 안함
        cleaned_sentence = ' '.join(words)
        sentence_vec = self.tfidf.transform([cleaned_sentence])
        cosin_sim = linear_kernel(sentence_vec, self.tfidf_matrix)
        recommendation = self.getRecommendation(cosin_sim)
        recommendation = '\n'.join(list(recommendation[1:]))
        self.lbl_recommend.setText(recommendation)

    def btn_slot(self):
        key_word = self.line_edit.text()
        if key_word in self.titles:
            self.recommendation_by_movie_title(key_word)
        elif key_word in list(self.embedding_model.wv.index_to_key):
            self.recommendation_by_key_word(key_word)
        else:
            self.recommendation_by_sentence(key_word)

    def combobox_slot(self):
        title = self.combo_box.currentText() #
        self.recommendation_by_movie_title(title)

    def getRecommendation(self, cosin_sim):
        simScore = list(enumerate(cosin_sim[-1]))  # enumerate를 쓰는 이유 : 인덱스와 값을 하나로 묶었기 때문에 순서가 바뀌어도 그 전 인덱스를 유지하게 가져갈 수 있다.
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
        simScore = simScore[:11]
        movie_idx = [i[0] for i in simScore]
        recMovieList = self.df_reviews.iloc[movie_idx, 0]
        return recMovieList

if __name__ == "__main__":                  # 모듈로 사용할 수 도 있으니 습관적으로 만들어주어라.
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())