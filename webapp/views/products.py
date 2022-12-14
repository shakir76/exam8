from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from webapp.forms import SearchForm, ProductForm
from webapp.models import Product, Review


class ListProduct(ListView):
    model = Product
    template_name = "product/index.html"
    context_object_name = "products"
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Product.objects.filter(
                Q(name__icontains=self.search_value))
        return Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})
            context["query"] = query
            context["search"] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class CreateProduct(PermissionRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = "product/create.html"

    def has_permission(self):
        return self.request.user.is_superuser or \
               'moderators' in self.request.user.groups.all().values_list('name', flat=True)


class ProductView(DetailView):
    template_name = "product/view.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review = Review.objects.filter(product=self.object)
        averge_ratings = 0
        for a in review:
            if a.moderated:
                averge_ratings += a.rating
        averge_ratings /= len(review)
        context['averge_ratings'] = averge_ratings
        context['reviews'] = review
        return context


class UpdateProduct(PermissionRequiredMixin, UpdateView):
    form_class = ProductForm
    template_name = 'product/update.html'
    model = Product

    def has_permission(self):
        return self.request.user.is_superuser or \
               'moderators' in self.request.user.groups.all().values_list('name', flat=True)


class DeleteProduct(PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('webapp:index')

    def has_permission(self):
        return self.request.user.is_superuser or \
               'moderators' in self.request.user.groups.all().values_list('name', flat=True)
