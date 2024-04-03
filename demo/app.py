from flask import Flask, render_template, request

from search.search_system import process_query

LINK_PREFIX = 'https://vc.ru/hr/'
app = Flask(__name__)


def convert_search_result_to_links(search_result):
    if search_result is not None and search_result:
        links = []
        for item in search_result:
            name = item.replace('.html', '').replace('lemmas', '')
            link = f"{LINK_PREFIX}{name}"
            links.append(link)
        return links
    else:
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_value = request.form['input_value']
        result = process_query(input_value)
        links_result = convert_search_result_to_links(result)
        if links_result is not None:
            return render_template('result.html', input_value=input_value, result=links_result)
        else:
            return render_template('error.html', input_value=input_value)
    else:
        return '''<html>
                    <head>
                        <title>Страница ввода запроса</title>
                    </head>
                    <body>
                        <h1>Введите запрос:</h1>
                        <form action="/" method="POST">
                            <input type="text" name="input_value">
                            <br><br>
                            <input type="submit" value="Поиск">
                        </form>
                    </body>
                </html>'''

if __name__ == '__main__':
    app.run(port=8000)