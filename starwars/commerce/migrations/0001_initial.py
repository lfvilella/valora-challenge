# Generated by Django 3.0.8 on 2020-07-31 18:51

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
            name="Tool",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_change", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=50)),
                ("description", models.TextField()),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_change", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("open", "Open"), ("finished", "Finished")],
                        default="open",
                        max_length=20,
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="commerce.Tool",
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="Advertiser",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_change", models.DateTimeField(auto_now=True)),
                ("phone", models.CharField(max_length=20)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="commerce.Order",
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
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        blank=True,
                        choices=[("sp", "SP"), ("pr", "PR"), ("mg", "MG")],
                        max_length=2,
                        null=True,
                    ),
                ),
                (
                    "address",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "neighborhood",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("number", models.IntegerField(blank=True, null=True)),
                (
                    "complement",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    "city",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "cep",
                    models.CharField(blank=True, max_length=12, null=True),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="commerce.Order",
                    ),
                ),
            ],
        ),
    ]
