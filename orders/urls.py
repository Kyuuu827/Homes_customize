from django.urls import path

from orders.views import OrderItemView

urlpatterns = [
	path('', OrderItemView.as_view()),
	path('/<int:id>', OrderItemView.as_view()),
]