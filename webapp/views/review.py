from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView

from webapp.forms import ReviewForm
from webapp.models import Review, Product


class IndexReView(ListView):
    model = Review
    template_name = "partial/list_partial.html"


class AddReview(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "reviews/create.html"


    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get("pk"))
        author = self.request.user
        form.instance.product = product
        form.instance.author = author
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:view_product', kwargs={'pk': self.object.product.pk})
