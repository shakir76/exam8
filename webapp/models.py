from django.contrib.auth import get_user_model
from django.db import models

STATUS_CODE = [('other', 'Разное'), ('keyboard', 'Клавиатура'), ('block', 'Блок питания'),
               ('matrix', 'Матрица'), ('battery', 'Батарейка'), ]


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name="Название")
    category = models.CharField(max_length=50, choices=STATUS_CODE, verbose_name="Категория", default=STATUS_CODE[0][0])
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name="Описание")
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True, verbose_name="Аватар")

    def __str__(self):
        return f"{self.id}. {self.name}: {self.category}"

    class Meta:
        db_table = "Product"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Review(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="authors",
                               verbose_name="Автор")
    product = models.ForeignKey('webapp.Product', on_delete=models.CASCADE, related_name="products",
                                verbose_name="Продукт")
    description = models.TextField(max_length=2000, null=False, blank=False, verbose_name="Описание")
    rating = models.IntegerField(verbose_name="Оценка", default=1)
    moderated = models.BooleanField(default=False, verbose_name="Промадерирование")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return f"{self.id}. {self.author}: {self.product}"

    class Meta:
        db_table = "Review"
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзыв"
