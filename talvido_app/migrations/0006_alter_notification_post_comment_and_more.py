# Generated by Django 4.2 on 2023-04-29 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("talvido_app", "0005_notification"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="post_comment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="talvido_app.postcomment",
                verbose_name="Post Comment",
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="post_comment_like",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="talvido_app.postcommentlike",
                verbose_name="Post Comment Like",
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="post_like",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="talvido_app.postlike",
                verbose_name="Post Like",
            ),
        ),
    ]
