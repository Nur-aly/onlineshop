from django.shortcuts import render

# Create your views here.
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem
from products.models import Product


def order_create(request):
    cart = Cart(request)
    latest_products = Product.objects.order_by('name')[:3]

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                )
            cart.clear()
            return render(request, 'created.html', {'order': order})
    else:
        form = OrderCreateForm()

    context = {
        'cart': cart,
        'form': form,
        'latest_products': latest_products,

    }
    return render(request, 'create.html', context)
