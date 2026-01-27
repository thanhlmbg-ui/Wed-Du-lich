from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .models import *
# Create your views here.

User = get_user_model()
def home(request):
    diemDuLich = DiemDuLich.objects.all()
    context={ 'diemDuLich': diemDuLich}
    return render(request,'app/home.html',context)

def cart(request):
    context={}
    return render(request,'app/cart.html',context)

def checkout(request):
    context={}
    return render(request,'app/checkout.html',context)

def gioiThieu(request):
    return render(request, 'app/gioiThieu.html')

def chinhSach(request):
    return render(request, 'app/chinhSach.html')

def lienHe(request):
    return render(request, 'app/lienHe.html')
# ======================
# AUTH
# ======================

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'app/login.html', {
                'mode': 'login',
                'error': 'Email hoặc mật khẩu không đúng'
            })

    return render(request, 'app/login.html', {
        'mode': 'login'
    })


def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirmPassword')

        if password != confirm:
            return render(request, 'app/login.html', {
                'mode': 'register',
                'error': 'Mật khẩu không khớp'
            })

        if User.objects.filter(username=email).exists():
            return render(request, 'app/login.html', {
                'mode': 'register',
                'error': 'Email đã tồn tại'
            })

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        auth_login(request, user)
        return redirect('home')

    return render(request, 'app/login.html', {
        'mode': 'register'
    })


