import os
import logging
import pandas as pd


# Путь к файлу EXCEL
PATH_TO_FILE_EXCEL = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.xlsx")

# Файл, в который сохраняются логи
PATH_TO_FILE_FILE_HANDLER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "utils.log")

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(PATH_TO_FILE_FILE_HANDLER, "w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_data_from_excel(path_to_file):
    """ Функция получает путь к файлу и возвращает список словарей """
    try:
        logger.info("Считывание EXCEL-файла")
        # Считываем Excel-файл
        transactions_excel = pd.read_excel(path_to_file)

        logger.info("Преобразование полученных данных в список словарей")
        # Преобразуем полученные данные в список словарей
        transactions_list_dicts = transactions_excel.to_dict(orient="records")

        return transactions_list_dicts
    except FileNotFoundError:
        logger.error(f"Ошибка: файл не найден")
        return []


if __name__ == "__main__":
    print(get_data_from_excel(PATH_TO_FILE_EXCEL))


def get_data_from_excel_df(path_to_file):
    """ Функция получает путь к файлу и возвращает DataFrame """
    try:
        logger.info("Считывание EXCEL-файла")
        # Считываем Excel-файл
        transactions_excel = pd.read_excel(path_to_file)

        return transactions_excel
    except FileNotFoundError:
        logger.error(f"Ошибка: файл не найден")
        return []


# if __name__ == '__main__':
#     print(get_data_from_excel_df(PATH_TO_FILE_EXCEL))
