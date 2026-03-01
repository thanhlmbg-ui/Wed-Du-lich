from django import forms
from .models import DanhGia

class DanhGiaForm(forms.ModelForm):
    class Meta:
        model = DanhGia
        fields = ['soSao', 'noiDungBinhLuan']
        widgets = {
            'soSao': forms.RadioSelect,
            'noiDungBinhLuan': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Chia sẻ cảm nhận của bạn...'
            })
        }
