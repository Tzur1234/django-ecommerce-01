# Generated by Django 4.2.3 on 2023-07-09 17:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0002_product_image_alter_product_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
