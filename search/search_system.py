import json
import math
import os
from typing import Dict, List
from nltk import word_tokenize

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)

inverted_index_path = os.path.join(current_dir, '..', 'inverted_index.json')
lemmas_tf_idf_path = os.path.join(current_dir, '..', 'classifier', 'lemmas')
lemmas_path = os.path.join(current_dir, '..', 'tokens', 'lemmas.txt')

LEMMAS_TFIDF_PATH = '../classifier/lemmas/'
LEMMA_TOKENS_FILE = os.path.join(current_dir, '..', 'tokens', 'lemmas.txt')
INVERTED_INDEX_FILE = 'inverted_index.json'


def load_inverted_index():
    with open(INVERTED_INDEX_FILE, encoding='utf-8') as file:
        json_index = file.readline()
        index = json.loads(json_index)
        return index


def load_lemma_tokens() -> Dict[str, str]:
    lemmas = {}
    with open(LEMMA_TOKENS_FILE, encoding='utf-8') as lemma_file:
        lines = lemma_file.readlines()
        for line in lines:
            line = line.rstrip('\n')
            words = line.split(' ')
            for word in words:
                lemmas[word] = words[0]
    return lemmas


def load_doc_to_lemma_tf_idf() -> Dict[str, Dict[str, float]]:
    result = {}
    for file_name in os.listdir(lemmas_tf_idf_path):
        with open(os.path.join(lemmas_tf_idf_path, file_name), encoding='utf-8') as tf_idf_file:
            lines = tf_idf_file.readlines()
            result[file_name] = {data[0]: float(data[2]) for data in [line.rstrip('\n').split(' ') for line in lines]}
    return result


def calculate_doc_vector_length(doc_to_words: Dict[str, float]):
    return math.sqrt(sum(i ** 2 for i in doc_to_words.values()))


def multiply_vectors(query_vector: List[str], doc_vector: Dict[str, float], doc_vector_len: int):
    return sum(doc_vector.get(token, 0) for token in query_vector) / len(query_vector) / doc_vector_len


def merge_or(set1, set2):
    return set1.union(set2)


def process_query(query: str):
    tokens = word_tokenize(query, language='russian')
    lemmas = [token_to_lemma[token] for token in tokens if token in token_to_lemma]
    doc_set = set()
    for lemma in lemmas:
        doc_set = merge_or(doc_set, reverse_index.get(lemma, set()))
    results = {doc: multiply_vectors(lemmas, doc_to_lemma[doc + '.txt'], doc_lengths[doc + '.txt']) for doc in doc_set}
    return dict(sorted(results.items(), key=lambda r: r[1], reverse=True))


docs_list = os.listdir(lemmas_tf_idf_path)
doc_to_lemma = load_doc_to_lemma_tf_idf()
lemma_to_doc = load_doc_to_lemma_tf_idf()  # Можете использовать одну из этих функций
doc_lengths = {doc: calculate_doc_vector_length(doc_to_lemma[doc]) for doc in docs_list}
token_to_lemma = load_lemma_tokens()
reverse_index = load_inverted_index()