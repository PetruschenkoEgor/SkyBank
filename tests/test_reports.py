import os

from src.reports import spending_by_category
from src.utils import get_data_from_excel_df

PATH_TO_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "df_1.xlsx")


def test_spending_by_category():
    """Тест траты по категориям"""
    assert (
        spending_by_category(get_data_from_excel_df(PATH_TO_FILE), "топливо", "20.12.2021")
        == '{"Unnamed: 0":0,"Дата операции":"18.12.2021 16:53:16","Дата платежа":"20.12.2021","Номер карты":"*7197",'
           '"Статус":"OK","Сумма операции":-176,"Валюта операции":"RUB","Сумма платежа":-176,"Валюта платежа":"RUB",'
           '"Кэшбэк":null,"Категория":"Топливо","MCC":5541,"Описание":"ЛУКОЙЛ","Бонусы (включая кэшбэк)":3,'
           '"Округление на инвесткопилку":0,"Сумма операции с округлением":176,"date":1639846396000}\n'
    )
