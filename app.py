# render_template позволяет загружать HTML-файлы
# requests помогает отправлять HTTP-запросы
from flask import Flask, render_template
import requests

# запускаем файл он будет называться app
app = Flask(__name__)

# Берем данные с сайта Futurama
EXTERNAL_API_URL = 'https://futuramaapi.com/api/characters'


# Создаем путь / , а home — это домашний экран
@app.route('/')
def home():
    try:
        # параметры для первой и второй страницы
        params_page_1 = {'page': 1}
        params_page_2 = {'page': 2}

        # Получение первой страницы

        #получение запроса по параметру который был указан выше
        response_1 = requests.get(EXTERNAL_API_URL, params=params_page_1)

       #смотрит какой статус выполнения 200 успешно 404 не найден 500 ошибка сервера
        response_1.raise_for_status()

        #преобразовывает в пайтон словарь из джсона
        data_page_1 = response_1.json()  # JSON данных страницы 1

        #получаем из джсона страницу 1 если ключа нету вернеться пустой список
        data_page_1 = data_page_1.get("items", [])  # Берем данные из ключа "items"

        # Получение второй страницы
        response_2 = requests.get(EXTERNAL_API_URL, params=params_page_2)
        response_2.raise_for_status()
        data_page_2 = response_2.json()  # JSON данных страницы 2
        data_page_2 = data_page_2.get("items", [])  # Берем данные из ключа "items"

        # Объединяем данные из двух страниц в один список
        combined_data = data_page_1 + data_page_2  # Добавляем вторую страницу к первой

    # При ошибке
    except requests.exceptions.RequestException as e:
        print(f"Ошибка {e}")
        # список персонажей
        combined_data = []

    # передаю переменную characters в функцию sorted с ключом lambda, который задает способ сортировки
    # в данном случае простой и потом указываю, по какому критерию сортировать
    sorted_characters = sorted(combined_data, key=lambda x: x.get("gender", "UNKNOWN"))

    # Этот файл говорит загрузить HTML-шаблон (который в папке templates) и передает переменную characters
    # в этот шаблон как posts
    return render_template('index.html', posts=sorted_characters)


# отладка
if __name__ == '__main__':
    app.run(debug=True)