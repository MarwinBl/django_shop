from django.urls import path
import basketapp.views as basketapp


urlpatterns = [
    path('', basketapp.index, name='index'),
    path('add/<slug:slug>/', basketapp.add_product, name='add'),
    path('del/<slug:slug>/<int:quantity>', basketapp.del_product, name='del'),
]