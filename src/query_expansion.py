# import numpy as np
import json

import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import pyspark
import pyspark.pandas as ps
from pyspark.ml.feature import RegexTokenizer
from pyspark.context import SparkContext
from pyspark.sql import SQLContext
import pandas as pd


def download_nltk_packages():
    nltk.download('wordnet')
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')


download_nltk_packages()


def expand_query_pipeline(sentence):
    # tokens = word_tokenize(sentence)
    # tagged_tokens = 1
    synonyms = wn.synsets(sentence)
    for name in synonyms.lemma_names():
        print(name)


sentenceDataFrame = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                                 columns=['a', 'b', 'c'])

sc = SparkContext('local', 'test')
sqlContext = SQLContext(sc)
# sqlContext.createDataFrame(sentenceDataFrame)

# tokenizer = RegexTokenizer(inputCol="sentence", outputCol="words", pattern="")
# tokenized = tokenizer.transform(sentenceDataFrame)

columns = ["language", "users_count"]
data = [("Java", "20000"), ("Python", "100000"), ("Scala", "3000")]

psdf = ps.DataFrame(["car", "job", "man"], columns=['titles'])
sdf = psdf.to_spark()
sdf.show()

# expand_query_pipeline("knowledge")
