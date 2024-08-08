import datetime
from get_data import get_data_from_excel, PATH_TO_FILE_EXCEL


def say_hello():
    """ Функция принимает строку со временем и здоровается в зависимости от времени суток """
    # Текущее время
    current_time = str(datetime.datetime.now())[11:16]

    # Получаем часы и переводим их в число
    time = int(current_time[:2])

    # В зависимости от времени здороваемся
    if 6 <= time <= 11:
        hello = "Доброе утро"
    elif 12 <= time <= 17:
        hello = "Добрый день"
    elif 18 <= time <= 22:
        hello = "Добрый вечер"
    else:
        hello = "Доброй ночи"

    return hello


if __name__ == '__main__':
    print(say_hello())

def mask_card_number(number_card):
    """ Маскирует номер карты(показывает 4 последние цифры) """
    number_card_str = str(number_card)

    # Проверяем корректность введенного номера карты
    if len(number_card_str) != 16 or not number_card_str.isdigit():
        result = "Некорректный номер карты!"
    else:
        # Делаем маску номера, заменяем часть строки подстрокой
        result = number_card_str[-4:]

    return result


if __name__ == "__main__":
    print(mask_card_number(7000792289606361))


def get_total_amount_expenses(transactions, number_card):
    """ Общая сумма расходов """
    # Список, в который попадают все операции по карте
    sum_list = []
    for tr in transactions:
        # Проверяем - операция относится к данной карте, статус - ок, не входит в указанные категории и со знаком минус
        if str(tr.get("Номер карты"))[-4:] == str(number_card)[-4:] and tr.get("Статус") == "OK" and tr.get("Категория") not in ["Переводы", "Пополнения", "Другое", "Бонусы"] and float(tr.get("Сумма платежа")) < 0:
            sum_list.append(tr.get("Сумма платежа"))
    sum_list = sum(sum_list)
    return -sum_list


# if __name__ == '__main__':
#     print(get_total_amount_expenses(get_data_from_excel(PATH_TO_FILE_EXCEL), "**7197"))

def show_cashback(expenses):
    """ Функция считает кэшбэк(1 рубль за каждые 100 рублей) """
    # Округляем кэшбэк до двух цифр после запятой
    cashback = round(expenses * 0.01, 2)
    return cashback


# if __name__ == '__main__':
#     print(show_cashback(get_total_amount_expenses(get_data_from_excel(PATH_TO_FILE_EXCEL), "**7197")))
