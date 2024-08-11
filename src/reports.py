import pandas as pd
import datetime
import logging
import os
from src.utils import get_data_from_excel_df, PATH_TO_FILE_EXCEL


# Самая свежая дата в таблице
today = "31.12.2021 16:44:00"

# Файл, в который сохраняются логи
PATH_TO_FILE_FILE_HANDLER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "reports.log")

logger = logging.getLogger("reports")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(PATH_TO_FILE_FILE_HANDLER, "w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def spending_by_category(transactions, category, date=today):
    logger.info("Определение конечного значения даты")
    # Конечное значение(до какой даты происходит поиск)
    end = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    logger.info("Определение начального значения даты")
    # Начальное значение(с какой даты начинается поиск)
    start = end - datetime.timedelta(days=90)

    logger.info("Создание дополнительного столбца с датой в формате datetime")
    # Создаем новый столбец "date", в него записываем дату операции в формате объект datetime
    transactions["date"] = transactions["Дата операции"].map(lambda x: datetime.datetime.strptime(str(x), "%d.%m.%Y %H:%M:%S"))
    logger.info("Выборка нужных строк по фильтру")
    # Делаем выборку нужных нам строк(чтобы дата была в нужном промежутке и была нужная категория)
    spending_category = transactions.loc[(transactions["date"] <= end) & (transactions["date"] >= start) & (transactions["Категория"] == category)]
    logger.info("Суммирование полученных значений")
    # Суммируем полученные значения
    sum_spending_category = abs(spending_category["Сумма платежа"]).sum(axis=0)

    return sum_spending_category


if __name__ == '__main__':
    print(spending_by_category(get_data_from_excel_df(PATH_TO_FILE_EXCEL), "Топливо", "31.12.2021 16:44:00"))
