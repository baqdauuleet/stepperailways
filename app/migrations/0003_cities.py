# Generated by Django 4.2.6 on 2023-12-08 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_reviews'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('cid', models.AutoField(primary_key=True, serialize=False)),
                ('city', models.TextField()),
            ],
        ),
    ]
