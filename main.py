import numpy as np
import json

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

    epochs = 1
    for i_epoch in range(epochs):
        article_i = 0
        for i, article in enumerate(data):
            print("Article", i, "of", len(data))
            for word in article['text'].split(" "):
                formatted_word = word.lower()
                for stop_char in stop_characters:
                    formatted_word = formatted_word.replace(stop_char, '')
                if formatted_word in stop_words:
                    continue
                if formatted_word not in corpus:
                    corpus.append(formatted_word)
                    word_count += 1
                    #print(formatted_word)
            print(word_count)

    for i, word in enumerate(corpus):
        print(i, ":", word)

    print(len(corpus))

    f.close()
