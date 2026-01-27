from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('gioiThieu/', views.gioiThieu, name='gioithieu'),
    path('chinhSach/', views.chinhSach, name='chinhsach'),
    path('lienHe/', views.lienHe, name='lienhe'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),

]
