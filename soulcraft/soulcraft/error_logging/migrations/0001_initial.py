# Generated by Django 4.2.11 on 2024-04-01 18:19

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ErrorLog",
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
                ("path", models.CharField(max_length=1024)),
                ("status_code", models.IntegerField()),
                ("method", models.CharField(max_length=10)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("error_message", models.TextField()),
            ],
        ),
    ]