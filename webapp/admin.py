from django.contrib import admin


# Register your models here.
from webapp.models import Product, Review


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']
    list_filter = ['name']
    search_fields = ['name']
    fields = ['name', 'category', 'description', 'avatar']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'author']
    list_display_links = ['author']
    list_filter = ['author']
    search_fields = ['author']
    fields = ['author', 'product', 'description', 'rating', 'moderated', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
