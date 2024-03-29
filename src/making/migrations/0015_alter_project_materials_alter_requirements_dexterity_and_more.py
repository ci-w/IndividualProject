# Generated by Django 4.1.6 on 2023-03-23 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('making', '0014_tool_unique_tool'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='materials',
            field=models.TextField(default='materials here', max_length=300),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='requirements',
            name='dexterity',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=1, help_text='This is how much you can use your hands.'),
        ),
        migrations.AlterField(
            model_name='requirements',
            name='language',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=1, help_text='This is what sort of words you can understand.'),
        ),
        migrations.AlterField(
            model_name='requirements',
            name='memory',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=1, help_text='This is what your memory is like.'),
        ),
        migrations.AlterField(
            model_name='requirements',
            name='vision',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=1, help_text="This is how much you can see. For 'low': <br> like this"),
        ),
        migrations.AlterField(
            model_name='tool',
            name='skill_level',
            field=models.IntegerField(choices=[(0, 'None'), (1, 'Low'), (2, 'Medium'), (3, 'High')]),
        ),
    ]
