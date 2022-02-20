from django.db import models

from core.models     import TimeStamp
from users.models    import User

class Menu(TimeStamp):
    name       = models.CharField(max_length=100)
    image_url  = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'menus'

class Category(TimeStamp):
    name = models.CharField(max_length=100)
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)

    class Meta:
        db_table = 'categories'

class SubCategory(TimeStamp):
    name     = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'

class ProductGroup(TimeStamp):
    name            = models.CharField(max_length=50)
    company         = models.CharField(max_length=50)
    displayed_price = models.DecimalField(max_digits=10, decimal_places=3)
    discount_rate   = models.DecimalField(max_digits=5, decimal_places=3)
    sub_category    = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    delivery        = models.ForeignKey("Delivery", on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_groups'

class Product(TimeStamp):
    name             = models.CharField(max_length=50)
    price            = models.DecimalField(max_digits=10, decimal_places=3)
    product_group    = models.ForeignKey('ProductGroup', on_delete=models.CASCADE)
    colors           = models.ManyToManyField("Color", related_name='products', through="ProductColor")

    class Meta:
        db_table = 'products'

class ProductImage(TimeStamp):
    image_url        = models.CharField(max_length=200)
    product_group    = models.ForeignKey('ProductGroup', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_images'

class ProductColor(TimeStamp):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    color   = models.ForeignKey('Color', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_colors'

class Color(TimeStamp):
    name = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'colors'

class Review(TimeStamp):
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    content        = models.CharField(max_length=500)
    star_rate      = models.DecimalField(max_digits=3, decimal_places=2)
    product_group  = models.ForeignKey('ProductGroup', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reviews'

class ReviewImage(TimeStamp):
    image_url  = models.CharField(max_length=200)
    review     = models.ForeignKey("Review", on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'review_images'

class Delivery(TimeStamp):
    delivery_type = models.CharField(max_length=50)
    payment_type  = models.CharField(max_length=50)
    delivery_fee  = models.DecimalField(max_digits=10, decimal_places=3)
    
    class Meta:
        db_table = 'deliveries'