from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from product.models import Product, Subcategory, Order


def index(request):
    context = {
        'products': Product.objects.filter(on_the_main=True)
    }
    return render(request, 'product/index.html', context)


def subcategory_product(request, id):
    context = {
        'subcategory': get_object_or_404(Subcategory, id=id)
    }
    return render(request, 'product/subcategory-product.html', context)


def product_details(request, id):
    context = {
        'product': get_object_or_404(Product, id=id)
    }
    return render(request, 'product/product-details.html', context)


def add_product_to_session(request, p_id):
    request.session.modified = True
    if 'products' not in request.session:
        request.session['products'] = {}
    request.session['products'].update({p_id: request.POST['quantity']})
    messages.info(request, 'Added to cart!')


def cart(request):
    if request.method == 'POST':
        next_page = request.POST.get('next', '/')
        p_id = request.POST.get('product_id')
        add_product_to_session(request, p_id)
        return HttpResponseRedirect(next_page)
    else:
        if request.session.get('products'):
            ses_products = request.session['products']
            orders = []
            for s_product_id in ses_products:
                product = Product.objects.get(pk=s_product_id)
                order = Order(product_id=product.id, title=product.title, description=product.description,
                              price=product.price, quantity=ses_products[s_product_id])
                orders.append(order)
            print()

            return render(request, 'product/cart.html', {'orders': orders, 'total': sum(orders)})
        else:
            return render(request, 'product/cart.html')


def delete_from_cart(request):
    if request.method == 'POST':
        p_id = request.POST.get('p_id')
        products = request.session.get('products')
        if products:
            products.pop(p_id)
            request.session['products'] = products
    return HttpResponseRedirect('/cart')


def add_to_cart(request):
    if request.method == 'POST':
        add_product_to_session(request, request.POST['p_id'])
    return HttpResponseRedirect('/cart')
