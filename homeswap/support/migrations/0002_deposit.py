# Generated by Django 5.0.4 on 2024-06-02 19:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("messaging", "0003_message_room"),
        ("support", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Deposit",
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
                ("sender_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "receiver_amount",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_paid_by_sender", models.BooleanField(default=False)),
                ("is_paid_by_receiver", models.BooleanField(default=False)),
                (
                    "receiver_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="room_receiver_deposit",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "room",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chat_room_deposit",
                        to="messaging.room",
                    ),
                ),
                (
                    "sender_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="room_sender_deposit",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
