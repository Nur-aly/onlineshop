from django.db import models



# модель заказа для сохранения данныъ заказа
from products.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=50, null=True, verbose_name='* Имя')
    last_name = models.CharField(max_length=50, null=True, verbose_name='* Фамилия')
    email = models.EmailField(verbose_name='E-mail')
    address = models.CharField(max_length=250, null=True, verbose_name='* Адрес проживания')
    postal_code = models.CharField(max_length=20, verbose_name='Почтовой индекс')

    #phone = models.IntegerField(max_length=22, null=True, verbose_name='* Телефон',)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


    def __str__(self):
        return 'Order №{}'.format(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='item', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_item', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

