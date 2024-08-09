import pytest
from unittest.mock import patch

from src.views import say_hello, mask_card_number



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

