# Generated by Django 2.1 on 2020-07-24 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0002_auto_20200724_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='closed_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='creation_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='last_activity_date',
            field=models.DateField(),
        ),
    ]
