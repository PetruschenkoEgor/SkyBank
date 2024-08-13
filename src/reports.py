import datetime
import logging
import os
import pandas as pd
from functools import wraps
from src.utils import get_data_from_excel_df, PATH_TO_FILE_EXCEL


# Самая свежая дата в таблице
TODAY = "31.12.2021"

# Файл, в который будет сохраняться отчет по тратам по категориям
PATH_TO_WRITE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports_file", "spending_by_category.txt")

# Файл, в который сохраняются логи
PATH_TO_FILE_FILE_HANDLER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "reports.log")

logger = logging.getLogger("reports")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(PATH_TO_FILE_FILE_HANDLER, "w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def write_to_path(path=PATH_TO_WRITE):
    """ Декоратор, запись в файл """
    def wrapper(function):
        @wraps(function)
        def inner(*args, **kwargs):
            try:
                logger.info("Вызов функции внутри декоратора")
                result = function(*args, **kwargs)
                logger.info("Запись в файл")
                # Запись в файл
                with open(path, 'w', encoding='utf-8') as file:
                    # file.write(result.to_string(header=False, index=False))
                    # Записывает построчно датафрейм в файл
                    result.to_string(file)
                return result
            except Exception as e:
                logger.error(f"Ошибка: {e}")
                return f"Ошибка: {e}"
        return inner
    return wrapper


@write_to_path()
def spending_by_category(transactions: pd.DataFrame, category: str, date: str = TODAY) -> pd.DataFrame:
    """ Траты по категориям за 3 месяца """
    category = category.title()

    logger.info("Определение конечного значения даты")
    date_ = f"{date} 00:00:00"
    # Конечное значение(до какой даты происходит поиск)
    end = datetime.datetime.strptime(date_, "%d.%m.%Y %H:%M:%S")

    logger.info("Определение начального значения даты")
    # Начальное значение(с какой даты начинается поиск)
    start = end - datetime.timedelta(days=90)

    logger.info("Создание дополнительного столбца с датой в формате datetime")
    # Создаем новый столбец "date", в него записываем дату операции в формате объект datetime
    transactions["date"] = transactions["Дата операции"].map(lambda x: datetime.datetime.strptime(str(x), "%d.%m.%Y %H:%M:%S"))

    logger.info("Выборка нужных строк по фильтру")
    # Делаем выборку нужных нам строк(чтобы дата была в нужном промежутке и была нужная категория)
    spending_category = transactions.loc[(transactions["date"] <= end) & (transactions["date"] >= start) & (transactions["Категория"] == category)]

    return spending_category


if __name__ == '__main__':
    print(spending_by_category(get_data_from_excel_df(PATH_TO_FILE_EXCEL), "топливо"))
