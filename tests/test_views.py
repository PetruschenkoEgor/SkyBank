import pytest
from unittest.mock import patch

from src.views import say_hello, mask_card_number, get_total_amount_expenses, show_cashback



# @patch('src.views.say_hello')
# def test_say_hello_day(mock_time):
#     mock_time.return_value = 13
#     assert say_hello() == "Добрый день"


@pytest.mark.parametrize("enter_value, expected_result",
                         [
                             (7000792289606361, "6361"),
                             ("7000792289606361", "6361"),
                             ("**6361", "6361"),
                             (6361, "6361"),
                             ("6361", "6361"),
                             (636, "Некорректный номер карты!"),
                             ("", "Некорректный номер карты!"),
                             (" ", "Некорректный номер карты!"),
                             ("jhgfdsaeyudhfydt", "Некорректный номер карты!")
                         ])
def test_mask_card_number(enter_value, expected_result):
    """Проверяем работу функции на различных входных форматах номеров карт"""
    assert mask_card_number(enter_value) == expected_result


def test_get_total_amount_expenses(amount_expenses):
    """ Тестируем суммирование трат по определенной карте """
    assert get_total_amount_expenses(amount_expenses, '*7197') == 337.0


def test_get_total_amount_expenses_not_card(amount_expenses):
    """ Тестируем суммирование трат, если такой карты нету """
    assert get_total_amount_expenses(amount_expenses, 197) == 0


def test_get_total_amount_expenses_not_transactions():
    """ Тестируем суммирование трат, если транзакций нету """
    assert get_total_amount_expenses([], 7197) == 0


def test_get_total_amount_expenses_not_number_card(amount_expenses):
    """ Тестируем суммирование трат, если номер карты отсутствует """
    assert get_total_amount_expenses(amount_expenses, "") == 0


@pytest.mark.parametrize("enter_value, expected_result",
[
    (317.0, 3.17),
    (10, 0.1),
    (1256.55, 12.57),
    (0.17, 0.0),
    (0.0, 0.0),
    (0, 0.0),
])
def test_show_cashback(enter_value, expected_result):
    """ Тестируем правильный расчет кэшбэка """
    assert show_cashback(enter_value) == expected_result


