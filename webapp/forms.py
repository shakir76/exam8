from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from webapp.models import Product, Review


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Найти')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'avatar']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['description', 'rating']

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating < 1 or rating > 5:
            raise ValidationError("Оценка должна быть от 1 до 5")
        return rating


class ReviewModeratForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['moderated', 'description', 'rating']
