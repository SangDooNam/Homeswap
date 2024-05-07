# Generated by Django 5.0.4 on 2024-05-04 11:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_alter_appuser_location_alter_appuser_postal_code_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appuser",
            name="postal_code",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(100000),
                    django.core.validators.MaxValueValidator(999999),
                ],
            ),
        ),
    ]
