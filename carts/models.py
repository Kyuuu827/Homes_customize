from django.db import models
from django.db.models.fields import IntegerField

from core.models     import TimeStamp
from users.models    import User
from products.models import Product, Color

class Cart(TimeStamp):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity   = models.IntegerField(default=0)
    color      = models.ForeignKey(Color, on_delete=models.CASCADE)

    class Meta:
        db_table = 'carts'