import datetime
from get_data import get_data_from_excel, PATH_TO_FILE_EXCEL


# Текущее время
current_time = str(datetime.datetime.now())[11:16]

def say_hello(time_of_day):
    """ Функция принимает строку со временем и здоровается в зависимости от времени суток """
    # Получаем часы и переводим их в число
    time = int(time_of_day[:2])

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
    print(say_hello(current_time))

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


def get_total_amount_expenses(transactions):
    """ Общая сумма расходов """
    numbers_card =[]
    for tr in transactions:
        if tr.get("Номер карты"):
            numbers_card.append(tr.get("Номер карты"))
    return set(numbers_card)


if __name__ == '__main__':
    print(get_total_amount_expenses(get_data_from_excel(PATH_TO_FILE_EXCEL)))

def show_cashback(transactions):
    """ Функция считает кэшбэк(1 рубль за каждые 100 рублей) """
    pass
