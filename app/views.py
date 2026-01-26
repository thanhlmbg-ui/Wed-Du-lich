from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    context={}
    return render(request,'app/home.html',context)
def cart(request):
    context={}
    return render(request,'app/cart.html',context)
def checkout(request):
    context={}
    return render(request,'app/checkout.html',context)
def login(request, mode):
    return render(request, 'app/login.html', {
        'mode': mode
    })
def login1(request, mode):
    return render(request, 'app/login.html')
