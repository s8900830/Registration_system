from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from qr_code.qrcode.utils import QRCodeOptions
from .forms import SignUpForm, UserPorfileForm
from .models import UserProfile
from datetime import datetime

# Create your views here.


def home(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.success(
                request, "There Was An Error Logging In, Please Try Again")
            return redirect('home')
    else:
        return render(request, 'home.html', {

        })


def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticated and login
            # 驗證跟登入
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, "You Have Successfully Registered! Welcome!")
            return redirect('edit_info')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def user_info(request):
    profile = UserProfile.objects.get(username=request.user)
    return render(request, 'info.html', {
        'profile': profile,
    })


def adduserdata(request):
    pass


def QRcode(request):
    pass


@login_required
def edit_info(request):
    if request.method == "POST":
        form = UserPorfileForm(request.POST)
        if form.is_valid():
            # D 要重新命名
            C = UserProfile.objects.all()
            D = UserProfile.objects.get(username=request.user)
            if D:
                profile = form.save(commit=False)

                profile.id = D.id
                profile.username = request.user
                profile.last_edited_at = datetime.now()
                profile.save()
            else:
                profile = form.save(commit=False)
                profile.username = request.user
                profile.save()

            messages.success(request, "Change Success!")
            return redirect('home')
        else:
            messages.success(
                request, "There Was An Error Logging In, Please Try Again")
            return redirect('home')
    else:
        form = UserPorfileForm()
        return render(request, 'edit.html', {
            'form': form
        })
    # pass
