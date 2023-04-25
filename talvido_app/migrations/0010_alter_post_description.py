# Generated by Django 4.2 on 2023-04-21 04:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("talvido_app", "0009_post"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="description",
            field=models.TextField(
                blank=True, max_length=1000, null=True, verbose_name="Post Description"
            ),
        ),
    ]