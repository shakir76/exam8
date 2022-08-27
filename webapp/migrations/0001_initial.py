# Generated by Django 4.1 on 2022-08-27 05:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('category', models.CharField(choices=[('other', 'Разное'), ('keyboard', 'Клавиатура'), ('block', 'Блок питания'), ('matrix', 'Матрица'), ('battery', 'Батарейка')], default='other', max_length=50, verbose_name='Категория')),
                ('description', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Описание')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars', verbose_name='Аватар')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'db_table': 'Product',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=2000, verbose_name='Описание')),
                ('rating', models.IntegerField(default=1, verbose_name='Оценка')),
                ('moderated', models.BooleanField(default=False, verbose_name='Промадерирование')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='webapp.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзыв',
                'db_table': 'Review',
            },
        ),
    ]
