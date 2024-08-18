import pytest

from src.services import investment_bank, transactions_for_investment_bank


def test_transactions_for_investment_bank(fix_services):
    """Тестируем правильное добавление данных из транзакции"""
    assert transactions_for_investment_bank(fix_services) == [{"date": "2018-01-23", "amount": -284.0}]


def test_transactions_for_investment_bank_not_list():
    """Пустой список на вход"""
    assert transactions_for_investment_bank([]) == []


@pytest.mark.parametrize(
    "month, transactions, limit, result",
    [
        (
            "2018-01",
            [
                {"date": "2018-01-03", "amount": -3.06},
                {"date": "2018-01-03", "amount": -51.0},
                {"date": "2018-01-01", "amount": -316.0},
            ],
            10,
            '{"month": "2018-01", "investamount": 19.9}',
        ),
        (
            "2018-01",
            [
                {"date": "2018-01-03", "amount": -3.06},
                {"date": "2018-01-03", "amount": -51.0},
                {"date": "2018-01-01", "amount": -316.0},
            ],
            50,
            '{"month": "2018-01", "investamount": 129.9}',
        ),
        (
            (
                "2018-01",
                [
                    {"date": "2018-01-03", "amount": -3.06},
                    {"date": "2018-01-03", "amount": -51.0},
                    {"date": "2018-01-01", "amount": -316.0},
                ],
                100,
                '{"month": "2018-01", "investamount": 229.9}',
            )
        ),
    ],
)
def test_investment_bank_10(month, transactions, limit, result):
    """Тестируем копилку, округление до 10, 50, 100"""
    assert investment_bank(month, transactions, limit) == result


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
