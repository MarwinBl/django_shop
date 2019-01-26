from django.urls import path, include

import authapp.views as authapp


urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('registration/', authapp.registration, name='registration'),
    path('edit/', authapp.edit, name='edit'),
    path('email-verify/<email>/<activation_key>', authapp.verify, name='verify'),
    path('verify/google/oauth2/', include('social_django.urls', namespace='social')),
]

