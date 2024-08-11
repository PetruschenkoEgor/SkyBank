import pandas as pd
import datetime
from src.utils import get_data_from_excel_df, PATH_TO_FILE_EXCEL


# Самая свежая дата в таблице
today = "31.12.2021 16:44:00"


def spending_by_category(transactions, category, date=today):
    # Конечное значение(до какой даты происходит поиск)
    end = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    # Начальное значение(с какой даты начинается поиск)
    start = end - datetime.timedelta(days=90)

    # Создаем новый столбец "date", в него записываем дату операции в формате объект datetime
    transactions["date"] = transactions["Дата операции"].map(lambda x: datetime.datetime.strptime(str(x), "%d.%m.%Y %H:%M:%S"))
    # Делаем выборку нужных нам строк(чтобы дата была в нужном промежутке и была нужная категория)
    spending_category = transactions.loc[(transactions["date"] <= end) & (transactions["date"] >= start) & (transactions["Категория"] == category)]
    # Суммируем полученные значения
    sum_spending_category = abs(spending_category["Сумма платежа"]).sum(axis=0)

    return sum_spending_category


if __name__ == '__main__':
    print(spending_by_category(get_data_from_excel_df(PATH_TO_FILE_EXCEL), "Топливо", "31.12.2021 16:44:00"))
