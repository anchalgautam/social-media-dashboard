# Generated by Django 5.1.4 on 2025-01-23 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('emailid', models.EmailField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('contact_no', models.IntegerField()),
            ],
        ),
    ]
