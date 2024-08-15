import datetime
import json
import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv

# Загрузка переменных из файла .env
load_dotenv()

# Путь к файлу EXCEL
PATH_TO_FILE_EXCEL = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.xlsx")

# Файл, в который сохраняются логи
PATH_TO_FILE_FILE_HANDLER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "utils.log")

# Файл с пользовательскими настройками
USERS_SETTINGS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "users_settings.json")

# Самая свежая дата в таблице
TODAY = "31.12.2021"

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(PATH_TO_FILE_FILE_HANDLER, "w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_data_from_excel(path_to_file: str) -> list:
    """Функция получает путь к файлу и возвращает список словарей"""
    try:
        logger.info("Считывание EXCEL-файла")
        # Считываем Excel-файл
        transactions_excel = pd.read_excel(path_to_file)

        logger.info("Преобразование полученных данных в список словарей")
        # Преобразуем полученные данные в список словарей
        transactions_list_dicts = transactions_excel.to_dict(orient="records")

        return transactions_list_dicts
    except FileNotFoundError:
        logger.error("Ошибка: файл не найден")
        return []


# if __name__ == "__main__":
#     print(get_data_from_excel(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "df_1.xlsx")))


def get_data_from_excel_df(path_to_file: str) -> pd.DataFrame | list:
    """Функция получает путь к файлу и возвращает DataFrame"""
    try:
        logger.info("Считывание EXCEL-файла")
        # Считываем Excel-файл
        transactions_excel = pd.read_excel(path_to_file)

        return transactions_excel
    except FileNotFoundError:
        logger.error("Ошибка: файл не найден")
        return []


# if __name__ == '__main__':
#     print(get_data_from_excel_df(PATH_TO_FILE_EXCEL))


def say_hello():
    """Функция принимает строку со временем и здоровается в зависимости от времени суток"""
    logger.info("Получаем текущее время")
    # Текущее время
    current_time = datetime.datetime.now()

    logger.info("Получаем часы и переводим их в число")
    # Получаем часы и переводим их в число
    time = current_time.hour

    # В зависимости от времени здороваемся
    if 6 <= time <= 11:
        logger.info("Приветствие: Доброе утро")
        hello = "Доброе утро"
    elif 12 <= time <= 17:
        logger.info("Приветствие: Добрый день")
        hello = "Добрый день"
    elif 18 <= time <= 22:
        logger.info("Приветствие: Добрый вечер")
        hello = "Добрый вечер"
    else:
        logger.info("Приветствие: Доброй ночи")
        hello = "Доброй ночи"

    return hello


# if __name__ == '__main__':
#     print(say_hello())


def mask_card_number(transactions: pd.DataFrame) -> list:
    """Маскирует номер карты(показывает 4 последние цифры)"""
    logger.info("Удаление значений nan")
    # Убираем значения nan из столбца "Номер карты"
    transactions_not_nan = transactions.loc[transactions["Номер карты"].notnull()]

    logger.info("Получение список уникальных номеров карт")
    # Получаем список уникальных номеров карт
    number_card = transactions_not_nan.loc[:, "Номер карты"].unique()

    return number_card


# if __name__ == "__main__":
#     print(mask_card_number(get_data_from_excel_df(PATH_TO_FILE_EXCEL)))


def show_cashback(expenses: float) -> float:
    """Функция считает кэшбэк(1 рубль за каждые 100 рублей)"""
    logger.info("Рассчет и округление кэшбэка")
    # Рассчитываем кэшбэк и округляем до двух цифр после запятой
    cashback = round(expenses * 0.01, 2)
    return cashback


def get_total_amount_expenses(transactions: pd.DataFrame, number_card: list, date: str = TODAY) -> list[dict]:
    """Общая сумма расходов"""
    logger.info("Определение конечного значения даты")
    date_ = f"{date} 00:00:00"
    # Конечное значение(до какой даты происходит поиск)
    end = datetime.datetime.strptime(date_, "%d.%m.%Y %H:%M:%S")
    date_time = f"{str(end)[5:7]}.{str(end)[:4]} 00:00:00"
    logger.info("Определение начального значения даты")
    # Начальное значение(с какой даты начинается поиск)
    start = datetime.datetime.strptime(f"01.{date_time}", "%d.%m.%Y %H:%M:%S")

    logger.info("Создание дополнительного столбца с датой в формате datetime")
    # Создаем новый столбец "date", в него записываем дату операции в формате объект datetime
    transactions["date"] = transactions["Дата операции"].map(
        lambda x: datetime.datetime.strptime(str(x), "%d.%m.%Y %H:%M:%S")
    )
    logger.info("Выборка нужных строк по фильтру")
    # Делаем выборку нужных нам строк(чтобы дата была в нужном промежутке и была нужная категория)
    amount_expenses = transactions.loc[(transactions["date"] <= end) & (transactions["date"] >= start)]

    # Полученные данные преобразуем в список словарей(выборка транзакций с нужной датой)
    transactions_list_dicts = amount_expenses.to_dict(orient="records")

    # Список для словарей с готовыми данными(добавляем в него с помощью цикла)
    amount_list = []
    for number in number_card:
        # Список, в который попадают все операции по определенной карте
        sum_list = []

        # Инициализация словаря
        dict_amount = dict()
        # Добавление номера карты в словарь
        dict_amount["last_digits"] = number

        amount_list.append(dict_amount)
        for tr in transactions_list_dicts:
            # Проверяем - операция относится к данной карте, статус - ок, не входит в указанные категории
            # и со знаком минус
            if (
                str(tr.get("Номер карты")) == number
                and tr.get("Статус") == "OK"
                and tr.get("Категория") not in ["Переводы", "Пополнения", "Другое", "Бонусы", "Наличные"]
                and float(tr.get("Сумма платежа")) < 0
            ):
                logger.info("Добавление в список суммы платежа")
                sum_list.append(tr.get("Сумма платежа"))

        logger.info("Рассчет суммы расходов по определенной карте и добавление в словарь")
        # Добавление в словарь трат по определенной карте
        dict_amount["total_spent"] = round(abs(sum(sum_list)), 2)

        # Общие траты по определенной карте
        total_spent = dict_amount.get("total_spent")
        # Вызываем функцию расчета кэшбэка
        cash_back = show_cashback(total_spent)

        dict_amount["cashback"] = cash_back

    return amount_list


# if __name__ == '__main__':
#     print(get_total_amount_expenses(get_data_from_excel_df(PATH_TO_FILE_EXCEL),
#                                     mask_card_number(get_data_from_excel_df(PATH_TO_FILE_EXCEL))))


def show_transactions_top_5(transactions: list[dict]) -> list[dict]:
    """Показывает топ 5 транзакций по сумме платежа"""
    logger.info("Сортировка транзакций по сумме платежа")
    # Сортируем транзакции по тратам(от большего к меньшему)
    sorted_trans = sorted(transactions, key=lambda x: x.get("Сумма платежа"))

    # Сщздаем пустой список, куда будем накидывать топ транзакций и счетчик, для подсчета кол-ва транзакций
    top_5 = []
    count = 0
    for transaction in sorted_trans:
        logger.info("Добавление транзакций в список, пока их не станет 5")
        # Добавляем транзакции в список, пока их не станет 5
        if count < 5:
            dict_trans = dict()
            dict_trans["date"] = transaction.get("Дата платежа")
            dict_trans["amount"] = transaction.get("Сумма платежа")
            dict_trans["category"] = transaction.get("Категория")
            dict_trans["description"] = transaction.get("Описание")
            top_5.append(dict_trans)
            count += 1

    return top_5


# if __name__ == '__main__':
#     print(show_transactions_top_5(get_data_from_excel(PATH_TO_FILE_EXCEL)))


# def show_currency_rates_data(file: str = USERS_SETTINGS) -> list[dict] | str:
#     """Показывает курс валют"""
#     # Список словарей с курсом валют usd, eur
#     currency_list = []
#
#     logger.info("Открытие файла с пользовательскими настройками")
#     # Открываем json-файл с пользовательскими настройками
#     with open(file) as f:
#         data = json.load(f)
#
#     # url = "https://api.apilayer.com/exchangerates_data/latest"
#     # Получение значения переменной API_KEY из .env-файла
#     headers = os.getenv("API_KEY_CURRENCY_RATES")
#
#     try:
#         for ticker in data.get("user_currencies"):
#             # Получение курса USD
#             payload = {"symbols": ["RUB"], "base": ticker}
#             url = "https://api.apilayer.com/exchangerates_data/latest"
#             logger.info("Выполнение get-запроса на получение курса валют")
#             response = requests.get(url, headers=headers, data=payload)
#             logger.info("Получение статус-кода get-запроса на получение курса валют")
#             # Получаем статус запроса
#             status_code = response.status_code
#
#             if status_code == 200:
#                 logger.info("Получение курса валют и округление до 2 цифр после запятой")
#                 result = response.json().get("rates")
#                 result = round(result.get("RUB"), 2)
#
#                 logger.info("Добавление курсов валют")
#                 # Создаем пустой словарь для курса валют и добавляем в него данные
#                 dict_currency = dict()
#                 dict_currency["currency"] = {ticker}
#                 dict_currency["rate"] = result
#                 # Добавляем словарь в список
#                 currency_list.append(dict_currency)
#             else:
#                 logger.error(f"Ошибка get-запроса получения курса валют. Статус код: {status_code}")
#                 return f"Произошла ошибка! Статус-код: {status_code}"
#
#         return currency_list
#     except requests.exceptions.RequestException as e:
#         logger.error(f"Ошибка get-запроса получения курса валют. Ошибка: {e}")
#         return f"Ошибка: {e}"


def show_currency_rates_data():
    """Показывает курс валют"""
    api_key = os.getenv("API_KEY_CURRENCY_RATES")
    response = requests.get(
        f"https://currate.ru/api/?get=rates&pairs=USDRUB,EURRUB&key={api_key}")
    status_code = response.status_code
    if status_code == 200:
        result = response.json()
        rate_usd = dict()
        rate_usd["currency"] = "USD"
        usd = round(float((result.get("data")).get("USDRUB")), 2)
        rate_usd["rate"] = usd
        rate_eur = dict()
        rate_eur["currency"] = "EUR"
        eur = round(float((result.get("data")).get("EURRUB")), 2)
        rate_eur["rate"] = eur
        rate_list = []
        rate_list.append(rate_usd)
        rate_list.append(rate_eur)
        return rate_list
    else:
        return f"Ошибка: статус_код {status_code}"


# if __name__ == '__main__':
#     print(show_currency_rates_data())


def show_stock_prices_data_sp500(file: str = USERS_SETTINGS) -> list[dict] | str:
    """Показывает стоимость акций из S&P 500"""
    # Создаем пустой список для словарей с ценами на акции
    prices = []

    logger.info("Открытие файла с пользовательскими настройками")
    # Открываем json-файл с пользовательскими настройками
    with open(file) as f:
        data = json.load(f)

    # Получение значения переменной API_KEY из .env-файла
    apikey = os.getenv("API_KEY_STOCK_PRICE")

    try:
        # Подставляем каждый тикер в get-запрос
        for ticker in data.get("user_stocks"):
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={apikey}"
            logger.info("Выполнение get-запроса на получение цен на акции")
            response = requests.get(url)
            logger.info("Получение статус-кода на получение цен на акции")
            # Получаем статус запроса
            status_code = response.status_code

            if status_code == 200:
                # Получаем эту строку, если API запросы закончились
                info = "Thank you for using Alpha Vantage! Our standard API rate limit is 25 requests per day."
                # Проверяем, что API запросы у нас не закончились
                if info != response.json().get("Information"):
                    logger.info("Получение цен на акции")
                    # Получаем нужные нам значения из полученных данных
                    result = response.json().get("Global Quote")

                    logger.info("Добавление цен на акции")
                    # Создаем пустой словарь и добавляем в него данные
                    price_dict = dict()
                    price_dict["stock"] = ticker
                    price_dict["rate"] = round(float(result.get("05. price")), 2)
                    # Добавляем словарь в список
                    prices.append(price_dict)
                # Сообщение о том, что API запросы закончились
                else:
                    logger.error("Запросы на получение API на сегодня закончились")
                    return "Запросы на сегодня закончились! Приходите завтра! В день разрешено 25 запросов!"
            # Произошла ошибка
            else:
                logger.error(f"Ошибка get-запроса получения курса акций. Статус код: {status_code}")
                return f"Произошла ошибка! Статус-код: {status_code}"

        return prices
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка get-запроса получения курса акций. Ошибка: {e}")
        return f"Ошибка: {e}"


# if __name__ == '__main__':
#     print(show_stock_prices_data_sp500())
