from django.shortcuts import render
from .models import *
import requests
from django.http import JsonResponse
import json
# Create your views here.
# ------- Đổ dữ liệu vào các trang-------
def store(request):
    product= Product.objects.all()
    print("product:",len(product))
    # lưu ý: store.html lấy giá trị theo thuộc tính
    context = {'products':product}
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
        pass
    else:
        items=[]
        order = {'get_cart_total':0,'get_all_quantity':0}
        pass
    context = {"items":items,'order':order}
    return render(request, 'store/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        
        customer = request.user.customer
        # get_or_create sẽ lỗi nếu có nhiều kết quả trả về, nó chỉ nên là 1 kq trả về
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # gọi tới bảng OrderItem có foreign key nối với bảng Order để lấy tất cả OrderItem có cùng order_id
        items = order.orderitem_set.all()
        pass
    else:
        items=[]
        order = {'get_cart_total':0,'get_all_quantity':0}
        pass
    context = {"items":items,'order':order}
    return render(request, 'store/checkout.html',context)


#--------- API get,post,put,delete--------
def update_item(request):
    data= json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    print('Action:',action)
    print('Product:',product_id)
    return JsonResponse({"message":"item was added"},status= 200)
