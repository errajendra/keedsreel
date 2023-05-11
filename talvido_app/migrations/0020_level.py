# Generated by Django 4.2 on 2023-05-10 12:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("talvido_app", "0019_alter_subscription_validity_referraluser"),
    ]

    operations = [
        migrations.CreateModel(
            name="Level",
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
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("level", models.CharField(max_length=100)),
                ("name", models.CharField(max_length=100)),
                ("description", models.CharField(max_length=200)),
                ("min_points", models.IntegerField(verbose_name="Minimum point")),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="levels/", verbose_name="Image"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
