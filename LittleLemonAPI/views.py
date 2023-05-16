from rest_framework import generics, status, viewsets
from .models import *
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render, redirect
from .serializers import CategorySerializer, MenuItemSerializers
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import AnonRateThrottle
from .throttles import TenCallsPerMinute
from django.contrib.auth.models import User, Group
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UpdateProfileForm
from .forms import SignupFrom
from django.http import JsonResponse
import json
def profile_view(request, username=None):
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
    else:
        user = current_user
    return render(request, 'LittleLemonAPI/perfil.html', {'user': user, 'cartItems': cartItems})

@login_required
def change_avatar(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('Profile', username=request.user.username)
    else:
        form = UpdateProfileForm(instance=profile)
    return render(request, 'LittleLemonAPI/change_avatar.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupFrom(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Usuario {username} Creado')
            return redirect('login')
    else:
        form = SignupFrom()
    return render(request, 'LittleLemonAPI/sign_up.html', {'form':form})





def ViewsHome(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    query = request.GET.get('q')
    items = []

    if query:
        items = MenuItem.objects.filter(title__icontains=query)

    return render(request, 'LittleLemonAPI/home.html', {'cartItems': cartItems, 'query': query, 'items': items})

def search(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    query = request.GET.get('q')
    items = MenuItem.objects.filter(category__title__icontains=query)

    content = {
        'query': query,
        'items': items,
        'cartItems': cartItems
    }
    return render(request, 'LittleLemonAPI/search.html', content)


class ViewPerfil(generic.ListView):
    template_name = 'LittleLemonAPI/perfil.html'
    model = User

class CreateCategory(generic.CreateView):
    template_name = 'LittleLemonAPI/add_category.html'
    model = Category
    fields = ['id', 'slug', 'title']

class WriteMenu(generic.CreateView):
    template_name = 'LittleLemonAPI/add_menu.html'
    model = MenuItem
    fields = ['title', 'price', 'inventory', 'category', 'image']

def updateitem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(productId)
    print(action)
    customer = request.user.profile
    product = MenuItem.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was Added', safe=False)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        total = order.get_cart_total
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    context = {'items': items, 'cartItems': cartItems, 'total': total}
    return render(request, 'LittleLemonAPI/cart.html', context)



def viewmenu(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']


    data = MenuItem.objects.all()
    paginator = Paginator(data, 9)
    page_number = request.GET.get('page')
    items = paginator.get_page(page_number)
    return render(request, 'LittleLemonAPI/menu.html', {'items': items, 'cartItems': cartItems})


#----------------filter option----------------
class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializers
    ordering_fields = ['price', 'inventory']
    search_fields = ['title', 'category__title']

@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        #-----------filter and ordening----------------
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        #----------------pagination--------------------#
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price=to_price)
        if search:
            items = items.filter(title__startswith=search)
        if ordering:
            ordering_fields = ordering.split(',')
            items = items.order_by(*ordering_fields)
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
        serializer_item = MenuItemSerializers(items, many=True)
        return Response(serializer_item.data)
    if request.method == 'POST':
        serializer_item = MenuItemSerializers(data=request.data)
        serializer_item.is_valid(raise_exception=True)
        serializer_item.save()
        return Response(serializer_item.data, status.HTTP_201_CREATED)

@api_view()
def single_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    serializer_item = MenuItemSerializers(item)
    return Response(serializer_item.data)

@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer_category = CategorySerializer(category)
    return Response(serializer_category.data)












@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"Message":"Secret Message"})

@api_view()
@permission_classes([IsAuthenticated])
def me(request):
    return Response(request.user.email)

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({'message':'Only Manager Should see this'})
    else:
        return Response({'message':'You are not Authorized'}, 403)

@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({'Message':'Successful'})

@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
    return Response({'Message':'Messsage for the logged user only'})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name='Manager')
        if request.method == "POST":
            managers.user_set.add(user)
        elif request.method == "DELETE":
            managers.user_set.remove(user)
        return Response({'Message':'OK'})
    return Response({'Message':'Error'}, status.HTTP_400_BAD_REQUEST)