from django import forms
from .models import DanhGia

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
