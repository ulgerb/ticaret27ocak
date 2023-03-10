# Generated by Django 4.1.5 on 2023-03-10 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appMy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='product', verbose_name='Resim'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, verbose_name='Slug Kategori'),
        ),
        migrations.AlterField(
            model_name='color',
            name='slug',
            field=models.SlugField(blank=True, verbose_name='Slug Kategori'),
        ),
        migrations.AlterField(
            model_name='product',
            name='detail',
            field=models.TextField(max_length=800, verbose_name='Özellikler'),
        ),
        migrations.AlterField(
            model_name='product',
            name='text',
            field=models.TextField(max_length=1000, verbose_name='Açıklama'),
        ),
    ]
