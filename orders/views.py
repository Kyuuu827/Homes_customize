import json

from django.views     import View
from django.http      import JsonResponse
from django.db        import transaction

from orders.models    import Order, OrderItem, OrderStatus
from core.utils       import signin_decorator


class OrderItemView(View):
    @signin_decorator
    def post(self, request):
        try:            
            data = json.loads(request.body)
            user = request.user
            products = data["products"]

            with transaction.atomic():    
                order = Order.objects.create(
                    user_id    = user.id,
                    address    = user.address_set.all()[0],
                    status_id  = OrderStatus.Status.BEFORE_DEPOSIT.value
                )

                OrderItem.objects.bulk_create([
                    OrderItem(
                        order_id   = order.id,
                        product_id = product["id"],
                        color_id   = product["color_id"],
                        quantity   = product["quantity"],
                    ) for product in products
                ])

                order.status.id = OrderStatus.Status.DEPOSIT_COMPLTED.value

            return JsonResponse({'MESSAGE' : 'CREATED'}, status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status = 400)


    @signin_decorator
    def get(self, request):
        user_id = request.user.id
        
        order_items = OrderItem.objects.select_related('product', 'product__product_group').filter(order__user_id=user_id) \
            .prefetch_related('product__product_group__productimage_set')

        if not order_items.exists():
            return JsonResponse( {'MESSAGE' : 'EMPTY'}, status = 404)

        results = [
            {
                "product_img"  : order_item.product.product_group.productimage_set.first().image_url,
                "price"        : order_item.product.price,
                "name"         : order_item.product.name,
                "quantity"     : order_item.quantity
            } for order_item in order_items]
        
        return JsonResponse( {'MESSAGE' : results}, status = 201)


    @signin_decorator
    def patch(self, request, id):
        try:
            data     = json.loads(request.body)
            color_id = data['color_id']
            quantity = data['quantity']

            OrderItem.objects.filter(order__user_id=request.user.id, id=id).update(
                color_id   = color_id,
                quantity   = quantity
            )

            return JsonResponse({'MESSAGE' : 'ORDER INFORMATION UPDATED'}, status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status = 400)


    @signin_decorator
    def delete(self, request, id):
        OrderItem.objects.filter(order__user_id=request.user.id, id=id).delete()

        return JsonResponse({'MESSAGE' : 'ORDER INFORMATION DELETED'}, status = 201)