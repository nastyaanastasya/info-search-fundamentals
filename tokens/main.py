import os
import re

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pymorphy2 import MorphAnalyzer


def group_tokens(tokens):
    morph = MorphAnalyzer()

    lemmas = {}
    for token in tokens:
        lemma = morph.parse(token)[0].normal_form
        if lemma not in lemmas:
            lemmas[lemma] = []
        lemmas[lemma].append(token)
    return lemmas


def clean_token(token):
    return re.sub("[^а-яА-ЯёЁ]", '', token)


def get_clean_tokens(file_path, stop_words):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        tokens = word_tokenize(soup.get_text())
        cleaned_tokens = [clean_token(token.lower()) for token in tokens if token not in stop_words and len(token) > 1]
        return cleaned_tokens


def get_tokens_from_files(directory, stop_words):
    html_files = [file for file in os.listdir(directory) if file.endswith('.html')]

    all_tokens = []
    for file_name in html_files:
        clean_tokens = get_clean_tokens(
            os.path.join(directory, file_name),
            stop_words
        )
        all_tokens.extend(clean_tokens)
    return set(all_tokens)


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().split()


# write tokens to file [tokens.txt]
stop_words = set(stopwords.words('russian'))
files_tokens = get_tokens_from_files(
    directory='../crawler/pages',
    stop_words=stop_words
)
with open('tokens.txt', 'w') as token_file:
    for token in files_tokens:
        token_file.write(f"{token}\n")

# write tokens grouped by lemmas to file [lemmas.txt]
grouped_tokens = group_tokens(
    read_file('tokens.txt')
)
with open('lemmas.txt', 'w') as lemma_file:
    for lemma, token_list in grouped_tokens.items():
        lemma_file.write(f"{lemma} {' '.join(token_list)}\n")
