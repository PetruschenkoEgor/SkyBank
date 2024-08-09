from src.get_data import get_data_from_excel, PATH_TO_FILE_EXCEL


def transactions_for_investment_bank(transactions: list[dict]) -> list[dict]:
    """ Функция преобразует список транзакций для инвест-копилки """
    # Создаем пустой список, куда будем накидывать словари с нужными данными
    result_list = []

    # Проходимся по транзакциям и добавляем нужные нам данные в словарь, словари добавляем в список
    for trans in transactions:
        # Проверяем, что бы транзакция была действительно успешной тратой
        if trans.get("Статус") == "OK" and trans.get("Категория") not in ["Переводы", "Пополнения", "Другое", "Бонусы", "Наличные"] and float(trans.get("Сумма платежа")) < 0:
            dict_trans = dict()
            date = trans.get("Дата операции")
            dict_trans["date"] = f"{date[6:10]}-{date[3:5]}-{date[:2]}"
            dict_trans["amount"] = float(trans.get("Сумма платежа"))
            result_list.append(dict_trans)
    return result_list


# if __name__ == '__main__':
#     print(transactions_for_investment_bank(get_data_from_excel(PATH_TO_FILE_EXCEL)))


def investment_bank(month, transactions, limit):
    """ Копилка, возвращает сумму, которую округлили до 10, 50 или 100 рублей и откладывают в инвесткопилку """
    # Возможная отложенная сумма
    deferred_amount = []
    for trans in transactions:
        digit_ = str(round(trans.get("amount"), 1))
        # Выбираем транзакции с нужным месяцем
        if month == trans.get("date")[:7]:
            # Выбираем до скольки округлить сумму согласно лимиту
            if limit == 10 and trans.get("amount") != 0.0:
                digit = float(digit_[-3:])
                # Сумма, которую можно отложить в инвест-копилку
                rounding = 10 - abs(digit)
                deferred_amount.append(rounding)
            elif limit == 50 and trans.get("amount") != 0.0:
                digit = float(digit_[-4:])
                if digit >= 50:
                    rounding = 100 - abs(digit)
                    deferred_amount.append(rounding)
                else:
                    rounding = 50 - abs(digit)
                    deferred_amount.append(rounding)
            elif limit == 100 and trans.get("amount") != 0.0:
                digit = float(digit_[-4:])
                rounding = 100 - abs(digit)
                deferred_amount.append(rounding)

    return sum(deferred_amount)

if __name__ == '__main__':
    print(investment_bank("2018-01", [{'date': '2018-01-01', 'amount': 0.0}], 100))
# if __name__ == '__main__':
#     print(investment_bank("2018-01", transactions_for_investment_bank(get_data_from_excel(PATH_TO_FILE_EXCEL)), 100))
