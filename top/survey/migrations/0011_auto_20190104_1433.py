# Generated by Django 2.0.2 on 2019-01-04 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0010_personchange'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personchange',
            name='email',
        ),
        migrations.RemoveField(
            model_name='personchange',
            name='father_name',
        ),
        migrations.RemoveField(
            model_name='personchange',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='personchange',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='personchange',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='personchange',
            name='phone_number2',
        ),
        migrations.RemoveField(
            model_name='personchange',
            name='position',
        ),
        migrations.AddField(
            model_name='clientchange',
            name='ch_type',
            field=models.CharField(default='Клиент', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clientchange',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='E-mail'),
        ),
        migrations.AddField(
            model_name='clientchange',
            name='father_name',
            field=models.CharField(blank=True, max_length=64, verbose_name='Отчество'),
        ),
        migrations.AddField(
            model_name='clientchange',
            name='first_name',
            field=models.CharField(blank=True, max_length=64, verbose_name='Имя'),
        ),
        migrations.AddField(
            model_name='clientchange',
            name='last_name',
            field=models.CharField(blank=True, max_length=64, verbose_name='Фамилия'),
        ),
        migrations.AddField(
            model_name='clientchange',
            name='phone_number',
            field=models.CharField(blank=True, max_length=14, verbose_name='Телефон'),
        ),
        migrations.AddField(
            model_name='clientchange',
            name='phone_number2',
            field=models.CharField(blank=True, max_length=14, verbose_name='Доп. телефон'),
        ),
        migrations.AddField(
            model_name='clientchange',
            name='position',
            field=models.CharField(blank=True, max_length=128, verbose_name='Должность'),
        ),
    ]
