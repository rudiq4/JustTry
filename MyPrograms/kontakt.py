import datetime
import locale

'''
AIM:
Створити книгу контактів з такии можливостями:
1.Добавляти новий контакт (First name, last name, phone number, date of registration)
2.Видаляти контакт
3.Переглядати інформацію про контакт
4.Виводити кількість контактів
5.Зберігати актуальну базу данних у файл
'''
__version__ = '0.0.1'

locale.setlocale(locale.LC_ALL, "ru_RU")  # Localization

info = '1. add - добавити контакт\n' \
       '2. delete - видалити контакт'

members = []


class General:
    count = 0

    def __init__(self, member_id, first_name, last_name, phone, reg):
        self.member_id = member_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.reg = reg
        ###
        General.count += 1

    # def __del__(self):
    #     General.count -= 1
    #     print('{}{} був видалена(ий) з ваших контактів'.format(first_name, last_name))

    def get_info(self):
        pass

    @staticmethod
    def how_many():
        print('Під час сесії було створено - {} контактів.'.format(General.count))


while True:
    f = open('members.txt', 'a+')
    ans = input('Введіть команду.(Список команд - info) -> ')
    if ans == 'break':
        print('Програма закривається')
        f.close()
        break
    elif ans == 'info':
        print(info)
    elif ans == 'how_many':
        print(General.how_many())
    elif ans == 'add':
        first_line = f.readline()
        if not first_line:  # если первая строка None
            member_id = 0
        else:
            digit = int(first_line[0])
            member_id = digit + 1
        first_name = input("Ім'я - ")
        last_name = input('Прізвище - ')
        phone = input('Номер телефону - ')
        registration = datetime.datetime.now()
        print('Новий контакт - {}{} створено'.format(first_name, last_name))
        line = str(member_id) + first_name + last_name + phone + str(registration)
        f.write(line + '\n')
        new_contact = General(member_id, first_name, last_name, phone, registration)
