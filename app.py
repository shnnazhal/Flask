from flask import Flask, render_template, request
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
        response_1 = requests.get(EXTERNAL_API_URL, params=params_page_1)
        response_1.raise_for_status()  # смотрит какой статус выполнения 200 успешно 404 не найден 500 ошибка сервера
        data_page_1 = response_1.json().get("items", [])  # преобразовывает в пайтон словарь из джсона

        # Получение второй страницы
        response_2 = requests.get(EXTERNAL_API_URL, params=params_page_2)
        response_2.raise_for_status()
        data_page_2 = response_2.json().get("items", [])

        # Объединяем данные из двух страниц в один список
        combined_data = data_page_1 + data_page_2

    # При ошибке
    except requests.exceptions.RequestException as e:
        print(f"Ошибка {e}")
        combined_data = []

    # Сортируем персонажей по полу
    sorted_characters = sorted(combined_data, key=lambda x: x.get("gender", "UNKNOWN"))

    # Загружаем HTML-шаблон и передаем переменную characters в шаблон как posts
    return render_template('index.html', posts=sorted_characters)

# просто чтобы пайтон понимал какой нужно запускать хтмл файл
@app.route('/send-names')
def send_names():
    return render_template('send_names.html')

# маршрут для отправки емайл (чтобы по нажатию кнопки происъодила отправка письма
@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        # делаем тоже самое что и выше
        params_page_1 = {'page': 1}
        params_page_2 = {'page': 2}

        response_1 = requests.get(EXTERNAL_API_URL, params=params_page_1)
        response_1.raise_for_status()
        data_page_1 = response_1.json().get("items", [])

        response_2 = requests.get(EXTERNAL_API_URL, params=params_page_2)
        response_2.raise_for_status()
        data_page_2 = response_2.json().get("items", [])

        combined_data = data_page_1 + data_page_2

        # извлекаем имеа персонажей из переменной combined_data а тоесть с апи
        names = [character.get("name", "Неизвестно") for character in combined_data]

        #join(names) обьеденяет все елементы со списка names в единую строку а \n делает чтобы каждый елемент был на новой строке
        names_str = "\n".join(names)

        # Настройки email
        sender_email = "name@gmail.com"
        receiver_email = "name@gmail.com"
        password = "password"

        # создание вида сообщения
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "Список персонажей Futurama со страницы 1 и 2"
#указываем что будет находитьсся в теле письма f"Список персонажей Futurama:\n{names_str}
        body = f"Список персонажей Futurama:\n{names_str}"

        #message.attach() добавляет текст созданный в body в письмо а "plain" обозначает что это простой текст без хтмл стилей
        message.attach(MIMEText(body, "plain"))

        # соеденения с SMPT-сервером
        with smtplib.SMTP("smtp.gmail.com", 587) as server:

            #шифрование
            server.starttls()

            #авторизация с использыванием логина и пароля который указан выше в переменной
            server.login(sender_email, password)

            #отправка письма. message.as_string()) строка преобразована в формат string
            server.sendmail(sender_email, receiver_email, message.as_string())

        return "Email успешно отправлен!"
    except Exception as e:
        return f"Ошибка при отправке email: {e}"

# отладка
if __name__ == '__main__':
    app.run(debug=True)