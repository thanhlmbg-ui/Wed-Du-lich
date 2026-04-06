from django import forms
from .models import DanhGia, DatCho, DiaDiem, TourDuLich, DanhMuc

class DanhGiaForm(forms.ModelForm):
    class Meta:
        model = DanhGia
        fields = ['so_sao', 'noi_dung_binh_luan']
        widgets = {
            'so_sao': forms.RadioSelect,
            'noi_dung_binh_luan': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Chia sẻ cảm nhận của bạn...'
            })
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = DatCho
        fields = ['ma_tour', 'start_date', 'end_date']
        widgets = {
            'ma_tour': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class DiaDiemForm(forms.ModelForm):
    class Meta:
        model = DiaDiem
        fields = ['ten_dia_diem', 'mo_ta', 'dia_chi', 'ma_danh_muc', 'anh_dai_dien']
        widgets = {
            'ten_dia_diem': forms.TextInput(attrs={'class': 'form-control'}),
            'mo_ta': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'dia_chi': forms.TextInput(attrs={'class': 'form-control'}),
            'ma_danh_muc': forms.Select(attrs={'class': 'form-control'}),
            'anh_dai_dien': forms.FileInput(attrs={'class': 'form-control'}),
        }

class TourDuLichForm(forms.ModelForm):
    class Meta:
        model = TourDuLich
        fields = ['ten_tour', 'thoi_gian', 'gia', 'ma_dia_diem']
        widgets = {
            'ten_tour': forms.TextInput(attrs={'class': 'form-control'}),
            'thoi_gian': forms.NumberInput(attrs={'class': 'form-control'}),
            'gia': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'ma_dia_diem': forms.Select(attrs={'class': 'form-control'}),
        }

class DanhMucForm(forms.ModelForm):
    class Meta:
        model = DanhMuc
        fields = ['ten_danh_muc', 'mo_ta']
        widgets = {
            'ten_danh_muc': forms.TextInput(attrs={'class': 'form-control'}),
            'mo_ta': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }