from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.home,name='home'),
    path('cart/', views.cart, name='gioHang'),
    path('booking/', views.booking, name='thanhToan'),
    path('introduce/', views.introduce, name='gioiThieu'),
    path('policy/', views.policy, name='chinhSach'),
    path('contact/', views.contact, name='lienHe'),
    path('service/', views.service, name='datDichVu'),
    path('detail/<int:id>/', views.detail, name='chiTietDiem'),
    path('search/', views.search, name='timKiem'),
    path('trangCaNhan/', views.trangCaNhan, name='trangCaNhan'),
    path('report/', views.report, name='baoCao'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

]
