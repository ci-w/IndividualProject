# Generated by Django 3.2.16 on 2022-10-27 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('making', '0002_auto_20221026_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=' '),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(default=' '),
            preserve_default=False,
        ),
    ]
