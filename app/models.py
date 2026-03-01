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
    moTa = models.TextField()
    diaChi = models.CharField(max_length=200)
    giaThamKhao = models.IntegerField()
    hinhAnh = models.ImageField(null=True,blank=True)
    ngayTao = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.ten
    @property
    def hinhAnhURL(self):
        try:
            url = self.hinhAnh.url
        except:
            url = ''
        return url
#BẢNG TOUR_DU_LỊCH
class TourDuLich(models.Model):
    tenTour = models.CharField(max_length=200)
    thoiGian = models.IntegerField()
    giaTour = models.DecimalField(max_digits=10, decimal_places=2)
    moTa = models.CharField(max_length=200, null=True, blank=True)

    diemDuLich = models.ForeignKey(
        DiemDuLich,
        on_delete=models.CASCADE,
        related_name="tours"
    )

    def __str__(self):
        return self.tenTour
#BẢNG ĐẶT_TOUR
class DatTour(models.Model):
    nguoiDung = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(TourDuLich, on_delete=models.CASCADE)

    ngayDat = models.DateField(auto_now_add=True)
    soLuongNguoi = models.IntegerField()

    trangThai = models.CharField(
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
    sao = [(i, f"{i} sao") for i in range(1, 6)]

    nguoiDung = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='danhGia'
    )

    diemDuLich = models.ForeignKey(
        DiemDuLich,
        on_delete=models.CASCADE,
        related_name='danhGia'
    )

    soSao = models.IntegerField(choices=sao)
    noiDungBinhLuan = models.TextField()

    ngayDanhGia = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('nguoiDung', 'diemDuLich')
        ordering = ['-ngayDanhGia']

    def __str__(self):
        return f"{self.nguoiDung.username} - {self.soSao}⭐"
