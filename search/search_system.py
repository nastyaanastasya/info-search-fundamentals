import json
import math
import os

from nltk import word_tokenize

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)

inverted_index_path = os.path.join(current_dir, '..', 'inverted_index.json')
lemmas_tf_idf_path = os.path.join(current_dir, '..', 'classifier', 'lemmas')
lemmas_path = os.path.join(current_dir, '..', 'tokens', 'lemmas.txt')


def load_inverted_index():
    with open(inverted_index_path, encoding='utf-8') as file:
        json_index = file.readline()
        index = json.loads(json_index)
        return index


def load_lemma_tokens():
    lemmas = {}
    with open(lemmas_path, encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            words = line.rstrip('\n').split(' ')
            for word in words:
                lemmas[word] = words[0]
    return lemmas


def load_doc_to_lemma_tf_idf():
    result = {}
    for file_name in os.listdir(lemmas_tf_idf_path):
        with open(os.path.join(lemmas_tf_idf_path, file_name), encoding='utf-8') as file:
            lines = file.readlines()
            result[file_name] = {data[0]: float(data[2]) for data in [line.rstrip('\n').split(' ') for line in lines]}
    return result


def calculate_doc_vector_length(doc_to_words):
    return math.sqrt(sum(i ** 2 for i in doc_to_words.values()))


def multiply_vectors(query_vector, doc_vector, doc_vector_len):
    return sum(doc_vector.get(token, 0) for token in query_vector) / len(query_vector) / doc_vector_len


def process_query(query):
    tokens = word_tokenize(query, language='russian')

    token_to_lemma = load_lemma_tokens()
    doc_to_lemma = load_doc_to_lemma_tf_idf()
    reverse_index = load_inverted_index()

    lemmas = [token_to_lemma[token] for token in tokens if token in token_to_lemma]
    doc_lengths = {doc: calculate_doc_vector_length(doc_to_lemma[doc]) for doc in os.listdir(lemmas_tf_idf_path)}

    doc_set = set()
    for lemma in lemmas:
        doc_set = doc_set.union(reverse_index.get(lemma))
    results = {doc: multiply_vectors(lemmas, doc_to_lemma[doc + '.txt'], doc_lengths[doc + '.txt']) for doc in doc_set}
    return dict(sorted(results.items(), key=lambda r: r[1]))
