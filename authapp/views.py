from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test, login_required

from authapp.forms import ShopUserLoginForm, ShopUserRegistrationForm, ShopUserEditForm
from authapp.models import ShopUser
from authapp.utills import send_verify_email, get_popup


@user_passes_test(lambda u: u.is_anonymous, login_url='index', redirect_field_name=None)
def login(request):
    login_form = ShopUserLoginForm(data=request.POST or None)
    index_page = reverse('index')
    next_page = request.GET.get('next', index_page)
    if request.method == 'POST' and login_form.is_valid():
        username, password = request.POST['username'], request.POST['password']
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect(request.POST.get('next', index_page))

    context = {
        'login_form': login_form,
        'next': next_page
        }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('index')


@user_passes_test(lambda u: u.is_anonymous, login_url='index', redirect_field_name=None)
def registration(request):
    reg_form = ShopUserRegistrationForm(request.POST or None, request.FILES or None)
    popup = ''
    if request.method == 'POST' and reg_form.is_valid():
        user = reg_form.save()
        send_verify_email(user)
        popup = get_popup('alert-info', [
            'На Вашу почту отправлено письмо, перейдите по ссылке для завершения регистрации.'
        ])
    return render(request, 'authapp/registration.html', {
        'reg_form': reg_form,
        'popup': popup,
    })


@login_required
def edit(request):
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
        return render(request, 'authapp/edit.html', {'edit_form': edit_form})
    edit_form = ShopUserEditForm(instance=request.user)
    return render(request, 'authapp/edit.html', {'edit_form': edit_form})


def verify(request, email, activation_key):
    user = get_object_or_404(ShopUser, email=email)
    errors = {}
    context = dict(errors=errors)
    if user.activation_key == activation_key and not user.is_active:
        if not user.activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        else:
            user.set_activation_key()
            user.save()
            send_verify_email(user)
            errors.update(key_expired='Истек срок ключа, мы отправили Вам новый')
    else:
        return HttpResponseNotFound()
    return render(request, 'authapp/verification.html', context)