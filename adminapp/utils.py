from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.urls import reverse_lazy


class AdminBaseView(View):
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class AdminListView(AdminBaseView, ListView):
    pass


class AdminCreateView(AdminBaseView, CreateView):
    template_name = 'adminapp/object_update.html'


class AdminUpdateView(AdminBaseView, UpdateView):
    template_name = 'adminapp/object_update.html'


class AdminDetailView(AdminBaseView, DetailView):
    pass


class AdminDeleteView(AdminBaseView, DeleteView):
    success_url_kwargs = None
    object_name = None
    is_active = False

    def get_success_url(self):
        return reverse_lazy(self.success_url, kwargs=self.get_success_url_kwargs())

    def get_success_url_kwargs(self):
        return self.success_url_kwargs

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = self.is_active
        self.object.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['is_active'] = self.is_active
        return context

