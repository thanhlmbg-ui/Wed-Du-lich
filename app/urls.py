from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.home,name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('gioiThieu/', views.gioiThieu, name='gioithieu'),
    path('chinhSach/', views.chinhSach, name='chinhsach'),
    path('lienHe/', views.lienHe, name='lienhe'),
    path('booking/', views.booking, name='datdichvu'),
    path('chi_tiet_diem/<int:id>/', views.chi_tiet_diem, name='chitietdiem'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

]
