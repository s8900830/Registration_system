from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from .forms import SignUpForm, UserPorfileForm
from .models import UserProfile, QRCodeList
from datetime import datetime
from .change import mainfunction
from io import BytesIO
import qrcode
import base64
from PIL import Image

# Create your views here.


def home(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")

            next_param = request.GET.get('next', 'home')
            if not next_param or next_param.isspace():
                next_param = 'home'
            return redirect(next_param)
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
            user = form.save()
            default_group, created = Group.objects.get_or_create(
                name='Members')
            user.groups.add(default_group.id)

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


@login_required
def user_info(request):
    try:
        profile = UserProfile.objects.get(username=request.user)
    except UserProfile.DoesNotExist:
        form = UserPorfileForm()
        messages.success(
            request, "You Don't Have Any Profile! Please Add Your Profile!")
        return render(request, 'edit.html', {
            'form': form
        })
    return render(request, 'info.html', {
        'profile': profile,
    })


def QRcode(request):
    try:
        code = QRCodeList.objects.get(username=request.user)
    except QRCodeList.DoesNotExist:
        code = QRCodeList.objects.create(
            username=request.user, code=mainfunction.code(15))
        code.save()
    full_url = f"{request.scheme}://{request.get_host()}/{code.code}"
    qr_image = qrcode.make(full_url, box_size=10)
    qr_image_pil = qr_image.get_image()
    stream = BytesIO()
    qr_image_pil.save(stream, format='PNG')
    qr_image_data = stream.getvalue()
    qr_image_base64 = base64.b64encode(qr_image_data).decode('utf-8')
    return JsonResponse({'qr_code_base64': f'{qr_image_base64}'})


@login_required
def edit_info(request):
    if request.method == "POST":
        form = UserPorfileForm(request.POST)
        if form.is_valid():
            try:
                data = UserProfile.objects.get(username=request.user)
                profile = form.save(commit=False)

                profile.id = data.id
                profile.username = request.user
                profile.last_edited_at = datetime.now()
                profile.save()
            except UserProfile.DoesNotExist:
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

# 驗證使用者


@login_required
def verify(request, url_suffix):
    try:
        codeprofile = QRCodeList.objects.get(code=url_suffix)
        profile = UserProfile.objects.get(username=codeprofile.username)
    except QRCodeList.DoesNotExist:
        return redirect('home')

    return render(request, 'verify.html', {
        'profile': profile,
    })


def group_list(request):
    groups = Group.objects.all()
    return render(request, 'manage.html', {'groups': groups})


def change_permission(request):
    return render(request, 'change_permission.html', {

    })
