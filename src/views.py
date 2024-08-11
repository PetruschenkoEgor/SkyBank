import datetime
import requests
from src.utils import get_data_from_excel, PATH_TO_FILE_EXCEL


def say_hello():
    """ Функция принимает строку со временем и здоровается в зависимости от времени суток """
    # Текущее время
    current_time = str(datetime.datetime.now())[11:16]

    # Получаем часы и переводим их в число
    time = int(current_time[:2])

    # В зависимости от времени здороваемся
    if 6 <= time <= 11:
        hello = "Доброе утро"
    elif 12 <= time <= 17:
        hello = "Добрый день"
    elif 18 <= time <= 22:
        hello = "Добрый вечер"
    else:
        hello = "Доброй ночи"

    return hello


# if __name__ == '__main__':
#     print(say_hello())


def mask_card_number(number_card: str | int) -> str:
    """ Маскирует номер карты(показывает 4 последние цифры) """
    number_card_str = str(number_card)

    # Проверяем корректность введенного номера карты
    if len(number_card_str) < 4 or not number_card_str[-4:].isdigit():
        result = "Некорректный номер карты!"
    else:
        # Делаем маску номера, заменяем часть строки подстрокой
        result = number_card_str[-4:]

    return result


# if __name__ == "__main__":
#     print(mask_card_number("fdavrgvae"))


def get_total_amount_expenses(transactions: list[dict], number_card: str | int) -> float:
    """ Общая сумма расходов """
    # Список, в который попадают все операции по карте
    sum_list = []
    for tr in transactions:
        # Проверяем - операция относится к данной карте, статус - ок, не входит в указанные категории и со знаком минус
        if (str(tr.get("Номер карты"))[-4:] == str(number_card)[-4:] and tr.get("Статус") == "OK"
                and tr.get("Категория") not in ["Переводы", "Пополнения", "Другое", "Бонусы", "Наличные"]
                and float(tr.get("Сумма платежа")) < 0):
            sum_list.append(tr.get("Сумма платежа"))

    # Суммируем список
    sum_list = sum(sum_list)
    return -sum_list


# if __name__ == '__main__':
#     print(get_total_amount_expenses(get_data_from_excel(PATH_TO_FILE_EXCEL), 4556))


def show_cashback(expenses: float) -> float:
    """ Функция считает кэшбэк(1 рубль за каждые 100 рублей) """
    # Округляем кэшбэк до двух цифр после запятой
    cashback = round(expenses * 0.01, 2)
    return cashback


# if __name__ == '__main__':
#     print(show_cashback(get_total_amount_expenses(get_data_from_excel(PATH_TO_FILE_EXCEL), "**7197")))


def show_transactions_top_5(transactions: list[dict]) -> list[dict]:
    """ Показывает топ 5 транзакций по сумме платежа """
    # Сортируем транзакции по тратам(от большего к меньшему)
    sorted_trans = sorted(transactions, key=lambda x: x.get("Сумма платежа"))

    # Сщздаем пустой список, куда будем накидывать топ транзакций и счетчик, для подсчета кол-ва транзакций
    top_5 = []
    count = 0
    for transaction in sorted_trans:
        # Накидываем транзакции в список, пока их не станет 5
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


def show_currency_rates_data():
    """ Показывает курс валют """
    url = "https://api.apilayer.com/exchangerates_data/latest"
    headers = {"apikey": "4kvX6s69BemzZNZ2DWO17p0PAMcl01Tr"}

    # Получение курса USD
    payload = {
        "symbols": "RUB",
        "base": "USD"
    }
    # response_usd = requests.get(url, headers=headers, params=payload)
    # status_code = response_usd.status_code
    # result_u = response_usd.json().get("rates")
    # result_usd = round(result_u.get("RUB"), 2)

    # Получение курса EUR
    payload = {
        "symbols": "RUB",
        "base": "EUR"
    }
    # response_usd = requests.get(url, headers=headers, params=payload)
    # status_code = response_usd.status_code
    # result_e = response_usd.json().get("rates")
    # result_eur = round(result_e.get("RUB"), 2)

    # Список словарей с курсом валют usd, eur
    currency_list = []

    # Создаем пустые словари для курса валют
    dict_usd = dict()
    dict_eur = dict()

    # Добавляем в словарь курс доллара
    dict_usd["currency"] = "USD"
    dict_usd["rate"] = result_usd
    # Добавляем словарь в список
    currency_list.append(dict_usd)

    #Добавляем в словарь курс евро
    dict_eur["currency"] = "EUR"
    dict_eur["rate"] = result_eur
    # Добавляем словарь в список
    currency_list.append(dict_eur)

    return currency_list


# if __name__ == '__main__':
#     print(show_currency_rates_data())


def show_stock_prices_data_sp500():
    """ Показывает стоимость акций из S&P 500 """
    url = "https://financialmodelingprep.com/api/v4/search/isin?isin=US0378331005&apikey=TKkLZFI8RhNVVQ8DUCBNiqRcvjcHkC4z"
    headers = {"apikey": "TKkLZFI8RhNVVQ8DUCBNiqRcvjcHkC4z"}
    response_usd = requests.get("https://financialmodelingprep.com/api/v4/search/isin?isin=US0378331005&apikey=TKkLZFI8RhNVVQ8DUCBNiqRcvjcHkC4z")
    result = response_usd.json()
    return result


if __name__ == '__main__':
    print(show_stock_prices_data_sp500())
