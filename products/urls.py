from django.urls import path

from products.views import MenuListView, ProductGroupsView, ProductGroupView

urlpatterns = [
	path('/menus', MenuListView.as_view()), 
    path('', ProductGroupsView.as_view()),
    path('/<int:id>', ProductGroupView.as_view()),
]