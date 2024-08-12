import datetime
import requests
import os
from src.utils import get_data_from_excel, get_data_from_excel_df, PATH_TO_FILE_EXCEL, say_hello, mask_card_number


def get_data_for_web_page():
    """" Главная функция раздела веб_страниц """
    # Создаем пустой словарь для добавления данных для раздела веб-страницы
    data_web_page = dict()

    # Записываем приветствие
    greeting = say_hello()
    data_web_page["greeting"] = greeting

    # Уникальные номера карт
    numbers_card = mask_card_number(get_data_from_excel_df(PATH_TO_FILE_EXCEL))
    for number in numbers_card:


    data_web_page["cards"] =

    return data_web_page


if __name__ == '__main__':
    print(get_data_for_web_page())
