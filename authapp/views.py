from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test, login_required
from django.conf import settings
from django.core.mail import send_mail

from authapp.forms import ShopUserLoginForm, ShopUserRegistrationForm, ShopUserEditForm
from authapp.models import ShopUser


def send_verify_email(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    title = f'Активация учетной записи {user.username}'
    message = f'''Для подтверждения учетной записи {user.username} на портале
                {settings.DOMAIN_NAME} перейдите по {settings.DOMAIN_NAME}{verify_link}'''
    html_message = f'''<div>Для подтверждения учетной записи {user.username} на портале
                {settings.DOMAIN_NAME} перейдите по <a href="{settings.DOMAIN_NAME}{verify_link}">ссылке</a>.</div>
                 <div>Если ссылка не открылась, скопируйте текст в адресную строку браузера</div>
                 <div style="background-color:#fff51f">{settings.DOMAIN_NAME}{verify_link}</div>'''
    return send_mail(title,
                     message,
                     settings.EMAIL_HOST_USER,
                     [user.email],
                     fail_silently=False,
                     html_message=html_message)


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

    context = {'login_form': login_form,
               'next': next_page
               }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('index')


@user_passes_test(lambda u: u.is_anonymous, login_url='index', redirect_field_name=None)
def registration(request):
    reg_form = ShopUserRegistrationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and reg_form.is_valid():
        user = reg_form.save()
        send_verify_email(user)
        return redirect('auth:login')
    return render(request, 'authapp/registration.html', {'reg_form': reg_form})


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
            auth.login(request, user)
        else:
            user.set_activation_key()
            user.save()
            send_verify_email(user)
            errors.update(key_expired='Истек срок ключа, мы отправили Вам новый')
    else:
        errors.update(validation='Ошибка валидации')
    return render(request, 'authapp/verification.html', context)