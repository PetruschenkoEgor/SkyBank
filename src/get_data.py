import os
import pandas as pd


# Путь к файлу EXCEL
PATH_TO_FILE_EXCEL = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.xlsx")


def get_data_from_excel(path_to_file):
    """ Функция получает путь к файлу и возвращает список словарей """
    try:
        # Считываем Excel-файл
        transactions_excel = pd.read_excel(path_to_file)

        # Убираем значения NaN
        # transactions_excel_not_nan_number_card = transactions_excel.loc[transactions_excel["Номер карты"].notnull()]

        # Преобразуем числа с плавающей точкой в int64
        # transactions_excel_not_nan = transactions_excel.astype({"Кэшбэк": "int64", "MCC": "int64"})

        # Преобразуем полученные данные в список словарей
        transactions_list_dicts = transactions_excel.to_dict(orient="records")

        return transactions_list_dicts
    except FileNotFoundError:
        return []


if __name__ == "__main__":
    print(get_data_from_excel(PATH_TO_FILE_EXCEL))
