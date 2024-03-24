import math
import os

from nltk import word_tokenize

lemmas_tf_idf_path = '../classifier/lemmas'
lemmas_path = '../tokens/lemmas.txt'
inverted_index_path = '../inverted_index.txt'


def load_lemmas():
    lemmas = {}
    with open(lemmas_path, encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            words = line.rstrip('\n').split(' ')
            for word in words:
                lemmas[word] = words[0]
    return lemmas


def load_lemma_tf_idf():
    result = {}
    for file_name in os.listdir(lemmas_tf_idf_path):
        with open(f"{lemmas_tf_idf_path}/" + file_name, encoding='utf-8') as file:
            lines = file.readlines()
            result[file_name] = {data[0]: float(data[2]) for data
                                 in [line.rstrip('\n').split(' ') for line in lines]}
    return result


def load_inverted_index():
    result = {}
    with open(inverted_index_path, encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            token = line.split(' ')[0].split('[')[0]
            result[token] = [f"lemmas{num}.txt" for num in line.rstrip('\n').split(' ')[1:]]
    return result


def calc_vect_len(vector):
    return math.sqrt(sum(i ** 2 for i in vector.values()))


def calc_values(lemma_tf_idf):
    lemmas_list = os.listdir(lemmas_tf_idf_path)
    return {lemma: calc_vect_len(lemma_tf_idf[lemma]) for lemma in lemmas_list}


def mult_vect(query_vector, value_vect, value_vec_len):
    return sum(value_vect.get(token) for token in query_vector) / len(query_vector) / value_vec_len


def process_query(query):
    tokens = word_tokenize(query, language='russian')
    inverted_index = load_inverted_index()
    lemma_tf_idf = load_lemma_tf_idf()
    values = calc_values(lemma_tf_idf)

    token_lemmas = load_lemmas()
    lemmas = [token_lemmas[token] for token in tokens if token in token_lemmas]

    result = set()
    for lemma in lemmas:
        result = result.union(inverted_index.get(lemma), set())
    results = {res: mult_vect(lemmas, lemma_tf_idf[res], values[res]) for res in result}
    return dict(res for res in results.items() if res[1] > 0.0)


# process user input with infinite loop
while True:
    input_query = input("Enter expression: ").lower()
    if input_query == 'quit' or input_query == 'q':
        exit()
    try:
        print(process_query(input_query))
    except Exception as e:
        print('An error occurred. Please, try again or "quit" to exit.')
