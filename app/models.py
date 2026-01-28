from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
# BẢNG NGƯỜI_DÙNG
class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
#BẢNG ĐIỂM_DU_LỊCH
class DiemDuLich(models.Model):
    ten = models.CharField(max_length=200)
    mo_ta = models.TextField()
    dia_chi = models.CharField(max_length=200)
    gia_tham_khao = models.IntegerField()
    hinh_anh = models.ImageField(null=True,blank=True)
    ngay_tao = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.ten
    @property
    def hinh_anhURL(self):
        try:
            url = self.hinh_anh.url
        except:
            url = ''
        return url
#BẢNG TOUR_DU_LỊCH
class TourDuLich(models.Model):
    ten_tour = models.CharField(max_length=200)
    thoi_gian = models.IntegerField()
    gia_tour = models.DecimalField(max_digits=10, decimal_places=2)
    mo_ta = models.CharField(max_length=200, null=True, blank=True)

    diem_du_lich = models.ForeignKey(
        DiemDuLich,
        on_delete=models.CASCADE,
        related_name="tours"
    )

    def __str__(self):
        return self.ten_tour
#BẢNG ĐẶT_TOUR
class DatTour(models.Model):
    nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(TourDuLich, on_delete=models.CASCADE)

    ngay_dat = models.DateField(auto_now_add=True)
    so_luong_nguoi = models.IntegerField()

    trang_thai = models.CharField(
        max_length=20,
        choices=[
            ('cho', 'Chờ'),
            ('xac_nhan', 'Xác nhận'),
            ('huy', 'Hủy')
        ],
        default='cho'
    )
#BẢNG ĐÁNH_GIÁ
class DanhGia(models.Model):
    SAO_CHOICES = [(i, f"{i} sao") for i in range(1, 6)]

    nguoi_dung = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='danh_gia'
    )

    diem_du_lich = models.ForeignKey(
        DiemDuLich,
        on_delete=models.CASCADE,
        related_name='danh_gia'
    )

    so_sao = models.IntegerField(choices=SAO_CHOICES)
    noi_dung_binh_luan = models.TextField()

    ngay_danh_gia = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('nguoi_dung', 'diem_du_lich')
        ordering = ['-ngay_danh_gia']

    def __str__(self):
        return f"{self.nguoi_dung.username} - {self.so_sao}⭐"
