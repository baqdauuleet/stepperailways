# Generated by Django 4.2.6 on 2023-12-08 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('rid', models.AutoField(primary_key=True, serialize=False)),
                ('rating', models.TextField()),
                ('author', models.TextField()),
                ('text', models.TextField()),
            ],
        ),
    ]