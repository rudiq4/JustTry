import time
import random

'''Міністерство внутрішніх справ'''
'''cmd/exit/add/check'''

cities = {
    'Волинська': 'АС', 'Львівська': 'ВС', 'Закарпатська': 'АО', 'Рівненська': 'ВК', 'Тернопільська': 'ВО',
    'Івано-Франківська': 'АТ', 'Житомирська': 'АМ', 'Вінницька': 'АВ', 'Чернівецька': 'СЕ', 'Київ': 'АА',
    'Київська': 'АІ', 'Черкаська': 'СА', 'Миколаївська': 'ВЕ', 'Одеська': 'ВН',
    'Чернігівська': 'СВ', 'Полтавська': 'ВІ', 'Кіровоградська': 'ВА', 'Херсонська': 'ВТ', 'Крим': 'АК',
    'Севастополь': 'СН', 'Харківська': 'АХ', 'Дніпропетровська': 'АЕ', 'Запорізька': 'АР', 'Луганська': 'ВВ',
    'Донецька': 'АН'
}

letters_list = ['A', 'B', 'C', 'E', 'H', 'I', 'K', 'M', 'O', 'P', 'T', 'X']

cmd = 'exit/add/check'

print('Database load ....')
time.sleep(1)


def plate_generator(region):
    first_letters = cities.get(region)
    last_letters = ''
    number = ''
    for ix in range(4):
        digit = str(random.randint(1, 9))
        number += digit
    for ix in range(2):
        letter = random.choice(letters_list)
        last_letters += letter
    full_number = first_letters + number + last_letters
    print('Номер {} успішно згенерований'.format(full_number))


while True:
    i = input('Введіть команду')
    if i == "cmd":
        print(cmd)
    elif i == 'exit':
        break
    elif i == 'add':
        x = input('Введіть область')
        if x in cities:
            plate_generator(x)
        else:
            print('Такої області не існує')
    else:
        print('Такої команди не існує! Список команд - cmd')


