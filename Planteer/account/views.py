from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from .forms import ProfileForm, CustomUserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.db import transaction

# Create your views here.

def sign_up(request:HttpRequest):
    if request.user.is_authenticated:
        return redirect('main:home_view')
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST,request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                new_user = user_form.save()
                profile = profile_form.save(commit=False)
                profile.user = new_user
                profile_form.save()
                messages.success(request, "You have been register")
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

def profile_view(request:HttpRequest,user_name):
    user = User.objects.get(username = user_name)
    print(user)
    user_profile = user.profile
    return render(request, 'account/profile.html',{'user_profile': user_profile})
    
