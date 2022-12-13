# import numpy as np
import json
import tempfile
import os.path

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

import pyspark
import pyspark.pandas as ps
from pyspark.ml.feature import Tokenizer
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.functions import col
import pandas as pd

import re
from datetime import datetime


def download_nltk_packages():
    nltk.download('wordnet')  # nltk package required for getting synonyms


download_nltk_packages()


def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)  # regex for removing special characters
    return text


def expand_query(text, n_synonyms=1):
    synonyms = set()
    for word in set(text.split(' ')):
        for synset in wn.synsets(word):
            for lemma in synset.lemmas()[:n_synonyms]:
                lemma_name = lemma.name().replace('_', ' ')
                if lemma_name.lower() != word:
                    synonyms.add(lemma_name)

    expanded_query = ''
    for synonym in synonyms:
        expanded_query += synonym + ' '
    return expanded_query[:-1]


if __name__ == '__main__':
    spark = SparkSession.builder \
        .master('local[8]') \
        .appName('readJSON') \
        .getOrCreate()

    # assign data directory
    directory = os.path.join('..', 'data')

    # iterate over data files
    counter = 0
    rowCounter = 0
    beginTime = datetime.now()
    for filename in os.listdir(directory):

        f = os.path.join(directory, filename)
        if not (os.path.isfile(f) and filename.endswith('.json')):
            continue  # skip directories and unrelated files

        df = spark.read.option('multiline', 'true').json(f)
        df = df.drop(col('text'))

        rdd2 = df.rdd.map(lambda x: (preprocess(x.title), 1))
        preprocessed_df = rdd2.toDF(['tokens']).select('tokens')
        pandas_df = preprocessed_df.toPandas()

        pandas_df['expansion'] = pandas_df.apply(lambda row: expand_query(row['tokens']), axis=1)

        rowCounter += pandas_df.shape[0]
        print(counter, 'th file: \n', pandas_df.head(1))
        print(rowCounter, 'rows processed thus far')
        counter += 1

    print('Time taken to process data: ', datetime.now() - beginTime)
