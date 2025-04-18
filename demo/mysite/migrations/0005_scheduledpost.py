# Generated by Django 5.1.7 on 2025-04-10 15:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mysite", "0004_remove_userprofile_user_profile_delete_post_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ScheduledPost",
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
                ("content", models.TextField()),
                (
                    "platform",
                    models.CharField(
                        choices=[
                            ("twitter", "Twitter"),
                            ("facebook", "Facebook"),
                            ("both", "Both"),
                        ],
                        max_length=10,
                    ),
                ),
                ("scheduled_time", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("posted", models.BooleanField(default=False)),
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
