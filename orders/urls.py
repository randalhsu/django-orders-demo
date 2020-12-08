from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_order', views.add_order, name='add_order'),
    path('remove_order', views.remove_order, name='remove_order'),
    path('get_top_3_products', views.get_top_3_products, name='get_top_3_products'),
    path('get_shop_statistics', views.get_shop_statistics,
         name='get_shop_statistics'),
]
