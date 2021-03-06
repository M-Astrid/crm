# Generated by Django 2.0.2 on 2019-01-14 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0017_auto_20190112_1910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientchange',
            name='crimea',
        ),
        migrations.RemoveField(
            model_name='clientchange',
            name='imp',
        ),
        migrations.RemoveField(
            model_name='clientchange',
            name='sanctions',
        ),
        migrations.RemoveField(
            model_name='clientchange',
            name='type',
        ),
        migrations.AddField(
            model_name='clientchange',
            name='delete',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='item',
            name='product_type',
            field=models.CharField(choices=[('Сервер', (('форм-фактор Rack', 'форм-фактор Rack'), ('форм-фактор Tower', 'форм-фактор Tower'), ('блейд-сервер', 'блейд-сервер'))), ('СХД', (('начального уровня', 'начального уровня'), ('общего назначения', 'общего назначения'), ('гибридная', 'гибридная'), ('для резервного копирования', 'для резервного копирования'), ('высокопроизводительного класса', 'высокопроизводительного класса'), ('система NAS', 'система NAS'), ('для расширения VMware', 'для расширения VMware'), ('программно-определяемая', 'программно-определяемая'), ('для видеоконтента', 'для видеоконтента')))], max_length=64, null=True, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='query',
            name='product_type',
            field=models.CharField(choices=[('Сервер', (('форм-фактор Rack', 'форм-фактор Rack'), ('форм-фактор Tower', 'форм-фактор Tower'), ('блейд-сервер', 'блейд-сервер'))), ('СХД', (('начального уровня', 'начального уровня'), ('общего назначения', 'общего назначения'), ('гибридная', 'гибридная'), ('для резервного копирования', 'для резервного копирования'), ('высокопроизводительного класса', 'высокопроизводительного класса'), ('система NAS', 'система NAS'), ('для расширения VMware', 'для расширения VMware'), ('программно-определяемая', 'программно-определяемая'), ('для видеоконтента', 'для видеоконтента')))], max_length=64, null=True, verbose_name='Тип'),
        ),
    ]
