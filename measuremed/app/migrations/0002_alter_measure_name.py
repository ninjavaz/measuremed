# Generated by Django 4.1.4 on 2022-12-30 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measure',
            name='name',
            field=models.CharField(default='', max_length=150),
        ),
    ]
