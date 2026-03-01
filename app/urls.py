from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.home,name='home'),
    path('cart/', views.cart, name='gioHang'),
    path('checkout/', views.checkout, name='thanhToan'),
    path('introduce/', views.introduce, name='gioiThieu'),
    path('policy/', views.policy, name='chinhSach'),
    path('contact/', views.contact, name='lienHe'),
    path('booking/', views.booking, name='datDichVu'),
    path('detail/<int:id>/', views.detail, name='chiTietDiem'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

]
