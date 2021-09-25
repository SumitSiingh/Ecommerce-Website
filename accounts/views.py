from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from .filters import *
from .decorators import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url = 'login')
def homepage(request):
    order_count = Order.objects.all().count()
    pending_count = Order.objects.filter(status = 'Pending').count()
    delivered_count = Order.objects.filter(status = 'Delivered').count()
    last_5_orders = Order.objects.all().order_by('-date_created')[:5]
    all_customers = Customer.objects.all()

    context = {'order_count': order_count, 'delivered_count': delivered_count,
               'pending_count': pending_count, 'last_5_orders': last_5_orders,
               'all_customers': all_customers}

    return render(request, 'accounts/homepage.html', context)

@login_required(login_url = 'login')
def customer(request):
    order_count = Order.objects.filter(customer = request.user.id).count()
    all_orders = Order.objects.filter(customer = request.user.id)

    myfilter = OrderFilter(request.GET, queryset = all_orders)
    all_orders = myfilter.qs

    context = {'all_orders': all_orders, 'order_count': order_count, 'myfilter': myfilter}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url = 'login')
def product(request):
    all_products = Product.objects.all()

    context = {'all_products': all_products}
    return render(request, 'accounts/product.html', context)

@login_required(login_url = 'login')
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')

        else:
            return HttpResponse('Something went wrong, retry.')

    form = OrderForm()
    context = {'form': form}
    return render(request, 'accounts/create_order.html', context)

@login_required(login_url = 'login')
def update_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance = order)
        if form.is_valid():
            form.save()
            return redirect('customer', pk=order.customer_id)

    form = OrderForm(instance=order)
    context = {'form': form}
    return render(request, 'accounts/create_order.html', context)

@login_required(login_url = 'login')
def delete_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        button = request.POST.get('choice')
        if button == 'Delete':
            order.delete()
            return redirect('customer', pk=order.customer_id)
        else:
            return redirect('customer', pk=order.customer_id)

    form = OrderForm(instance=order)
    context = {'form': form}
    return render(request, 'accounts/delete_order.html', context)

@admin_or_logged_out_only
def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('first_name').capitalize()
            new_phone = form.cleaned_data.get('phone')
            new_user = form.save()

            Customer.objects.create(
            user = new_user,
            phone = new_phone
            )

            messages.success(request, f"Hey {user_name}, Your account is created, login now!")
            return redirect('login')
        else:
            for msg in form.error_messages:
                messages.error(request, msg)

    form = RegisterForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@admin_or_logged_out_only
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                messages.info(request, 'Username or password is invalid')
        else:
            return render(request, 'Something went wrong, retry.')

    form = LoginForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)

@login_required(login_url = 'login')
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url = 'login')
def user_profile(request):
    user = request.user.customer

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse('Somethig went wrong, retry')

    form = ProfileForm(instance = user)
    context = {'form': form}
    return render(request, 'accounts/profile.html', context)
