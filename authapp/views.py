from django.shortcuts import render, redirect
from django.contrib import auth

from authapp.forms import ShopUserLoginForm, ShopUserRegistrationForm, ShopUserEditForm


def login(request):
    login_form = ShopUserLoginForm(data=request.POST or None)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return redirect('index')

    context = {'login_form': login_form}
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('index')


def registration(request):
    reg_form = ShopUserRegistrationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and reg_form.is_valid():
        reg_form.save()
        return redirect('auth:login')
    return render(request, 'authapp/registration.html', {'reg_form': reg_form})


def edit(request):
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
        return render(request, 'mainapp/edit.html', {'edit_form': edit_form})
    edit_form = ShopUserEditForm(instance=request.user)
    return render(request, 'mainapp/edit.html', {'edit_form': edit_form})