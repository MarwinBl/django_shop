from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from basketapp.models import Basket
from orderapp.forms import OrderItemForm
from orderapp.models import Order, OrderItem


class FormSetMixin(object):
    @staticmethod
    def init_formset(order=Order, order_item=OrderItem, form=OrderItemForm, extra=1):
        return inlineformset_factory(order, order_item, form=form, extra=extra)

    def get_formset(self, formsetargs=[], formsetkwargs={}, *initargs, **initkwargs):
        return self.init_formset(*initargs, **initkwargs)(
            *formsetargs,
            **formsetkwargs,
        )

    def get_formset_from_basket(self):
        basket_items = Basket.get_items(self.request.user)
        if basket_items:
            formset = self.get_formset(extra=len(basket_items))
            for num, form in enumerate(formset.forms):
                form.initial['product'] = basket_items[num].product
                form.initial['quantity'] = basket_items[num].quantity
        else:
            formset = self.get_formset()
        return formset

    def get_formset_from_post(self, instance=False):
        formsetkwargs = dict(
            data=self.request.POST,
            instance=self.object if instance else None,
        )
        return self.get_formset(formsetkwargs=formsetkwargs)

    def clear_basket(self):
        Basket.get_items(self.request.user).delete()


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreate(FormSetMixin, CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orderitems'] = (self.get_formset_from_post()
                                 if self.request.POST else self.get_formset_from_basket())
        return context

    def form_valid(self, form):
        formset = self.get_formset_from_post()
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
                self.clear_basket()

        if self.object.get_total_cost() == 0:
            self.object.delete()
        return super().form_valid(form)


class OrderUpdate(FormSetMixin, UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orderitems'] = (self.get_formset_from_post(instance=True)
                                 if self.request.POST
                                 else self.get_formset(formsetkwargs={'instance': self.object}))
        return context

    def form_valid(self, form):
        formset = self.get_formset_from_post(instance=True)
        with transaction.atomic():
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()
        return super().form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('order:list')


class OrderRead(DetailView):
    model = Order


def forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()
    return redirect('order:list')




