# Generated by Django 5.1.7 on 2025-04-11 07:17

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mysite", "0007_feedcomment_feedlike"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="feedlike",
            unique_together={("user", "content", "platform")},
        ),
    ]
