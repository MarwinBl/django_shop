from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import reverse


def get_popup(status, message_list):
    return '<div class="errorlist">%s</div>' % ''.join([
        f'<div class="alert {status} alert-dismissible fade show" role="alert">\
        %s\
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">\
        <span aria-hidden="true">&times;</span>\
        </button>\
        </div>' % message for message in message_list])


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