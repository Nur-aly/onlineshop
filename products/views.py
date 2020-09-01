from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Category, Product


def product_list(request, category_slug=None):  # category_slug is needed to create categories URL
	# if categories don't exist, it has to be None
	category = None
	categories = Category.objects.all()
	products = Product.objects.filter(status=True)

	if category_slug:   # if slug is not empty and user chooses any of categories
		category = get_object_or_404(Category, slug=category_slug)  # we take category by slug
		products = category.products.filter(category=category)  # we take all products from initial category
	context = {
			'category': category,
			'categories': categories,
			'products': products,
		}

	return render(request, 'products.html', context)


def product_detail(request, id, slug):
	product = get_object_or_404(Product, slug=slug, id=id, status=True)
	return render(request, 'product_detail.html', context={'product': product})
