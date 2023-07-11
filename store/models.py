from django.db import models
from django.contrib.auth.models import User

"""
Ý nghĩa của các mô hình:

Customer: Đại diện cho khách hàng. Mô hình này chứa thông tin về tên, email và các chi tiết khác của khách hàng.

Product: Đại diện cho sản phẩm. Mô hình này chứa thông tin về tên, giá và các chi tiết khác của sản phẩm.

Order: Đại diện cho đơn hàng. Mô hình này liên kết với khách hàng thông qua khóa ngoại, lưu trữ ngày đặt hàng và trạng thái hoàn thành của đơn hàng.

OrderItem: Đại diện cho các mặt hàng trong đơn hàng. Mô hình này liên kết với đơn hàng và sản phẩm thông qua khóa ngoại, lưu trữ số lượng của các loại sản phẩm được đặt mua trong đơn hàng.

ShippingAddress: Đại diện cho địa chỉ giao hàng. Mô hình này liên kết với khách hàng và đơn hàng thông qua khóa ngoại, lưu trữ địa chỉ giao hàng và các chi tiết khác của địa chỉ.

Với mô hình này, bạn có thể lưu trữ thông tin về khách hàng, sản phẩm, đơn hàng, mặt hàng trong đơn hàng và địa chỉ giao hàng trong cơ sở dữ liệu của Django. 
Bằng cách tương tác với các đối tượng được tạo từ mô hình này, bạn có thể thực hiện các hoạt động như tạo đơn hàng mới, thêm mặt hàng vào đơn hàng, 
lưu trữ địa chỉ giao hàng và nhiều hoạt động khác liên quan đến hệ thống đặt hàng của bạn.
"""

# Create your models here.
class Customer(models.Model):
    # one customer is only one user, if user is deleted the customer is deleted too, 2 thằng đều có khóa ngoại hướng tới primary key thằng kia
    user = models.OneToOneField(User, on_delete=models.CASCADE, null= True, blank=True)
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    
    # dùng để show trên admin page, hoặc query model
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    name = models.CharField(max_length=255,null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    # check if digital or physical, 
    # digital là tệp video, sách điện tử,pdf... thường dùng để download về máy
    # physical là quần áo, đồ điện tử,... cần được ship tới nơi cụ thể
    digital = models.BooleanField(default=False, null=True, blank=True)
    # image, thì phải tải library Pilow
    image = models.ImageField(null = True, blank=True)
    
    def __str__(self) -> str:
        return self.name
    
    # set phương thức làm thuộc tính cho Product
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    pass

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank = True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    # Check order được giao tới chưa
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=255, null=True)
    
    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total =sum([order_item.get_total_item for order_item in order_items])
        return total
    
    @property
    def get_all_quantity(self):
        order_items = self.orderitem_set.all()
        total_quantity = sum([order_item.quantity for order_item in order_items])
        return total_quantity
    
    @property
    def shipping(self):
        shipping = False
        order_items = self.orderitem_set.all()
        for i in order_items:
            if i.product.digital == False:
                shipping = True
        return shipping
    pass

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total_item(self):
        total = self.quantity * self.product.price
        return total
    pass

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    # set 1 ship cho 1 order
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True,null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    state= models.CharField(max_length=255, null=True)
    zipcode = models.CharField(max_length=255, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address
    pass

