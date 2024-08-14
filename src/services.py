import datetime
import json
import logging
import os

from src.utils import PATH_TO_FILE_EXCEL, get_data_from_excel

# Файл, в который сохраняются логи
PATH_TO_FILE_FILE_HANDLER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "services.log")

logger = logging.getLogger("services")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(PATH_TO_FILE_FILE_HANDLER, "w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def transactions_for_investment_bank(transactions: list[dict]) -> list[dict]:
    """Функция преобразует список транзакций для инвест-копилки"""
    # Создаем пустой список, куда будем накидывать словари с нужными данными
    result_list = []

    # Проходимся по транзакциям и добавляем нужные нам данные в словарь, словари добавляем в список
    for trans in transactions:
        logger.info("Проверка транзакции(успешный статус, нужные категории и операция со знаком минус)")
        # Проверяем, что бы транзакция была действительно успешной тратой
        if (
            trans.get("Статус") == "OK"
            and trans.get("Категория") not in ["Переводы", "Пополнения", "Другое", "Бонусы", "Наличные"]
            and float(trans.get("Сумма платежа")) < 0
        ):
            dict_trans = dict()

            # Добавляем дату в словарь
            date = datetime.datetime.strptime(trans.get("Дата операции"), "%d.%m.%Y %H:%M:%S")
            date_ = date.strftime("%Y-%m-%d")
            dict_trans["date"] = date_

            # Добавляем сумму платежа в словарь
            dict_trans["amount"] = float(trans.get("Сумма платежа"))

            # Добавляем словари в список
            result_list.append(dict_trans)

    return result_list


if __name__ == '__main__':
    print(transactions_for_investment_bank(get_data_from_excel(PATH_TO_FILE_EXCEL)))


def investment_bank(month: str, transactions: list[dict[str, any]], limit: int) -> str:
    """Копилка, возвращает сумму, которую округлили до 10, 50 или 100 рублей и откладывают в инвесткопилку"""
    # Возможная отложенная сумма
    deferred_amount = []

    for trans in transactions:
        logger.info("Получение траты и ее округление")
        digit_ = str(round(trans.get("amount"), 1))

        logger.info("Выборка транзакции с нужным месяцем")
        # Выбираем транзакции с нужным месяцем
        if month == trans.get("date")[:7]:

            # Выбираем до скольки округлить сумму согласно лимиту
            if limit == 10 and trans.get("amount") != 0.0:
                digit = float(digit_[-3:])
                logger.info("Получение суммы для копилки(округление до 10)")
                # Сумма, которую можно отложить в инвест-копилку
                rounding = 10 - abs(digit)
                deferred_amount.append(rounding)

            elif limit == 50 and trans.get("amount") != 0.0:
                digit = float(digit_[-4:])

                if digit >= 50:
                    logger.info("Получение суммы для копилки(округление до 50)")
                    rounding = 100 - abs(digit)
                    deferred_amount.append(rounding)

                else:
                    logger.info("Получение суммы для копилки(округление до 50)")
                    rounding = 50 - abs(digit)
                    deferred_amount.append(rounding)

            elif limit == 100 and trans.get("amount") != 0.0:
                digit = float(digit_[-4:])
                logger.info("Получение суммы для копилки(округление до 100)")
                rounding = 100 - abs(digit)
                deferred_amount.append(rounding)

    logger.info("Добавление в словарь данных")
    # Добавляем в словарь нужные данные
    deferred_amount_result = dict()
    deferred_amount_result["month"] = month
    deferred_amount_result["investamount"] = sum(deferred_amount)

    return json.dumps(deferred_amount_result, ensure_ascii=False)


if __name__ == "__main__":
    print(investment_bank("2018-01", [
        {"date": "2018-01-03", "amount": -3.06},
        {"date": "2018-01-03", "amount": -51.0},
        {"date": "2018-01-01", "amount": -316.0},
    ], 100))
