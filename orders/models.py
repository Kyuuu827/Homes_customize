from django.db import models
from django.db.models.fields import IntegerField

from core.models     import TimeStamp
from users.models    import User, Address
from products.models import Product, Color

class Order(TimeStamp):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    address      = models.ForeignKey(Address, on_delete=models.CASCADE)
    status       = models.ForeignKey("OrderStatus", on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'

class OrderItem(TimeStamp):
    order        = models.ForeignKey("Order", on_delete=models.CASCADE)
    product      = models.ForeignKey(Product, on_delete=models.CASCADE)
    color        = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity     = models.IntegerField(default=0)
    status       = models.CharField(max_length=30)

    class Meta:
        db_table = 'order_items'

class OrderStatus(TimeStamp):
    class Status(models.IntegerChoices):
        BEFORE_DEPOSIT   = 1 
        STAND_BY         = 2 
        DEPOSIT_COMPLTED = 3 
        CANCEL           = 4 

    description = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'order_statuses'

class Shipment(TimeStamp):
    order_item      = models.ForeignKey("OrderItem", on_delete=models.CASCADE)
    tracking_number = models.IntegerField(default=0)
    date            = models.DateField(auto_now=True)

    class Meta:
        db_table = 'shipments'