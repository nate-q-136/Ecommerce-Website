from .models import *
import json


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        # get_or_create sẽ lỗi nếu có nhiều kết quả trả về, nó chỉ nên là 1 kq trả về
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # gọi tới bảng OrderItem có foreign key nối với bảng Order để lấy tất cả OrderItem có cùng order_id
        items = order.orderitem_set.all()
        cart_items = order.get_all_quantity
        pass
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cart_items = cookieData['cart_items']
        pass
    return {"items":items,'order':order,'cart_items':cart_items}


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
        print('request:',request)
        pass
    except:
        cart={}
        pass
    print('cart:',cart)
    items=[]
    order = {'get_cart_total':0,'get_all_quantity':0, 'shipping':False}
    cart_items = order['get_all_quantity']
    for i in cart:
        # nếu item bị xóa trong database thì khi thêm sẽ báo lỗi
        try:
            cart_items += cart[i]['quantity']
            product_id = i
            product = Product.objects.get(id=product_id)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_all_quantity']+=cart[i]['quantity']
            item = {
                'product':{
                    'id':product_id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                },
                'quantity':cart[i]['quantity']
            }
            if product.digital == False:
                order['shipping']=True
            items.append(item)
        except:
            pass
    return {"items":items, "order":order, "cart_items":cart_items}


def guestOrder(request,data):
    print("user not logged in")
    print("cookies:",request.COOKIES)
    # take data from cookies and request
    name = data['form']['name']
    email = data['form']['email']
    cookieData = cookieCart(request)
    items = cookieData['items']
    order = cookieData['order']
    cart_items = cookieData['cart_items']
    # save data
    customer,created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()
    # vì khi người khác đăng nhập vào thì phải tạo 1 order mới hoàn toàn, không có sẵn
    order = Order.objects.create(customer=customer,complete=False)
    
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    
    return customer, order
