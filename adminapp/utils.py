from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponseNotAllowed, JsonResponse


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
    template_name = 'adminapp/object_del_or_restore.html'
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


class AdminAjaxConfirmView(View):
    models_dict = {}

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        if self.request.is_ajax():
            _request = self.request.POST.dict()
            _action = _request['action']
            _model, _pk = _request['object'].split('/')
            if self.delete_or_restore_obj(self.models_dict[_model], _pk, _action):
                return JsonResponse({'status': True})
            else:
                return JsonResponse({'status': False,
                                     'message': 'Да прост вот ошибка'})
        return HttpResponseNotAllowed

    @staticmethod
    def delete_or_restore_obj(model, pk, action):
        try:
            object = model.objects.get(pk=pk)
            object.is_active = False if action == 'del' else True
            object.save()
        except:
            return False
        else:
            return True
