import json

from django.http import JsonResponse
from django.views import View
from django.db.models import Sum

from users.models    import User
from products.models import Product, ProductGroup
from .models         import Cart
from core.utils      import signin_decorator

class CartListView(View):
    @signin_decorator
    def post(self, request):
        try :
            data = json.loads(request.body)
            product_id = data['ProductId']
            quantity   = data['quantity']
            color_id   = data['ColorId']
            user_id    = request.user.id

            cart, created = Cart.objects.get_or_create(
                product_id = product_id,
                color_id   = color_id,
                user_id    = user_id
            )

            cart.quantity +=quantity
            cart.save()

            return JsonResponse({'message' : 'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message' : 'NO_DATA'}, status=400)

    @signin_decorator
    def get(self, request):
        try:
            carts= Cart.objects.select_related('product','color','product__product_group', 'product__product_group__delivery').prefetch_related('product__product_group__productimage_set').filter(user_id = request.user.id)

            cart_items =[{
                'cart_id'  : cart.id,
                'product'  : {
                    'id'                     : cart.product.id,
                    'name'                   : cart.product.name,
                    'price'                  : cart.product.price,
                    'quantity'               : cart.quantity,
                    'image'                  : cart.product.product_group.productimage_set.all()[0].image_url,
                    'company'                : cart.product.product_group.company,
                    'color'                  : { 
                        'color_name' :cart.color.name,
                        'color_id'  :cart.color.id
                    },
                    'delivery_fee'           : cart.product.product_group.delivery.delivery_fee,
                    'delivery_payment_type'  : cart.product.product_group.delivery.payment_type
                }
            } for cart in carts]

            total_product_price = sum([cart.product.price*cart.quantity for cart in carts])
            prepayment_delivery_fee = sum([cart.product.product_group.delivery.delivery_fee for cart in carts if cart.product.product_group.delivery.payment_type == '선불'])
            payment_price = total_product_price + prepayment_delivery_fee

            return JsonResponse({'cart_items' : cart_items, 'total_product_price' :total_product_price, 'prepayment_delivery_fee' : prepayment_delivery_fee, 'payment_price' : payment_price }, status=200)

        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_CART'})

    @signin_decorator
    def delete(self, request, id):
        Cart.objects.filter(user_id=request.user.id, id=id).delete()

        return JsonResponse({'message' : 'SUCCESS'}, status=204)

    @signin_decorator
    def patch(self, request, id):
        data          = json.loads(request.body)
        cart          = Cart.objects.filter(user_id=request.user.id, id=id).update(quantity = data['quantity'])

        return JsonResponse({'message' : 'SUCCESS'}, status=200)