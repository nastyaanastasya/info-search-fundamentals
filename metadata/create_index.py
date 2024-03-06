import os
from glob import glob
import re
import html2text
import spacy

DIR = "crawler/pages/"
webs_pl = glob(f"{DIR}/**.html")
LEMMAS_FILE = "tokens/lemmas.txt"
TOKENS_FILE = "tokens/tokens.txt"
index_output_file_name = "inverted_index.txt"

lemmas_map = dict()
index = dict()
file = open(LEMMAS_FILE, 'r')
lines = file.readlines()


class InvertedIndex:
    def __init__(self, lemma):
        self.lemma = lemma
        self.count = 0
        self.files = set()

    def add_count(self, count):
        self.count += count

    def add_file(self, file_idx):
        self.files.add(file_idx)
        self.count += 1

    def __repr__(self):
        return f"InvertedIndexEntry(lemma = '{self.lemma}', count = {self.count}, files = {sorted(self.files)})"


for line in lines:
    tokens = re.split('\\s+', line)
    lemma = tokens[0]
    lemmas_map[lemma] = []
    for i in range(1, len(tokens) - 1):
        token = tokens[i]
        if not len(token.strip()) == 0:
            lemmas_map[lemma].append(token)

file.close()

h2t = html2text.HTML2Text()
h2t.ignore_links = True

nlp = spacy.load("ru_core_news_sm")


def get_tokens(text):
    return [w for w in nlp(text) if (w.is_alpha and not w.is_stop)]


for pl in webs_pl:
    with open(pl, "r") as file:
        file_idx_match = re.search(r'.*_(\d+)\.html', os.path.basename(pl))
        file_idx = int(file_idx_match.group(1))
        file_content = file.read()
        file_text = h2t.handle(file_content)
        file_tokens = get_tokens(file_text)

        for token in file_tokens:
            lemma = token.lemma_
            if lemma in lemmas_map.keys():
                if lemma not in index.keys():
                    index[lemma] = InvertedIndex(lemma)
                index[lemma].add_file(file_idx)


with open(index_output_file_name, "w") as f:
    for index_entry in index.values():
        sorted_files = sorted(index_entry.files)
        f.write(f"{index_entry.lemma}[{index_entry.count}] {' '.join(map(str, sorted_files))}\n")
