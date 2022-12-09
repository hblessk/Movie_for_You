import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import collections
from matplotlib import font_manager, rc
from PIL import Image
import matplotlib as mpl

# 한글을 쓰기 위해서 한글 폰트 설정
font_path = './malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
mpl.rcParams['axes.unicode_minus'] = False
rc('font', family=font_name)

df = pd.read_csv('./crawling_data/one_sentences.csv')
words = df[df['titles']=='속닥속닥 (The Whispering)']['reviews']
print(words.iloc[0])
words = words.iloc[0].split()
print(words)

worddict = collections.Counter(words)
worddict = dict(worddict)
print(worddict)

#wordcloud 이미지를 보여줌
wordcloud_img = WordCloud(background_color='white', max_words=2000, font_path=font_path).generate_from_frequencies(worddict) # 그림안에 출력되는 단어 개수 2000개로 제한
plt.figure(figsize=(12, 12))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')

words = df[df['titles']=='속닥속닥 (The Whispering)']['reviews']
words = words.iloc[0].split()
worddict = collections.Counter(words)
worddict = dict(worddict)



plt.show()