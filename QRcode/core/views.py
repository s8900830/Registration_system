from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group,User
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
        messages.error(
                request, "找不到相關 QRcode")
        return redirect('home')

    return render(request, 'info.html', {
        'profile': profile,
        'codeprofile':codeprofile
    })

@login_required
def group(request):
    groups = Group.objects.all()
    return render(request, 'manage.html', {'groups': groups})

@login_required
def group_list(request,pk,action):
    groups = Group.objects.all()
    if pk == None:
        return render(request, 'manage.html', {'groups': groups})
    else:
        if action == 'verify':
            try:
                profile = UserProfile.objects.get(id=pk)
                codeprofile = QRCodeList.objects.get(username=profile.username)
                codeprofile.verify = 1
                codeprofile.admin_verify=request.user.username
                codeprofile.save()
            except UserProfile.DoesNotExist:
                return redirect('manage')
            messages.success(
                request, "User Verifyed")
            return render(request, 'manage.html', {
                'groups': groups
            })
        elif action == "cancel":
            try:
                profile = UserProfile.objects.get(id=pk)
                codeprofile = QRCodeList.objects.get(username=profile.username)
                codeprofile.verify = 0
                codeprofile.admin_verify=""
                codeprofile.save()
            except UserProfile.DoesNotExist:
                return redirect('manage')
            messages.success(
                request, "Canel Verify User")
            return render(request, 'manage.html', {
                'groups': groups
            })
        
@login_required
def change_permission(request,pk):
    try:
        profile = UserProfile.objects.get(username=pk)
        codeprofile = QRCodeList.objects.get(username=profile.username)
    except UserProfile.DoesNotExist:
                messages.success(request, "Not Find Any UserData")
                return redirect('manage')
    except QRCodeList.DoesNotExist:
            messages.success(request, "QRCode Not Create")
            return render(request, 'change_permission.html', {
            'profile':profile,
        })
    return render(request, 'change_permission.html', {
        'profile':profile,
        'codeprofile':codeprofile
    })

@login_required
def admin_user_edit(request,pk):
    if request.method == "POST":
        change_group = request.POST["change_group"]
        profile = UserProfile.objects.get(pk=pk)
        user = User.objects.get(username=profile.username)
        default_group, created = Group.objects.get_or_create(name=change_group)
        user.groups.clear()
        user.groups.add(default_group.id)
        messages.success(request, f"{change_group}")
        return redirect('manage')
    else:
        return redirect('manage')
