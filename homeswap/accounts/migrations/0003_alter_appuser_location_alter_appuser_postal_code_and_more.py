# Generated by Django 5.0.4 on 2024-05-04 11:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_rename_addresse_appuser_street"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appuser",
            name="location",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="appuser",
            name="postal_code",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="appuser",
            name="street",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
