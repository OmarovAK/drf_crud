import requests
from bs4 import BeautifulSoup
import random


def add_product_model():
    url = 'https://fitaudit.ru/categories/fvs'

    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')

    all_product = soup.findAll('span', class_='fimlist_text_wrap')

    list_product_from_site = [product.text.strip().replace('\t\t\t', " ") for product in all_product]

    for prod_ in list_product_from_site:
        url_ = 'http://127.0.0.1:8000/add_product/'
        data = {
            'title': prod_,
            'description': f'Продукт {prod_.lower()}'
        }
        result = requests.post(url=url_, data=data)
        print(result.json())


def delete_product_model():
    url_list_product = 'http://127.0.0.1:8000/list_product/'
    result_list = requests.get(url=url_list_product)
    list_id = [i.get('id') for i in result_list.json()]
    if len(list_id) > 0:
        for id_in_product_model in list_id:
            url_delete_product_model = 'http://127.0.0.1:8000/delete_product/{0}'.format(id_in_product_model)
            result_delete = requests.delete(url=url_delete_product_model)
            if result_delete.status_code == 204:
                print(f'Продукт с id {id_in_product_model} успешно удален')
    else:
        print('Продуктов нет. Сначало добавьте продукты')


def add_stock():
    list_stocks = ['север', 'юг', 'запад', 'восток', 'центр']

    for stock in list_stocks:
        data = {
            'address': stock.title()
        }
        url = 'http://127.0.0.1:8000/add_stock/'
        res = requests.post(url=url, data=data)
        print(res.json())


def fill_warehouses():
    url_stock = 'http://127.0.0.1:8000/list_stock/'

    url_products = 'http://127.0.0.1:8000/list_product/'

    res = requests.get(url=url_stock)

    dict_stocks = {i['id']: i['address'] for i in res.json()}

    res = requests.get(url=url_products)

    dict_product = {i['title']: i['id'] for i in res.json()}

    if len(dict_stocks) > 0 and len(dict_product) > 0:
        for key, value in dict_stocks.items():
            local_dict = dict_product.copy()
            local_list_id = [i for i in local_dict.values()]

            while True:
                try:
                    count_prod = int(input(f'Какое количество продуктов добавить на склад {value}: '))
                    if count_prod <= len(local_list_id):
                        for _ in range(count_prod):
                            product_id = local_list_id.pop(local_list_id.index(random.choice(local_list_id)))
                            product_name = str()
                            quantity = random.randint(1, 25)
                            price = random.randint(25, 600)
                            for name, id_ in local_dict.items():
                                if product_id == id_:
                                    product_name = name

                            data = {
                                'product': product_id,
                                'stock': key,
                                'quantity': quantity,
                                'price': price,
                            }
                            url_add_product_stocks = 'http://127.0.0.1:8000/add_stock_product/'
                            res = requests.post(url=url_add_product_stocks, data=data)
                            if res.status_code == 201:
                                print(
                                    f'На склад {value} успешно добавлены {product_name} в количествe {quantity}  шт. на сумму {quantity * price} тенге')
                            elif res.status_code == 500:
                                print(f'Продукт {product_name} ранее был добавлен на данный склад ({value})')
                        break
                    else:
                        print(
                            f'Количество добавленных продуктов должно быть не равно 0 и не более {len(local_list_id)}')

                except ValueError:
                    print('Ожидается число')
    else:
        if len(dict_product) == 0:
            print('Не заполнен список продуктов. Заполните таблицу продуктов')
        elif len(dict_stocks) == 0:
            print('Не заполнен список складов. Заполните таблицу складов')


def search_products():
    prod = input('Какой продукт найти? ')

    url = f'http://127.0.0.1:8000/list_product/?search={prod}'

    res = requests.get(url=url)
    count = False
    for i in res.json():
        if len(i['stocks']) > 0:
            count = True
            for id_stock in i['stocks']:
                url_ = f'http://127.0.0.1:8000/list_stock/{id_stock}'
                res_ = requests.get(url=url_)
                print(f"{i['title'].upper()} есть на складе {res_.json()['address']}")
    if not count:
        print(f'{prod} - такого продукта нет на складах')


def main():
    dict_command = {
        'add': 'Заполнение таблиц',
        'delete': 'Удаление продуктов',
        'search': 'Поиск продуктов',
        'quit': 'Выход из программы',
    }

    for key, value in dict_command.items():
        print(f'Команда {key} Действие {value}')

    while True:
        command = input('Введите команду ')
        if command in dict_command.keys():
            if command == 'add':
                add_product_model()
                add_stock()
                fill_warehouses()
            elif command == 'delete':
                delete_product_model()
            elif command == 'search':
                search_products()
            else:
                break
        else:
            print('Такой команды нет')

main()