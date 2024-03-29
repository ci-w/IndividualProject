# Generated by Django 4.1.6 on 2023-02-08 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('making', '0003_project_requirements'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirements',
            name='dexterity',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='requirements',
            name='language',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='requirements',
            name='memory',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='requirements',
            name='vision',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')]),
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('skill_level', models.IntegerField()),
                ('requirements', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='making.requirements')),
            ],
        ),
    ]
