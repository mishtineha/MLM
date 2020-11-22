from django.shortcuts import render,redirect
from django.contrib.auth.models import User
# Create your views here.

def dashboard(request):
    return render(request, 'Neha/dashboard.html')

def add_new(request):
    print(request.POST)
    username = request.POST.get('username')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    password = username
    if username and email:
        User.objects.create_user(username=username, password=password, email=email)
        return redirect('dash')


    return render(request, 'Neha/add_new.html')