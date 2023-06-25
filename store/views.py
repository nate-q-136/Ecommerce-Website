from django.shortcuts import render
from .models import *
import requests
from django.http import JsonResponse
import json
# Create your views here.
# ------- Đổ dữ liệu vào các trang-------
def store(request):
    if request.user.is_authenticated:
        
        customer = request.user.customer
        # get_or_create sẽ lỗi nếu có nhiều kết quả trả về, nó chỉ nên là 1 kq trả về
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # gọi tới bảng OrderItem có foreign key nối với bảng Order để lấy tất cả OrderItem có cùng order_id
        items = order.orderitem_set.all()
        cart_items = order.get_all_quantity
        pass
    else:
        items=[]
        order = {'get_cart_total':0,'get_all_quantity':0}
        cart_items = order['get_all_quantity']
        
    product= Product.objects.all()
    print("product:",len(product))
    # lưu ý: store.html lấy giá trị theo thuộc tính
    context = {'products':product,'cart_items':cart_items}
    # render trả về 1 HttpResponse, request: request đầu vào; template_name: page is used và page này nhận context vào để sài; context: the response
    return render(request, 'store/store.html',context)

def cart(request):
    # check login chưa
    if request.user.is_authenticated:
        
        customer = request.user.customer
        # get_or_create sẽ lỗi nếu có nhiều kết quả trả về, nó chỉ nên là 1 kq trả về
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # gọi tới bảng OrderItem có foreign key nối với bảng Order để lấy tất cả OrderItem có cùng order_id
        items = order.orderitem_set.all()
        cart_items = order.get_all_quantity
        pass
    else:
        items=[]
        order = {'get_cart_total':0,'get_all_quantity':0}
        cart_items = order['get_all_quantity']
        pass
    context = {"items":items,'order':order, 'cart_items':cart_items}
    return render(request, 'store/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        
        customer = request.user.customer
        # get_or_create sẽ lỗi nếu có nhiều kết quả trả về, nó chỉ nên là 1 kq trả về
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # gọi tới bảng OrderItem có foreign key nối với bảng Order để lấy tất cả OrderItem có cùng order_id
        items = order.orderitem_set.all()
        cart_items = order.get_all_quantity
        pass
    else:
        items=[]
        order = {'get_cart_total':0,'get_all_quantity':0}
        cart_items = order['get_all_quantity']
        pass
    context = {"items":items,'order':order,'cart_items':cart_items}
    return render(request, 'store/checkout.html',context)


#--------- API get,post,put,delete--------
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
