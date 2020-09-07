from decimal import Decimal
from django.conf import settings
from products.models import *


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart: # эсли секция пустая и человек первые тут на сайте , то создаётся новая сессия cart
            cart = self.session[settings.CART_SESSION_ID]={}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        '''
        Добавление товара в корзину или обновление его количество.
        '''
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        '''Удаление товара из карзины'''

        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def __iter__(self):
        ''' Проходим по товарам карзины и получаем соответствующие объекты product'''

        product_ids = self.cart.keys()
        # получаем объекты модели Product и передаем их в карзину.
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price']*item['quantity']
        yield item

    def __len__(self):
        ''' Возвращает общая количество  товаров в корзине'''
        return sum(
                item['quantity']
                for item in self.cart.values()
        )

    def get_total_price(self):
        ''' Возвращает общую сумму товаров в корзине'''

        return sum(
                Decimal(item['price'])*item['quantity']
                for item in self.cart.values()
        )

    def clear(self):
        # очистка корзины
        del self.session[settings.CART_SESSION_ID]
        self.save()

