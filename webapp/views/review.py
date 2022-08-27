from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from webapp.forms import ReviewForm, SearchForm, ReviewModeratForm
from webapp.models import Review, Product


class IndexReView(ListView):
    model = Review
    template_name = "partial/list_partial.html"


class AddReview(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "reviews/create.html"
    moderators_form = ReviewModeratForm

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get("pk"))
        author = self.request.user
        form.instance.product = product
        form.instance.author = author
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:view_product', kwargs={'pk': self.object.product.pk})

    def get_form_class(self):
        if 'moderators' in self.request.user.groups.all().values_list('name', flat=True):
            return self.moderators_form
        else:
            return super().get_form_class()


class UpdateReview(PermissionRequiredMixin, UpdateView):
    form_class = ReviewForm
    template_name = 'reviews/update.html'
    model = Review
    moderators_form = ReviewModeratForm

    def get_form_class(self):
        if 'moderators' in self.request.user.groups.all().values_list('name', flat=True):
            return self.moderators_form
        else:
            return super().get_form_class()

    def get_success_url(self):
        return reverse('webapp:view_product', kwargs={'pk': self.object.product.pk})

    def has_permission(self):
        return self.request.user.is_superuser or \
               'moderators' in self.request.user.groups.all().values_list('name', flat=True) or \
               self.request.user == self.get_object().author


class DeleteReview(PermissionRequiredMixin, DeleteView):
    model = Review

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:view_product', kwargs={'pk': self.object.product.pk})

    def has_permission(self):
        return self.request.user.is_superuser or \
               'moderators' in self.request.user.groups.all().values_list('name', flat=True) or \
               self.request.user == self.get_object().author


class ListNotModerReView(PermissionRequiredMixin, ListView):
    model = Review
    template_name = "reviews/list_not_review.html"
    context_object_name = 'reviews'
    ordering = "-updated_at"
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Review.objects.filter(
                Q(author__icontains=self.search_value))
        return Review.objects.filter(moderated=False).order_by("-updated_at")

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

    def has_permission(self):
        return self.request.user.is_superuser or \
               'moderators' in self.request.user.groups.all().values_list('name', flat=True)
