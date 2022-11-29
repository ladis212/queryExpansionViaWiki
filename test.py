import numpy as np
import json

from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Definicia modelu

# Zoznam stop-words (a, the, "/", ".", ..., mozno specialne aj veci ako ---History---)

if __name__ == '__main__':
    f = open("testFile.json")

    data = json.load(f)  # neskor nie cely dataset naraz ale po castiach, kvoli RAM
    texts = [item['text'] for item in data]

    # tfidf = TfidfVectorizer()
    # transformed = tfidf.fit_transform(texts)
    # df = pd.DataFrame({"word": tfidf.get_feature_names_out(),
    #                   "TF-IDF": [item[0] for item in transformed[0].T.todense()]})
    word_to_index = dict()
    index_to_word = dict()
    corpus = []
    word_count = 0

    stop_words = ["a", "an", "and", "another", "at", "be", "but", "can", "can't", "do", "does", "doesn't",
                  "each", "every", "get", "he", "him", "his", "her", "is", "in", "isn't", "it", "its",
                  "no", "not", "of", "one", "on", "or", "she", "that", "the", "their", "this", "to", "was",
                  "which", "who", "-"]

    stop_characters = [".", ",", "!", "?", "(", ")", "[", "]", "{", "}", ":", "&", ";" "\"", "=", "*", "$", "|",
                       "€"]

    # df = df.sort_values('TF-IDF', ascending=False)
    # print(df)

    # Vytvorenie modelu

    epochs = 1
    for i_epoch in range(epochs):
        article_i = 0
        for i, article in enumerate(data):
            print(i)

    # Trenovanie modelu na 'title' a 'text'
    # Kazdych X krokov by bol vykonany evaluation na testovacej mnozine
    #        print(article['title'])
    f.close()

    # pridaj nejaky search engine cez library ktory by prehladaval dataset
    # a vedel by som donho hodit expanded query z modelu
