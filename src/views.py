import json

from src.utils import (PATH_TO_FILE_EXCEL, TODAY, USERS_SETTINGS, get_data_from_excel, get_data_from_excel_df,
                       get_total_amount_expenses, mask_card_number, say_hello, show_currency_rates_data,
                       show_stock_prices_data_sp500, show_transactions_top_5)


def get_data_for_web_page(date: str = TODAY) -> str:
    """ " Главная функция раздела веб_страниц"""
    # Создаем пустой словарь для добавления данных для раздела веб-страницы
    data_web_page = dict()

    # Приветствие
    greeting = say_hello()
    data_web_page["greeting"] = greeting

    # Общая сумма расходов по каждой карте
    cards = get_total_amount_expenses(
        get_data_from_excel_df(PATH_TO_FILE_EXCEL),
        mask_card_number(get_data_from_excel_df(PATH_TO_FILE_EXCEL)),
        date=TODAY,
    )
    data_web_page["cards"] = cards

    # Топ-5 транзакций по сумме платежа
    top_transactions = show_transactions_top_5(get_data_from_excel(PATH_TO_FILE_EXCEL))
    data_web_page["top_transactions"] = top_transactions

    # Курсы валют
    currency_rates = show_currency_rates_data()
    data_web_page["currency_rates"] = currency_rates

    # Цены на акции S&P 500
    stock_prices = show_stock_prices_data_sp500(USERS_SETTINGS)
    data_web_page["stock_prices"] = stock_prices

    return json.dumps(data_web_page, ensure_ascii=False)


if __name__ == "__main__":
    print(get_data_for_web_page())
