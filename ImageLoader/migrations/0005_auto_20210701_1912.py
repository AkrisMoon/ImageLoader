# Generated by Django 3.2.4 on 2021-07-01 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ImageLoader', '0004_auto_20210701_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='height',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='width',
            field=models.IntegerField(blank=True),
        ),
    ]
