from django.shortcuts import render, redirect, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.db import models
from django.db.models import Avg, Sum, F, Count, Q
from .models import *
from .forms import *
# Create your views here.

User = get_user_model()
#trang chủ
def home(request):
    diaDiem = DiaDiem.objects.all()
    context={ 'diaDiem': diaDiem}
    return render(request,'app/home.html',context)

#giỏ hàng
@login_required
def cart(request):
    datCho_list = DatCho.objects.filter(ma_nguoi_dung=request.user).order_by('-ngay_dat')
    return render(request,'app/cart.html', {'datCho_list': datCho_list})

#thanh toán
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            datCho = form.save(commit=False)
            datCho.ma_nguoi_dung = request.user
            datCho.save()
            return redirect('home')  # hoặc trang thông báo
    else:
        form = BookingForm()

    return render(request, 'app/booking.html', {'form': form})


#giới thiệu
def introduce(request):
    return render(request, 'app/introduce.html')

#chính sách web
def policy(request):
    return render(request, 'app/policy.html')

#liên hệ
def contact(request):
    return render(request, 'app/contact.html')

#đặt dịch vụ
def service(request):
    danhMuc = DanhMuc.objects.all()
    diaDiem = DiaDiem.objects.all()
    # lọc theo danh mục
    danh_muc_id = request.GET.get('danhMuc')
    if danh_muc_id:
        diaDiem = diaDiem.filter(ma_danh_muc_id=danh_muc_id)
    # tìm kiếm
    q = request.GET.get('q')
    if q:
        diaDiem = diaDiem.filter(ten_dia_diem__icontains=q)
    # sắp xếp
    sap_xep = request.GET.get('sapXep')
    if sap_xep == 'moi':
        diaDiem = diaDiem.order_by('-ngay_tao')
    elif sap_xep == 'cu':
        diaDiem = diaDiem.order_by('ngay_tao')

    return render(request, 'app/service.html', {
        'danhMuc': danhMuc,
        'diaDiem': diaDiem
    })

#chi tiết điểm
def detail(request, id):
    diem = get_object_or_404(DiaDiem, pk=id)
    danhGiaList = diem.danh_gia.all()

    form = DanhGiaForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        form = DanhGiaForm(request.POST)
        if form.is_valid():
            # Chặn đánh giá trùng
            daDanhGia = DanhGia.objects.filter(
                ma_nguoi_dung=request.user,
                ma_dia_diem=diem
            ).exists()

            if not daDanhGia:
                danhGia = form.save(commit=False)
                danhGia.ma_nguoi_dung = request.user
                danhGia.ma_dia_diem = diem
                danhGia.save()

            return redirect('chiTietDiem', id=id)

    return render(request, 'app/detail.html', {
        'diem': diem,
        'danhGiaList': danhGiaList,
        'form': form
    })

# Tìm kiếm
def search(request):
    query = request.GET.get('q', '')
    diaDiem_results = []
    tourDuLich_results = []

    if query:
        # Tìm kiếm trong DiaDiem
        diaDiem_results = DiaDiem.objects.filter(
            models.Q(ten_dia_diem__icontains=query) |
            models.Q(mo_ta__icontains=query) |
            models.Q(dia_chi__icontains=query)
        )

        # Tìm kiếm trong TourDuLich
        tourDuLich_results = TourDuLich.objects.filter(
            models.Q(ten_tour__icontains=query)
        )

    context = {
        'query': query,
        'diaDiem_results': diaDiem_results,
        'tourDuLich_results': tourDuLich_results,
    }
    return render(request, 'app/search.html', context)


#trang cá nhân
@login_required
def trangCaNhan(request):
    user = request.user
    dat_cho_list = DatCho.objects.filter(ma_nguoi_dung=user).order_by('-ngay_dat')
    danhGia_list = DanhGia.objects.filter(ma_nguoi_dung=user).order_by('-ngay_danh_gia')
    
    context = {
        'user': user,
        'dat_cho_list': dat_cho_list,
        'danhGia_list': danhGia_list,
    }
    return render(request, 'app/trangCaNhan.html', context)


# ======================
# AUTH
# ======================
#đăng nhập
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        # Kiểm tra email không được trống
        if not email:
            return render(request, 'app/login.html', {
                'mode': 'login',
                'error': 'Vui lòng nhập email'
            })

        # Kiểm tra mật khẩu không được trống
        if not password:
            return render(request, 'app/login.html', {
                'mode': 'login',
                'error': 'Vui lòng nhập mật khẩu'
            })

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
                'error': 'Email hoặc mật khẩu không chính xác'
            })

    return render(request, 'app/login.html', {
        'mode': 'login'
    })

#đăng ký
def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirmPassword', '')

        # Kiểm tra tên không được trống
        if not name:
            return render(request, 'app/login.html', {
                'mode': 'register',
                'error': 'Vui lòng nhập họ và tên'
            })

        # Kiểm tra email không được trống
        if not email:
            return render(request, 'app/login.html', {
                'mode': 'register',
                'error': 'Vui lòng nhập email'
            })

        # Kiểm tra mật khẩu không được trống
        if not password:
            return render(request, 'app/login.html', {
                'mode': 'register',
                'error': 'Vui lòng nhập mật khẩu'
            })

        # Kiểm tra mật khẩu khớp
        if password != confirm:
            return render(request, 'app/login.html', {
                'mode': 'register',
                'error': 'Mật khẩu không khớp'
            })

        # Kiểm tra độ dài mật khẩu
        if len(password) < 6:
            return render(request, 'app/login.html', {
                'mode': 'register',
                'error': 'Mật khẩu phải có ít nhất 6 ký tự'
            })

        # Kiểm tra email đã tồn tại
        if User.objects.filter(email=email).exists():
            return render(request, 'app/login.html', {
                'mode': 'register',
                'error': 'Email này đã được đăng ký'
            })

        if User.objects.filter(username=email).exists():
            return render(request, 'app/login.html', {
                'mode': 'register',
                'error': 'Email này đã tồn tại trong hệ thống'
            })

        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )
            auth_login(request, user)
            return redirect('home')
        except Exception as e:
            return render(request, 'app/login.html', {
                'mode': 'register',
                'error': 'Đã xảy ra lỗi khi đăng ký. Vui lòng thử lại.'
            })

    return render(request, 'app/login.html', {
        'mode': 'register'
    })

# Báo cáo thống kê
@login_required
def report(request):
    # Thống kê tổng quan
    total_diem = DiaDiem.objects.count()
    total_tour = TourDuLich.objects.count()
    total_dat_cho = DatCho.objects.count()
    total_danh_gia = DanhGia.objects.count()

    # 1. Thống kê số lượt đặt chỗ theo ngày/tháng
    dat_cho_by_month = DatCho.objects.extra(select={'month': "strftime('%%Y-%%m', ngay_dat)"}).values('month').annotate(count=Count('ma_dat_cho')).order_by('month')
    
    # Thống kê theo địa điểm
    dat_cho_by_diem = DatCho.objects.values('ma_tour__ma_dia_diem__ten_dia_diem').annotate(count=Count('ma_dat_cho')).order_by('-count')[:10]

    # 2. Điểm đến được đặt nhiều nhất
    top_diem_dat = DatCho.objects.values('ma_tour__ma_dia_diem__ten_dia_diem').annotate(count=Count('ma_dat_cho')).order_by('-count')[:10]

    # Điểm đến được đánh giá nhiều nhất
    top_diem_danh_gia = DanhGia.objects.values('ma_dia_diem__ten_dia_diem').annotate(count=Count('ma_danh_gia')).order_by('-count')[:10]

    # 3. Tỷ lệ trạng thái
    trang_thai_stats = DatCho.objects.values('trang_thai').annotate(count=Count('ma_dat_cho'))
    total_requests = total_dat_cho
    approved_rate = (DatCho.objects.filter(trang_thai='confirmed').count() / total_requests * 100) if total_requests > 0 else 0
    rejected_rate = (DatCho.objects.filter(trang_thai='cancelled').count() / total_requests * 100) if total_requests > 0 else 0
    pending_rate = (DatCho.objects.filter(trang_thai='pending').count() / total_requests * 100) if total_requests > 0 else 0

    # Thống kê cho DiaDiem
    diem_stats = []
    for diem in DiaDiem.objects.all():
        danh_gia_count = DanhGia.objects.filter(ma_dia_diem=diem).count()
        avg_rating = DanhGia.objects.filter(ma_dia_diem=diem).aggregate(Avg('so_sao'))['so_sao__avg'] or 0
        dat_count = DatCho.objects.filter(ma_tour__ma_dia_diem=diem).count()
        diem_stats.append({
            'diem': diem,
            'danh_gia_count': danh_gia_count,
            'avg_rating': round(avg_rating, 1),
            'dat_count': dat_count
        })

    # Thống kê cho TourDuLich
    tour_stats = []
    for tour in TourDuLich.objects.all():
        dat_tour_count = tour.dat_cho_list.count()
        tour_stats.append({
            'tour': tour,
            'dat_tour_count': dat_tour_count,
        })

    context = {
        'diem_stats': diem_stats,
        'tour_stats': tour_stats,
        'total_diem': total_diem,
        'total_tour': total_tour,
        'total_dat_cho': total_dat_cho,
        'total_danh_gia': total_danh_gia,
        'dat_cho_by_month': list(dat_cho_by_month),
        'dat_cho_by_diem': list(dat_cho_by_diem),
        'top_diem_dat': list(top_diem_dat),
        'top_diem_danh_gia': list(top_diem_danh_gia),
        'approved_rate': round(approved_rate, 1),
        'rejected_rate': round(rejected_rate, 1),
        'pending_rate': round(pending_rate, 1),
        'trang_thai_stats': list(trang_thai_stats),
    }
    return render(request, 'app/report.html', context)


