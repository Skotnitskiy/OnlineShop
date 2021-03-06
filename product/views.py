from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.template.defaultfilters import register

from product.models import Product, Subcategory, Order, OrderDetails, Category, ExchangeRate
from product.forms import AddProductForm, DelProductForm, OrderForm
import smtplib
from email.message import EmailMessage


def index(request):
    add_product_form = AddProductForm()
    context = {
        'products': Product.objects.filter(on_the_main=True),
        'categories': Category.objects.all(),
        'form': add_product_form,
        'uah': ExchangeRate.objects.get(currency_name='UAH').currency
    }
    return render(request, 'product/index.html', context)


def multiply(value, arg):
    return round(value*arg, 2)


register.filter('multiply', multiply)


def subcategory_product(request, id):
    context = {
        'subcategory': get_object_or_404(Subcategory, id=id),
        'next': '/{}'.format(id),
        'uah': ExchangeRate.objects.get(currency_name='UAH').currency
    }
    return render(request, 'product/subcategory-product.html', context)


def increase_product_rating(id):
    product = get_object_or_404(Product, id=id)
    product.rating += 1
    product.save()
    return product


def product_details(request, id):
    init_data = {'next': request.path,
                 'product_id': id}
    add_product_form = AddProductForm(initial=init_data)
    product = increase_product_rating(id)
    context = {
        'product': product,
        'form': add_product_form,
        'uah': ExchangeRate.objects.get(currency_name='UAH').currency * product.price
    }
    return render(request, 'product/product-details.html', context)


def add_product_to_session(request, add_product_form):
    request.session.modified = True
    if 'products' not in request.session:
        request.session['products'] = {}
    if add_product_form.is_valid():
        quantity = add_product_form.cleaned_data['quantity']
        p_id = add_product_form.cleaned_data['product_id']
        if quantity <= 10:
            request.session['products'].update({p_id: quantity})
            messages.info(request, 'Added to cart!')
        else:
            messages.error(request, 'The goods must be no more than 10')


def get_orders(session, **kwargs):
    ses_products = session['products']
    orders = []
    for s_product_id in ses_products:
        product = Product.objects.get(pk=s_product_id)
        if kwargs:
            order = Order(order_details=kwargs.get('order_details'), product_id=product.id, title=product.title,
                          description=product.description, price=product.price, quantity=ses_products[s_product_id],
                          img_url=product.img_url)
        else:
            order = Order(product_id=product.id, title=product.title, description=product.description,
                          price=product.price, quantity=ses_products[s_product_id], img_url=product.img_url)
        orders.append(order)
    return orders


def send_report(rep):
    gmail_user = 'geekpy.test@gmail.com'
    gmail_password = 'qwerty123Ss'

    msg = EmailMessage()
    you = 'one2011@yandex.ua'
    msg['Subject'] = 'Report Sergey Skotnitskiy'
    msg['From'] = gmail_user
    msg['To'] = you
    msg.set_content(rep)
    msg.set_type('text/html')

    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.login(gmail_user, gmail_password)
    s.sendmail(gmail_user, [you], msg.as_string())
    s.close()


def report(orders):
    html = '<table border=1>' \
           '<th>Title</th>' \
           '<th>Price</th>' \
           '<th>Description</th>' \
           '<th>Quantity</th>' \
           '{} </table>'
    rows = ''
    for order in orders:
        rows += '<tr><td>{}<br> <img src="{}"</td>'.format(order.title, order.img_url)
        rows += '<td>{} USD</td>'.format(order.price)
        rows += '<td>{}</td></tr>'.format(order.description)
        rows += '<td>{}</td></tr>'.format(order.quantity)
    return html.format(rows)


def checkout(request):
    checkout_form = OrderForm(request.POST)
    email = ''
    if checkout_form.is_valid():
        email = checkout_form.cleaned_data['email']
        order_details = OrderDetails(full_name=checkout_form.cleaned_data['full_name'],
                                     email= email,
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
        orders = Order.objects.filter(order_details__email=email)
        rep = report(orders)
        send_report(rep)


def cart(request):
    uah = ExchangeRate.objects.get(currency_name='UAH').currency
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
            context = {'orders': orders,
                       'total': sum(orders),
                       'orderForm': order_details_form,
                       'uah': uah
                       }
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


def orders(request):
    if request.method == 'POST':
        mail_form = request.POST
        email = mail_form['email']
        orders = Order.objects.filter(order_details__email=email)
        context = {
            'orders': orders
        }
        return render(request, 'product/orders.html', context)
    else:
        messages.info(request, 'No orders!')
        return render(request, 'product/orders.html')
