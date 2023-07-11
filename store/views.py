from django.shortcuts import render
from .models import *
import requests
from django.http import JsonResponse
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from .utils import cookieCart,cartData, guestOrder
# Create your views here.
# ------- Đổ dữ liệu vào các trang-------
def store(request):
    data = cartData(request)
    cart_items = data['cart_items']
        
    product= Product.objects.all()
    print("product:",len(product))
    # lưu ý: store.html lấy giá trị theo thuộc tính
    context = {'products':product,'cart_items':cart_items}
    # render trả về 1 HttpResponse, request: request đầu vào; template_name: page is used và page này nhận context vào để sài; context: the response
    return render(request, 'store/store.html',context)

def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']
    context = {"items":items,'order':order, 'cart_items':cart_items}
    return render(request, 'store/cart.html',context)

def checkout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']
    
    context = {"items":items,'order':order,'cart_items':cart_items}
    return render(request, 'store/checkout.html',context)


#--------- API get,post,put,delete--------
# @csrf_exempt
def update_item(request):
    data= json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    print('Action:',action)
    print('Product:',product_id)
    # luông update item, lấy ra customer
    # láy product muon thêm
    customer = request.user.customer
    product = Product.objects.get(id = product_id)
    order,created = Order.objects.get_or_create(customer = customer, complete = False)
    order_item, created = OrderItem.objects.get_or_create(product = product, order=order)
    if action == "add":
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1
    order_item.save()
    if order_item.quantity == 0:
        order_item.delete()
        # order_item.save()
        
    return JsonResponse({"message":"item was added"},status= 200)

# @csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        
    else:
        customer, order = guestOrder(request,data)
        
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    
    if total == order.get_cart_total:
        order.complete = True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode']
        )
        
    return JsonResponse({"message":"Payment completed"},status=200)