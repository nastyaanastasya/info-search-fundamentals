import re

inv_index_file_name = "inverted_index.txt"
files_total_count = 151
all_files_set = set(range(1, files_total_count))
all_files_set_var_name = "all_files_set"


class InvertedIndex:
    def __init__(self, lemma, count, files):
        self.lemma = lemma
        self.count = count
        self.files = files

    def __repr__(self):
        return f"InvertedIndexEntry(lemma = '{self.lemma}', count = {self.count}, files = {sorted(self.files)})"


inv_index = dict()
inv_index_var_name = "inv_index"


with open(inv_index_file_name, 'r', encoding="utf-8") as file:
    lines = file.readlines()
    for line in lines:
        pattern = r'(\w+)\[(\d+)\]\s+([\w\s]+)'
        match = re.match(pattern, line)

        lemma = match.group(1)
        count = int(match.group(2))
        files = [int(num) for num in match.group(3).split(' ')]

        inv_index_entry = InvertedIndex(lemma, count, set(files))

        inv_index[lemma] = inv_index_entry

CLOSE = ')'
OPEN = '('

AND_REPLACE = ").intersection("
OR_REPLACE = ").union("
NOT_REPLACE = ").difference("

OR = 'or'
NOT = 'not'
AND = 'and'



def next_is_word(current_i, query_words):
    next_i = current_i + 1

    if next_i == len(query_words):
        return False

    next_word = query_words[next_i]

    return not next_word in (OR, NOT, AND, CLOSE, OPEN)


def boolean_search(initial_query, inverted_index):
    initial_query = initial_query.replace(OPEN, f" {OPEN} ").replace(CLOSE, f" {CLOSE} ")
    initial_query = initial_query.replace(OR, f" {OR} ").replace(NOT, f" {NOT} ").replace(AND, f" {AND} ")
    query_words = initial_query.strip().lower().split(' ')
    query_words = list(filter(lambda x: x != "", query_words))

    i = 0
    query = OPEN

    for word in query_words:
        if word == '':
            query = query
        elif word == OPEN:
            query += OPEN
        elif word == CLOSE:
            query += CLOSE
        elif word == OR:
            query += OR_REPLACE
        elif word == AND:
            query += AND_REPLACE
        elif word == NOT:
            if next_is_word(i, query_words):
                query += f'{all_files_set_var_name}.difference('
            else:
                query += NOT_REPLACE
        else:
            token = word
            if token in inv_index.keys():
                query += f'{inv_index_var_name}["{token}"].files'
            else:
                query += f'set()'
        i += 1

    query += CLOSE

    return sorted(eval(query))


while True:
    user_input = input("Введите запрос:\n")
    if user_input.lower() == 'exit':
        break
    test_query = user_input.lower()
    try:
        result = boolean_search(test_query, inv_index)
        print(f'Результат = {result}')
    except:
        try:
            result = boolean_search(test_query + ')', inv_index)
            print(f'Результат = {result}')
        except:
            print("Неправильное значение. Пожалуйста, введите запрос еще раз")
