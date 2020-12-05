from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_order', views.add_order, name='add_order'),
    path('remove_order', views.remove_order, name='remove_order'),
]
