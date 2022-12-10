import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split
from wordcloud import WordCloud

# %matplotlib inline
def spamdetection():
    sms = pd.read_csv('spam.csv', encoding='ISO-8859-1')
    sms.head()
    cols_to_drop = ['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4']
    sms.drop(cols_to_drop, axis=1, inplace=True)
    sms.columns = ['label', 'message']
    sms.head()
    sms.info()
    sms.isnull().sum()
    cv = CountVectorizer(decode_error='ignore')
    X = cv.fit_transform(sms['message'])

    X_train, X_test, y_train, y_test = train_test_split(
        X, sms['label'], test_size=0.3, random_state=101)
    sms['message'][0]
    mnb = MultinomialNB()
    mnb.fit(X_train,y_train)
    print('training accuracy is --> ',mnb.score(X_train,y_train)*100)
    print('test accuracy is --> ',mnb.score(X_test,y_test)*100)


    def visualize(label):
        words = ''
        for msg in sms[sms['label'] == label]['message']:
            msg = msg.lower()
            words += msg + ' '
        wordcloud = WordCloud(width=600, height=400).generate(words)
        plt.imshow(wordcloud)
        plt.axis('off')


    visualize('spam')
    visualize('ham')
    # just type in your message and run
    your_message = 'You are the lucky winner for the lottery price of $6million.'
    your_message = cv.transform([your_message])
    claass = mnb.predict(your_message)
    print(f'This is a {claass[0]} message')
