import pandas as pd
import pytest
from unittest.mock import patch
import datetime
import os
from src.utils import (
    say_hello,
    mask_card_number,
    get_total_amount_expenses,
    show_cashback,
    show_transactions_top_5,
    show_currency_rates_data,
    get_data_from_excel_df,
    get_data_from_excel
)


PATH_TO_FILE_EMPTY = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "emptyr.xlsx")
PATH_TO_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "df_1.xlsx")


# @patch('src.utils.datetime')
# @pytest.mark.parametrize("hour, greeting",
#                          [
#                              (7, "Доброе утро"),
#                              (13, "Добрый день"),
#                              (19, "Добрый вечер"),
#                              (2, "Доброй ночи")
#                          ])
# def test_say_hello_day(mock_datetime, hour, greeting):
#     mock_now = datetime.datetime(2023, 6, 20, hour, 0, 0)
#     mock_datetime.now.return_value = mock_now
#     result = say_hello()
#     assert result == greeting


# def test_mask_card_number(df):
#     """Проверяем работу функции на различных входных форматах номеров карт"""
#     assert mask_card_number(df) == ['*7197']


# def test_get_total_amount_expenses(amount_expenses):
#     """Тестируем суммирование трат по определенной карте"""
#     assert get_total_amount_expenses(amount_expenses, "*7197") == 621.0


# def test_get_total_amount_expenses_not_card(amount_expenses):
#     """Тестируем суммирование трат, если такой карты нету"""
#     assert get_total_amount_expenses(amount_expenses, 197) == 0


# def test_get_total_amount_expenses_not_transactions():
#     """Тестируем суммирование трат, если транзакций нету"""
#     assert get_total_amount_expenses([], 7197) == 0


# def test_get_total_amount_expenses_not_number_card(amount_expenses):
#     """Тестируем суммирование трат, если номер карты отсутствует"""
#     assert get_total_amount_expenses(amount_expenses, "") == 0


@pytest.mark.parametrize(
    "enter_value, expected_result",
    [
        (317.0, 3.17),
        (10, 0.1),
        (1256.55, 12.57),
        (0.17, 0.0),
        (0.0, 0.0),
        (0, 0.0),
    ],
)
def test_show_cashback(enter_value, expected_result):
    """Тестируем правильный расчет кэшбэка"""
    assert show_cashback(enter_value) == expected_result


def test_show_transactions_top_5(amount_expenses):
    """Тестируем выдачу 5 самых больших трат в нужном формате"""
    assert show_transactions_top_5(amount_expenses) == [
        {
            "date": "24.01.2018",
            "amount": -115909.42,
            "category": "Переводы",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
        {"date": "04.01.2018", "amount": -316.0, "category": "Красота", "description": "OOO Balid"},
        {"date": "25.01.2018", "amount": -284.0, "category": "Транспорт", "description": "Яндекс Такси"},
        {"date": "10.01.2018", "amount": -250.0, "category": "Связь", "description": "МТС"},
        {"date": "05.01.2018", "amount": -21.0, "category": "Красота", "description": "OOO Balid"},
    ]


def test_show_transactions_top_5_not_transactions():
    """Тестируем, если транзакции отсутствуют"""
    assert show_transactions_top_5([]) == []


def test_show_transactions_top_5_2(trans_2):
    """Тестируем, если транзакции всего 2"""
    assert show_transactions_top_5(trans_2) == [
        {"date": "04.01.2018", "amount": -316.0, "category": "Красота", "description": "OOO Balid"},
        {"date": "05.01.2018", "amount": -21.0, "category": "Красота", "description": "OOO Balid"},
    ]


# @patch("src.views.response")
# def test_show_currency_rates_data(mock_get):
#     """ Тест курса валют """
#     mock_get.return_value.status_code = 200
#     mock_get.return_value.json.return_value = {'success': True, 'timestamp': 1723358944, 'base': 'USD', 'date': '2024-08-11', 'rates': {'RUB': 86.80366}}
#     result = show_currency_rates_data()
#     assert result == [{'currency': {'USD'}, 'rate': 86.8}]

def test_get_data_from_excel_df():
    """ Тест, если файл не найден """
    assert get_data_from_excel_df(PATH_TO_FILE_EMPTY) == []


# def test_get_data_from_excel_df_read():
#     """ Тест на считывание DataFrame """
#     assert get_data_from_excel_df(PATH_TO_FILE) ==


def test_get_data_from_excel():
    """ Тест, если файл не найден """
    assert get_data_from_excel(PATH_TO_FILE_EMPTY) == []


def test_get_data_from_excel_read():
    """ Тест на считывание DataFrame """
    assert get_data_from_excel(PATH_TO_FILE) == [{'Unnamed: 0': 0, 'Дата операции': '18.12.2021 16:53:16', 'Дата платежа': '20.12.2021', 'Номер карты': '*7197', 'Статус': 'OK', 'Сумма операции': -176, 'Валюта операции': 'RUB', 'Сумма платежа': -176, 'Валюта платежа': 'RUB', 'Кэшбэк': nan, 'Категория': 'Топливо', 'MCC': 5541, 'Описание': 'ЛУКОЙЛ', 'Бонусы (включая кэшбэк)': 3, 'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 176}]

# df = pd.DataFrame({"Дата операции": ["18.12.2021 16:53:16"], "Дата платежа": ["20.12.2021"], "Номер карты": ["*7197"], "Статус": ["OK"], "Сумма операции": [-176.0], "Валюта операции": ["RUB"], "Сумма платежа": [-176.0], "Валюта платежа": ["RUB"], "Кэшбэк": ["NaN"], "Категория": ["Топливо"], "MCC": [5541.0], "Описание": ["ЛУКОЙЛ"], "Бонусы (включая кэшбэк)": [3], "Округление на инвесткопилку": [0], "Сумма операции с округлением": [176.0]})
# df.to_excel(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "df_1.xlsx"))