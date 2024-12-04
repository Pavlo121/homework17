from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm, RegistrationForm, PasswordChangeFormCustom

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация успешна!")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'profiles/register.html', {'form': form})

def edit_profile_view(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлен!")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'profiles/edit_profile.html', {'form': form})

def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeFormCustom(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request.user, form)
            messages.success(request, "Пароль успешно изменен!")
            return redirect('profile')
    else:
        form = PasswordChangeFormCustom(request.user)
    return render(request, 'profiles/change_password.html', {'form': form})

def profile_view(request):
    return render(request, 'profiles/profile.html', {'user': request.user})
