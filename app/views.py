from django.shortcuts import render, redirect, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .models import *
from .forms import DanhGiaForm

from .models import *
# Create your views here.

User = get_user_model()
def home(request):
    diemDuLich = DiemDuLich.objects.all()
    context={ 'diemDuLich': diemDuLich}
    return render(request,'app/home.html',context)

def cart(request):
    diemDuLich = DiemDuLich.objects.all()
    context = {"diemDuLich": diemDuLich}
    return render(request,'app/cart.html',context)

def checkout(request):
    diemDuLich = DiemDuLich.objects.all()
    context = {"diemDuLich": diemDuLich}
    return render(request,'app/checkout.html',context)

def gioiThieu(request):
    return render(request, 'app/gioiThieu.html')

def chinhSach(request):
    return render(request, 'app/chinhSach.html')

def lienHe(request):
    return render(request, 'app/lienHe.html')

def booking(request):
    diemDuLich = DiemDuLich.objects.all()
    context = {"diemDuLich": diemDuLich}
    return render(request, 'app/booking.html', context)

def chi_tiet_diem(request, id):
    diem = get_object_or_404(DiemDuLich, id=id)
    danh_gia_list = diem.danh_gia.all()

    form = DanhGiaForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        form = DanhGiaForm(request.POST)
        if form.is_valid():
            # Chặn đánh giá trùng
            da_danh_gia = DanhGia.objects.filter(
                nguoi_dung=request.user,
                diem_du_lich=diem
            ).exists()

            if not da_danh_gia:
                danh_gia = form.save(commit=False)
                danh_gia.nguoi_dung = request.user
                danh_gia.diem_du_lich = diem
                danh_gia.save()

            return redirect('chitietdiem', id=id)

    return render(request, 'app/chi_tiet_diem.html', {
        'diem': diem,
        'danh_gia_list': danh_gia_list,
        'form': form
    })


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


