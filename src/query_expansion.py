# import numpy as np
import json
import tempfile
import os.path

import nltk
from nltk.corpus import wordnet as wn

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

import re
from datetime import datetime


def download_nltk_packages():
    nltk.download('wordnet')  # nltk package required for getting synonyms


download_nltk_packages()


def preprocess(text):  # simple preprocessing that is runnable within a pyspark dataframe
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)  # regex for removing special characters
    return text


def expand_query(text, n_synonyms=1):  # function to expand a query with synonyms via NLTK
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
    return expanded_query[:-1]  # exclude the last ' '


if __name__ == '__main__':  # ensure this code only runs when running this file and not in the unit tests
    spark = SparkSession.builder \
        .master('local[8]') \
        .appName('readJSON') \
        .getOrCreate()  # SparkSession required for PySpark

    # assign data directory
    directory = os.path.join('..', 'data')

    # iterate over data files
    counter = 0
    rowCounter = 0
    beginTime = datetime.now()
    for filename in os.listdir(directory):  # process every file in the data directory

        f = os.path.join(directory, filename)
        if not (os.path.isfile(f) and filename.endswith('.json')):
            continue  # skip directories and unrelated files

        df = spark.read.option('multiline', 'true').json(f)
        df = df.drop(col('text'))

        rdd2 = df.rdd.map(lambda x: (preprocess(x.title), 1))  # apply the preprocess function
        preprocessed_df = rdd2.toDF(['tokens']).select('tokens')  # convert back to pyspark df
        pandas_df = preprocessed_df.toPandas()  # convert to pandas df for further processing

        pandas_df['expansion'] = pandas_df.apply(lambda row: expand_query(row['tokens']), axis=1)

        rowCounter += pandas_df.shape[0]  # count up the amount of processed rows
        print(counter, 'th file: \n', pandas_df.head(1))  # show only the head, but the entire dataframe is expanded
        print(rowCounter, 'rows processed thus far')
        counter += 1

    print('Time taken to process data: ', datetime.now() - beginTime)
