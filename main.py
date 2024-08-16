import json
import re

from src.reports import spending_by_category
from src.services import investment_bank, transactions_for_investment_bank
from src.utils import PATH_TO_FILE_EXCEL, get_data_from_excel, get_data_from_excel_df, say_hello
from src.views import get_data_for_web_page


def main():
    """Главная функция"""
    # Главная функция раздела Главная страница
    views_main = json.loads(get_data_for_web_page())

    print(say_hello())

    # Информация по карте(номер карты, траты, кэшбэк)
    info_card = input("Хотите получить информацию по вашим картам за последний месяц? Да/Нет: ").lower()
    while True:
        if info_card == "да":
            print("Информация по вашим картам:")
            for card in views_main.get("cards"):
                print(f"Карта: {card.get("last_digits")}")
                print(f"Расходы: {card.get("total_spent")}")
                print(f"Кэшбэк: {card.get("cashback")}")
            break
        elif info_card == "нет":
            break
        else:
            print("Введите Да или Нет!")
            info_card = input("Хотите получить информацию по вашим картам? Да/Нет: ").lower()

    # Топ-5 трат
    top_5 = input("Хотите получить ТОП-5 трат по вашим картам? Да/Нет: ").lower()
    while True:
        if top_5 == "да":
            print("ТОП-5 трат по вашим картам:")
            for top in views_main.get("top_transactions"):
                print(
                    f"Дата: {top.get("date")}\n"
                    f"Сумма: {top.get("amount")}\n"
                    f"Категория: {top.get("category")}\n"
                    f"Информация: {top.get("description")}"
                )
            break
        elif top_5 == "нет":
            break
        else:
            print("Введите Да или Нет!")
            top_5 = input("Хотите получить ТОП-5 трат по вашим картам? Да/Нет: ").lower()

    # Курсы валют
    currency_rates = input("Хотите получить информацию о курсах валют? Да/Нет: ").lower()
    while True:
        if currency_rates == "да":
            print("Информация по курсам валют USD и EUR:")
            for currency in views_main.get("currency_rates"):
                print(f"Валюта: {currency.get("currency")}\n" f"Курс: {currency.get("rate")}")
            break
        elif currency_rates == "нет":
            break
        else:
            print("Введите Да или Нет!")
            currency_rates = input("Хотите получить информацию о курсах валют? Да/Нет: ").lower()

    # Цены акций S&P 500
    s_p = input(
        "Хотите получить информацию о ценах на акции крупнейших американских компаний S&P 500? Да/Нет: "
    ).lower()
    while True:
        if s_p == "да":
            print("Информация о ценах на акции крупнейших американских компаний S&P 500:")
            for sp in views_main.get("stock_prices"):
                print(f"Тикер: {sp.get("stock")}\n" f"Цена: {sp.get("rate")}")
            break
        elif s_p == "нет":
            break
        else:
            print("Введите Да или Нет!")
            s_p = input(
                "Хотите получить информацию о ценах на акции крупнейших американских компаний S&P 500? Да/Нет: "
            ).lower()

    # Инвесткопилка
    investing = input(
        "Хотите узнать сколько вы бы отложили в инвест копилку по своим картам за месяц? Да/Нет: "
    ).lower()
    while True:
        if investing == "да":
            # month = input("Введите год и месяц в формате 'ГГГГ-ММ': ")
            while True:
                month = input("Введите год и месяц в формате 'ГГГГ-ММ': ")
                pattern = r"\d\d\d\d\-\d\d"
                if re.search(pattern, month):
                    while True:
                        limit = input("Укажите до какой суммы округлять(10, 50 или 100 руб): ")
                        if limit == "10" or limit == "50" or limit == "100":
                            invest_bank = json.loads(
                                investment_bank(
                                    month,
                                    transactions_for_investment_bank(get_data_from_excel(PATH_TO_FILE_EXCEL)),
                                    int(limit),
                                )
                            )
                            print(
                                f"За {month[-2:]} месяц {month[:4]} года вы могли бы отложить \n"
                                f"{invest_bank.get("investamount")} рублей"
                            )
                            break
                        else:
                            print("Выберите из значений 10, 50 или 100.")
                    break
                else:
                    print("Неверный формат даты")
                    # month = input("Введите год и месяц в формате 'ГГГГ-ММ': ")
            break
        elif investing == "нет":
            break
        else:
            print("Введите Да или Нет!")
            investing = input(
                "Хотите узнать сколько вы бы отложили в инвест копилку по своим картам за месяц? Да/Нет: "
            ).lower()

    # Отчеты
    while True:
        reports = input("Хотите получить отчет по тратам в заданной категории за три месяца? Да/Нет: ").lower()
        if reports == "да":
            while True:
                category = input("Введите категорию трат: ").lower()
                if category.isalpha():
                    while True:
                        date = input("Введите дату в формате ДД.ММ.ГГГГ: ")
                        pattern = r"\d\d\.\d\d\.\d\d\d\d"
                        if re.search(pattern, date):
                            spending = spending_by_category(get_data_from_excel_df(PATH_TO_FILE_EXCEL), category, date)
                            print("Ваш отчет сформирован. Его так же можно скачать по ссылке [ссылка]")
                            print(spending)
                            break
                        else:
                            print("Неправильный формат даты!")
                    break
                else:
                    print("Неправильный формат категории!")
            break
        elif reports == "нет":
            break
        else:
            print("Введите Да или Нет!")


if __name__ == "__main__":
    print(main())
