# Generated by Django 2.0.2 on 2018-12-29 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0008_auto_20181229_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='ending',
            field=models.TextField(blank=True, verbose_name='Завершающий блок'),
        ),
        migrations.AlterField(
            model_name='block',
            name='dell',
            field=models.TextField(blank=True, verbose_name='Заказывают Dell'),
        ),
        migrations.AlterField(
            model_name='block',
            name='emc',
            field=models.TextField(blank=True, verbose_name='Заказывают EMC'),
        ),
        migrations.AlterField(
            model_name='block',
            name='huawei',
            field=models.TextField(blank=True, verbose_name='Заказывают Huawei'),
        ),
        migrations.AlterField(
            model_name='block',
            name='sugon',
            field=models.TextField(blank=True, verbose_name='Заказывают SUGON'),
        ),
    ]
