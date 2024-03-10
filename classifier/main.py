import math
import os

directory_path = "../crawler/pages"
lemmas_path = "../tokens/lemmas.txt"
tokens_path = "../tokens/tokens.txt"
output_tokens_dir = "../classifier/tokens/"
output_lemmas_dir = "../classifier/lemmas/"


def read_files_in_directory(directory):
    files_content = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
                files_content.append(content)

    return files_content


def read_terms(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().split()


def read_lemma_forms(file_path):
    lemma_forms = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            lemma_forms[i] = parts
    return lemma_forms


def calculate_idf(term, documents):
    num_documents_with_term = sum(1 for doc in documents if term in doc)
    num_documents = len(documents)
    idf = math.log(num_documents / (1 + num_documents_with_term))
    return idf


def calculate_all_idf(tokens, documents):
    all_idf = {}
    for token in tokens:
        idf = calculate_idf(token, documents)
        all_idf[token] = idf
    return all_idf


def calculate_tf(term, document):
    words = document.split()
    term_count = words.count(term)
    total_words = len(words)
    tf = term_count / total_words if total_words > 0 else 0
    return tf


def calculate_all_lemma_idf(lemmas, documents):
    all_idf = {}
    for i in lemmas:
        idf = calculate_lemma_idf(lemmas[0], documents)
        all_idf[i] = idf
    return all_idf


def calculate_lemma_idf(terms, documents):
    num = 0
    for term in terms:
        num += sum(1 for doc in documents if term in doc)
    num_documents = len(documents)
    idf = math.log(num_documents / (1 + num))
    return idf


def calculate_lemma_tf(document, lemma_forms):
    words = document.split()
    total_words = len(words)
    term_count = 0
    for lemma in lemma_forms:
        term_count += words.count(lemma)

    tf = term_count / total_words
    return tf


documents = read_files_in_directory(directory_path)
terms = read_terms(tokens_path)
lemmas = read_lemma_forms(lemmas_path)


def process_documents(documents, terms):
    all_tokens_idf = calculate_all_idf(terms, documents)
    all_lemmas_idf = calculate_all_lemma_idf(lemmas, documents)

    for i, document in enumerate(documents):
        with open(f"{output_tokens_dir}/token_{i}.txt", "w") as tokens_file:
            for term in terms:
                tf = calculate_tf(term, document)
                idf = all_tokens_idf[term]
                tf_idf = tf * idf
                tokens_file.write(f"{term} {idf} {tf_idf}\n")

        with open(f"{output_lemmas_dir}/lemmas{i}.txt", "w") as lemmas_file:
            for j in lemmas:
                tf = calculate_lemma_tf(documents[i], lemmas[j])
                idf = all_lemmas_idf[j]
                tf_idf = tf * idf
                lemmas_file.write(f"{lemmas[j][0]} {idf} {tf_idf}\n")


process_documents(documents, terms)
