from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from product.models import Product, Subcategory, Order, OrderDetails, Category
from product.forms import AddProductForm, DelProductForm, OrderForm


def index(request):
    add_product_form = AddProductForm()
    context = {
        'products': Product.objects.filter(on_the_main=True),
        'categories': Category.objects.all(),
        'form': add_product_form
    }
    return render(request, 'product/index.html', context)


def subcategory_product(request, id):
    context = {
        'subcategory': get_object_or_404(Subcategory, id=id),
        'next': '/{}'.format(id)
    }
    return render(request, 'product/subcategory-product.html', context)


def product_details(request, id):
    init_data = {'next': request.path,
                 'product_id': id}
    add_product_form = AddProductForm(initial=init_data)
    context = {
        'product': get_object_or_404(Product, id=id),
        'form': add_product_form
    }
    return render(request, 'product/product-details.html', context)


def add_product_to_session(request, add_product_form):
    request.session.modified = True
    if 'products' not in request.session:
        request.session['products'] = {}
    if add_product_form.is_valid():
        quantity = add_product_form.cleaned_data['quantity']
        p_id = add_product_form.cleaned_data['product_id']
        request.session['products'].update({p_id: quantity})
    messages.info(request, 'Added to cart!')


def get_orders(session, **kwargs):
    ses_products = session['products']
    orders = []
    for s_product_id in ses_products:
        product = Product.objects.get(pk=s_product_id)
        if kwargs:
            order = Order(order_details=kwargs.get('order_details'), product_id=product.id, title=product.title,
                          description=product.description, price=product.price, quantity=ses_products[s_product_id])
        else:
            order = Order(product_id=product.id, title=product.title, description=product.description,
                          price=product.price, quantity=ses_products[s_product_id])
        orders.append(order)
    return orders


def checkout(request):
    checkout_form = OrderForm(request.POST)
    if checkout_form.is_valid():
        order_details = OrderDetails(full_name=checkout_form.cleaned_data['full_name'],
                                     email=checkout_form.cleaned_data['email'],
                                     city=checkout_form.cleaned_data['city'],
                                     phone=checkout_form.cleaned_data['phone'])
        unique_od = OrderDetails.objects.filter(email=order_details.email)
        if not unique_od:  # if this email not exists save all record
            order_details.save()
        else:  # else update record
            unique_od.update(full_name=order_details.full_name,
                             city=order_details.city,
                             phone=order_details.phone)

        order_details = OrderDetails.objects.get(email=order_details.email)

        # Get orders to save them and link order_details
        orders = get_orders(request.session, order_details=order_details)
        for order in orders:
            order.save()
        request.session['products'] = {}
        messages.info(request, 'Order saved!')


def cart(request):
    if request.method == 'POST':
        if request.POST.get('city'):  # if received request from checkout form
            checkout(request)
            return HttpResponseRedirect('/cart')
        else:
            add_product_form = AddProductForm(request.POST)
            if add_product_form.is_valid():
                next_page = add_product_form.cleaned_data['next']
                add_product_to_session(request, add_product_form)
                return HttpResponseRedirect(next_page)
            else:
                messages.info(request, 'Cart is empty!')
                return HttpResponseRedirect('/cart')
    else:
        if request.session.get('products'):
            orders = get_orders(request.session)
            order_details_form = OrderForm()
            context = {'orders': orders, 'total': sum(orders), 'orderForm': order_details_form}
            return render(request, 'product/cart.html', context)
        else:
            return render(request, 'product/cart.html')


def delete_from_cart(request):
    if request.method == 'POST':
        del_product_form = DelProductForm(request.POST)
        if del_product_form.is_valid():
            p_id = del_product_form.cleaned_data['product_id']
            products = request.session.get('products')
            if products:
                products.pop(p_id)
                request.session['products'] = products
    return HttpResponseRedirect('/cart')


def add_to_cart(request):
    nxt = '/'
    if request.method == 'POST':
        add_product_form = AddProductForm(request.POST)
        nxt = add_product_form['next'].data
        add_product_to_session(request, add_product_form)
    return HttpResponseRedirect(nxt)
