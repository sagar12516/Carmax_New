# import nltk
# import ssl
#
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
#
# nltk.download()

import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import streamlit as st
import plotly.express as px
import altair as alt



lemma = WordNetLemmatizer()
stop_words = stopwords.words('english')
sent = SentimentIntensityAnalyzer()
pos = 0
neutral = 0
neg = 0
new_count = 0
old_count = 0
dict = {'name':[],'comment':[]}


# def text_prep(self,x):
#     corp = str(x).lower()
#     corp = re.sub('[^a-zA-Z]+', ' ', corp).strip()
#     tokens = word_tokenize(corp)
#     words = [t for t in tokens if t not in self.__class__.stop_words]
#     lemmatize = [self.__class__.lemma.lemmatize(w) for w in words]
#
#     return lemmatize
#
# def preprocessing(self,x):
#     preprocess_tag = self.text_prep(x)
#     print(preprocess_tag)
#     file = open('/Users/venkatsagar/Documents/pos_neg_words/negative-words.txt', 'r',encoding="latin-1")
#     neg_words = file.read().split()
#     # print(neg_words)
#     file = open('/Users/venkatsagar/Documents/pos_neg_words/positive-words.txt', 'r',encoding="latin-1")
#     pos_words = file.read().split()
#     # print(pos_words)
#
#     num_pos = list(map(lambda x: len([i for i in x if i in pos_words]),preprocess_tag))
#     pos_count = num_pos
#     print("pos ct ",pos_count)
#     num_neg = list(map(lambda x: len([i for i in x if i in neg_words]),preprocess_tag))
#     neg_count = num_neg
#     print("neg ct ", neg_count)
#
#     sentiment = round((pos_count - neg_count ), 2)
#
#     print(sentiment)


def preprocessing(self, st, x,placeholder,neg=neg,pos=pos,neutral=neutral,dict=dict):

    # self.__class__.new_count += 1
    dict['comment'].append(x)
    polarity = [round(SentimentIntensityAnalyzer().polarity_scores(x)['compound'], 2)]
    print(polarity[0])

    if polarity[0] < 0.0:
        neg+=polarity[0]
        dict['name'].append('negative')
    elif polarity[0] == 0.0:
        neutral+=polarity[0]
        dict['name'].append('neutral')
    elif polarity[0] > 0.0:
        pos+=polarity[0]
        dict['name'].append('positive')


    df = pd.DataFrame.from_dict(dict)
    print("df ",df)
    if len(list(df['name'])) == 0:
        st.markdown("No Results found")

    else:
        val_cts = df['name'].value_counts()
        x = sorted(list(map(str, list(val_cts.index))))
        y = list(map(int, val_cts.values))
        with placeholder.container():
            # st.markdown(f"### {df['comment']}")
            fig = px.bar(x=x, y=y, color= x)
            fig.update_layout(xaxis_type='category',
                              xaxis_title="Polarity",
                              yaxis_title="Count",
                              yaxis={
                                  "tickvals": list(range(0, 10000,2))
                              }
                              )

            st.write(fig)
            # val_cts = df['name'].value_counts()
            # x = sorted(list(map(str, list(val_cts.index))))
            # y = list(map(int, val_cts.values))
            # fig = px.bar(x=x, y=y, color=x)




