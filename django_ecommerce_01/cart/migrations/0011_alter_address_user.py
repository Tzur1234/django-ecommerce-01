# Generated by Django 4.2.3 on 2023-07-12 13:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("cart", "0010_remove_address_address_type_alter_address_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="user",
            field=models.OneToOneField(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]