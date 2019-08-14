import datetime
import time


class General:
    count = 0

    def __init__(self, user_id, fn, ln, phone, reg):
        self.user_id = user_id
        self.fn = fn
        self.ln = ln
        self.phone = phone
        self.reg = reg
        print('Member {} {} was created'.format(fn, ln))
        General.count += 1

    @staticmethod
    def how_many():
        print('Під час сесії було створено - {} контактів.'.format(General.count))


while True:
    i = input('Enter command here -> ')
    if i == 'stop':
        print('Shutdown(wait 3sec).....')
        time.sleep(3)
        break

    elif i == 'add':
        f = open('db.txt', 'a+')
        check = f.readline()
        members = int(check[9])
        user_id = members + 1
        members += 1

        fn = input('Enter your first name > ')
        ln = input('Enter you last name > ')
        phone = input('Enter your phone > ')
        reg = datetime.datetime.now()
        new_member = General(user_id, fn, ln, phone, reg)
        data = {"user_id": user_id, "first_name": fn, "last_name": ln, "phone": phone, "reg": reg}
        for key, val in data.items():
            f.write('{}:{}\n'.format(key, val))
        last = f.readlines()[-1]
        f.close()

    elif i == 'how_many':
        General.how_many()
