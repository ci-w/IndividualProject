# Generated by Django 4.1.6 on 2023-02-08 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('making', '0005_remove_tool_requirements_requirements_tools'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requirements',
            name='tools',
        ),
        migrations.AddField(
            model_name='tool',
            name='requirements',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='making.requirements'),
            preserve_default=False,
        ),
    ]
