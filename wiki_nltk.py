import numpy as np
import json

import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

def tokenizer(sentence):
    return word_tokenize(sentence)


def pos_tagger(tokens):
    return nltk.pos_tag(tokens)


def stopword_treatment(tokens):
    stopword = stopwords.words('english')
    result = []
    for token in tokens:
        if token[0].lower() not in stopword:
            result.append(tuple([token[0].lower(), token[1]]))
    return result


pos_tag_map = {
    'NN': [wn.NOUN],
    'JJ': [wn.ADJ, wn.ADJ_SAT],
    'RB': [wn.ADV],
    'VB': [wn.VERB]
}


def pos_tag_converter(nltk_pos_tag):
    root_tag = nltk_pos_tag[0:2]
    try:
        pos_tag_map[root_tag]
        return pos_tag_map[root_tag]
    except KeyError:
        return ''


def get_synsets(tokens):
    synsets = []
    for token in tokens:
        wn_pos_tag = pos_tag_converter(token[1])
        if wn_pos_tag == '':
            continue
        else:
            synsets.append(wn.synsets(token[0], wn_pos_tag))
    return synsets


def get_tokens_from_synsets(synsets):
    tokens = {}
    for synset in synsets:
        for s in synset:
            if s.name() in tokens:
                tokens[s.name().split('.')[0]] += 1
            else:
                tokens[s.name().split('.')[0]] = 1
    return tokens


def get_hypernyms(synsets):
    hypernyms = []
    for synset in synsets:
        for s in synset:
            hypernyms.append(s.hypernyms())

    return hypernyms


def get_tokens_from_hypernyms(synsets):
    tokens = {}
    for synset in synsets:
        for s in synsets:
            for ss in s:
                if ss.name().split('.')[0] in tokens:
                    tokens[(ss.name().split('.')[0])] += 1
                else:
                    tokens[(ss.name().split('.')[0])] = 1
    return tokens


def underscore_replacer(tokens):
    new_tokens = {}
    for key in tokens.keys():
        mod_key = re.sub(r'_', ' ', key)
        new_tokens[mod_key] = tokens[key]
    return new_tokens


def generate_tokens(sentence):
    tokens = tokenizer(sentence)
    tokens = pos_tagger(tokens)
    tokens = stopword_treatment(tokens)
    synsets = get_synsets(tokens)
    synonyms = get_tokens_from_synsets(synsets)
    synonyms = underscore_replacer(synonyms)
    hypernyms = get_hypernyms(synsets)
    hypernyms = get_tokens_from_hypernyms(hypernyms)
    hypernyms = underscore_replacer(hypernyms)
    tokens = {**synonyms, **hypernyms}
    return tokens


if __name__ == '__main__':
    f = open("testFile.json")

    data = json.load(f)  # neskor nie cely dataset naraz ale po castiach, kvoli RAM
    texts = [item['text'] for item in data]
    text = texts[0]
    print(data[0])
    print(generate_tokens(text))
    print(generate_tokens('''Haskell (/ˈhæskəl/[25]) is a general-purpose, statically-typed, purely functional programming language with type inference and lazy evaluation.[26][27] Designed for teaching, research and industrial applications, Haskell has pioneered a number of programming language features such as type classes, which enable type-safe operator overloading, and monadic IO. Haskell's main implementation is the Glasgow Haskell Compiler (GHC). It is named after logician Haskell Curry.[1]
Haskell's semantics are historically based on those of the Miranda programming language, which served to focus the efforts of the initial Haskell working group.[28] The last formal specification of the language was made in July 2010, while the development of GHC continues to expand Haskell via language extensions.
Haskell is used in academia and industry.[29][30][31] As of May 2021[update], Haskell was the 28th most popular programming language by Google searches for tutorials,[32]  and made up less than 1% of active users on the GitHub source code repository.[33]
Following the release of Miranda by Research Software Ltd. in 1985, interest in lazy functional languages grew. By 1987, more than a dozen non-strict, purely functional programming languages existed. Miranda was the most widely used, but it was proprietary software. At the conference on Functional Programming Languages and Computer Architecture (FPCA '87) in Portland, Oregon, there was a strong consensus that a committee be formed to define an open standard for such languages. The committee's purpose was to consolidate existing functional languages into a common one to serve as a basis for future research in functional-language design.[34]
'''))

    f.close()