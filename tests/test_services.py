import pytest

from src.services import transactions_for_investment_bank, investment_bank


def test_transactions_for_investment_bank(fix_services):
    """Тестируем правильное добавление данных из транзакции"""
    assert transactions_for_investment_bank(fix_services) == [{"date": "2018-01-23", "amount": -284.0}]


def test_transactions_for_investment_bank_not_list():
    """Пустой список на вход"""
    assert transactions_for_investment_bank([]) == []


# def test_investment_bank_10(fix_investment_bank):
#     """ Тестируем копилку, округление до 10 """
#     assert investment_bank("2018-01", fix_investment_bank, 10) == 19.9


# def test_investment_bank_50(fix_investment_bank):
#     """ Тестируем копилку, округление до 50 """
#     assert investment_bank("2018-01", fix_investment_bank, 50) == 129.9


# def test_investment_bank_100(fix_investment_bank):
#     """ Тестируем копилку, округление до 100 """
#     assert investment_bank("2018-01", fix_investment_bank, 100) == 229.9


# def test_investment_bank_0_10(fix_0):
#     """ Тестируем копилку, округление до 10, если трата 0 """
#     assert investment_bank("2018-01", fix_0, 10) == 0


# def test_investment_bank_0_50(fix_0):
#     """ Тестируем копилку, округление до 50, если трата 0 """
#     assert investment_bank("2018-01", fix_0, 50) == 0


# def test_investment_bank_0_100(fix_0):
#     """ Тестируем копилку, округление до 100, если трата 0 """
#     assert investment_bank("2018-01", fix_0, 100) == 0
