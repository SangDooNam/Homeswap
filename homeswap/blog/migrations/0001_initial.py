# Generated by Django 5.0.4 on 2024-05-07 09:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0004_alter_appuser_postal_code"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("location", models.CharField(max_length=100)),
                ("max_capacity", models.PositiveIntegerField()),
                ("to_city", models.CharField(max_length=100)),
                ("date_period", models.DateField()),
                ("num_travelers", models.PositiveIntegerField()),
                ("description", models.TextField()),
                (
                    "home_photos",
                    models.ManyToManyField(
                        related_name="blog_posts", to="accounts.homephoto"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
