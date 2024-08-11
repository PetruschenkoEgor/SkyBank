import pandas as pd
import datetime
from src.utils import get_data_from_excel_df, PATH_TO_FILE_EXCEL


def spending_by_category(transactions, category):
    """ Возвращает траты по заданной категории за последние три месяца """
    # Уберем транзакции, в которых не указана категория
    # df_not_nan = transactions.loc[transactions["Категория"].notnull()]

    # Получаем текущую дату
    date = datetime.datetime.now()
    # Получаем дату 3 месяца назад
    start_date = date - datetime.timedelta(days=90)
    date_ = date.strftime("%m")

    # if date == "today":
    #     date = datetime.datetime.now()

    # Получаем месяц из датафрейма столбца "Дата операции"
    # month = str(transactions["Дата операции"].str.extract(r'\d\d\.(\d\d)\.'))

    # Делаем выборку нужных нам занчений по дате и категории
    # spending_category = transactions.loc[(transactions["Категория"] == category) & (transactions["Дата операции"].str.extract(r'\d\d\.(\d\d)\.') == "12")]

    return start_date
    # Отсортировать по дате и сделать выборку до определенного числа


# if __name__ == '__main__':
#     print(spending_by_category(get_data_from_excel_df(PATH_TO_FILE_EXCEL), "Топливо"))

# Дата сегодня
today = datetime.datetime.now()

def spending_by_category_(transactions, category, date):
    today = datetime.datetime.now()
    end = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    start = end - datetime.timedelta(days=90)
    # spending_category = transactions.loc[transactions["Дата операции"][:10] == "01.01.2018"]
    # spending_category = transactions[transactions["Дата операции"]]
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'])  # If your Date column is of the type object otherwise skip this
    date_range = str(transactions['Дата операции'].dt.date.min(start)) + ' to ' + str(transactions['Дата операции'].dt.date.max(end))
    return date_range


if __name__ == '__main__':
    print(spending_by_category_(get_data_from_excel_df(PATH_TO_FILE_EXCEL), "Топливо", "01.01.2018 12:49:53"))
