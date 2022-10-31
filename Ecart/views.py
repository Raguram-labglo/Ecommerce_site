from django.shortcuts import render, redirect
from django.db.models import Q
from Ecart.forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Sum

def Form_in(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)
        if user is not None:
            login(request,user)
            return redirect('show')
        else:
            form = AuthenticationForm()
            messages.info(request, 'username or password is incorrect')
            return render(request,'log_in.html',{'form':form})
    else:
        form = AuthenticationForm()
        return render(request, 'log_in.html', {'form':form})

def Form_out(request):

    logout(request)
    return redirect('login')

@login_required(login_url= '/ecommerce/')
def Product_list(request):

    all_product = Product.objects.all()
    wish, list = Wish.objects.get_or_create(user = request.user)
    wish_product = wish.favourite.all()
    alredy_wish = wish_product
    wish_product_list = []
    for product in alredy_wish:
        wish_product_list.append(product)
    print(wish_product_list)
    return render(request, 'show.html', {'products':all_product, 'alredy':wish_product_list})

@login_required(login_url= '/ecommerce/')
def Search(request):

    context = {}
    if 'need' in request.POST: 
        find = request.POST.get('need')
        all = Product.objects.all()
        context['product list'] = all
        suggetions_qs = Product.objects.filter(Q(title__icontains = find) | Q(name__icontains = find) | Q(brand__icontains = find) & Q(in_stock__gt = 0))
        context['data'] = suggetions_qs
    return render(request, 'search.html', context)

@login_required(login_url= '/ecommerce/')
def add_to_cart(request, id):
    if request.method == "POST":
        context = {}
        product_selected = Product.objects.get(id = id)
        price_of_product = product_selected.price
        add_cart = Cart.objects.create(user = request.user, product=product_selected , price = price_of_product)
        context['data'] = add_cart.product
        context['pricedata'] = add_cart
    return redirect(Product_list)

@login_required(login_url= '/ecommerce/')
def Show_cart(request):

    cart_list = Cart.objects.filter(Q(user = request.user) & Q(is_active = True))
    total_price = cart_list.aggregate(Sum('price'))
    cart_total_price = total_price['price__sum']
    context = {'data':cart_list, 'total_price': cart_total_price}
    return render(request, 'cart.html', context)

def Update_cart(request,id):
    quantity = request.POST.get('quantity')
    update_cart = Cart.objects.get(id = id)
    update_cart.quantity = quantity
    update_cart.price = int(update_cart.product.price) * int(update_cart.quantity)
    update_cart.save()
    return render(request, 'cart.html')
@login_required(login_url= '/ecommerce/')
def Remove_cart(request, id):

    cart_del = Cart.objects.get(id=id)
    cart_del.delete()
    return redirect(Show_cart)

@login_required(login_url= '/ecommerce/')
def Order_details(request):
    
    get_order = Order.objects.filter(user = request.user.id)
    if get_order == None :
        context = {'message': 'your order page is empty'}
        return render(request, 'order_details.html', context)
    total_orders_price = Order.objects.filter(user = request.user).aggregate(Sum('order_items__price'))
    price = total_orders_price['order_items__price__sum']
    if price == None:
        context = {'message': 'your order page is empty'}
        return render(request, 'order_details.html', context)
    tax = int(18/100*price)
    tax_price = price +tax
    order_product = get_order
    context = {'order_product':get_order,  'price':price, 'tax':tax, 'tax_price':tax_price}
    return render(request, 'order_details.html', context)

@login_required(login_url= '/ecommerce/')
def current_order(request):
    get_order = Order.objects.filter(Q(user = request.user.id) & Q(order_status = 'pending')).last()
    if get_order == None :
        context = {'message': 'your order page is empty'}
        return render(request, 'order_details.html', context)
    current_products = get_order.order_items.all()
    price_of_products = get_order.order_items.values('price').aggregate(Sum('price'))['price__sum']
    tax = int(18/100*price_of_products)
    total_price = price_of_products + tax
    return render(request, 'current_order.html',{'orders':current_products, 'detail':get_order, 'price_of_products':price_of_products, 'tax':tax, 'total':total_price} )

@login_required(login_url= '/ecommerce/')
def Create_order(request):
    user = request.user
    orders = Order.objects.create(user = request.user)
    orders.order_items.add(*Cart.objects.filter(Q(user = request.user) & Q(is_active = True)))
    inactive  = Cart.objects.filter(user = request.user)
    inactive.update(is_active = False)
    orders.save()
    return redirect(current_order)

@login_required(login_url= '/ecommerce/')
def Cancel_order(request, id):
    product = Cart.objects.get(id = id)
    product.delete()
    return redirect(Order_details) 

@login_required(login_url= '/ecommerce/')
def Wish_list_products(request,id):
    if request.method == "POST":
        wish_product = Product.objects.get(id = id)
        print(wish_product)
        obj,add_wish = Wish.objects.get_or_create(user = request.user)
        obj.favourite.add(wish_product)
        obj.save()
    return redirect(Product_list)

@login_required(login_url= '/ecommerce/')
def Show_wish(request):

    wished_products = Wish.objects.get(user = request.user)
    context = {'wish_list':wished_products.favourite.all()}
    return render(request, 'wish_list.html', context)

@login_required(login_url= '/ecommerce/')
def Remove_wish(request, id):
    if request.method == "POST":
        product_qs = Product.objects.get(id = id)
        wish_qs = Wish.objects.get(user = request.user)
        wish_qs.favourite.remove(product_qs)
    return redirect(Product_list)