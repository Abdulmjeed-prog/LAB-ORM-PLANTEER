from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from .forms import UserForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def sign_up(request:HttpRequest):
    if request.user.is_authenticated:
        return redirect('main:home_view')
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "You have benn register")
            return redirect('account:login_view')
        else:
            print(user_form.errors)
            messages.error(request, "something goes Wrong")
            return render(request, 'account/signup.html', {'user_form': user_form})
        
    return render(request, 'account/signup.html')

def login_view(request:HttpRequest):
    if request.user.is_authenticated:
        return redirect('main:home_view')
    if request.method == 'POST':
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])

        if user:
            login(request,user)
            messages.success(request, "Logged in successufly")
            return redirect('main:home_view')
        else:
            messages.error(request, "Your Username or Password is wrong, try again")
            
    
    return render(request, 'account/login.html')

def logout_view(request:HttpRequest):
    logout(request)
    response = redirect(request.GET.get("next"))
    return response
    
