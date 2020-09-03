from decimal import Decimal
from django.conf import settings
from store.products.models import Product


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSIONS_ID)
        if not cart:  # если сессия пустая и человек на нашем сайте впервые , то создается новая сессия cart

            cart = self.session[settings.CART_SESSIONS_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        '''
        Добавление товара в корзину или обновлние его количества.
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
        '''удаление товара из корзины'''
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def __iter__(self):
        ''' Проходим по товарам корзины и получаем соответствующие обьекты Product.'''
        product_ids = self.keys()
        # Получаем обьекты модели Product и передаем их в корзину.
        products = Product.objects.filiter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
        yield item

    def __len__(self):
        ''' Возврващает общее количество товаров в корзине.'''
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        '''  Возвращает общее количкство товаров в корзине '''
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values())
    
    def clear(self):
        # Отчистка корзины
        del self.session[settings.CART_SESSIONS_ID]
        self.save()
        
