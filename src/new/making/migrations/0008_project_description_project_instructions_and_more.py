# Generated by Django 4.1.6 on 2023-02-08 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('making', '0007_userprofile_requirements'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.TextField(default='hi', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='instructions',
            field=models.TextField(default='hi'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='requirements',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='making.requirements'),
            preserve_default=False,
        ),
    ]