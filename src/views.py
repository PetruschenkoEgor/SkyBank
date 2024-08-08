import datetime


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