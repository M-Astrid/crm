# Generated by Django 2.0.2 on 2018-12-19 10:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('survey', '0016_auto_20181213_1259'),
    ]

    operations = [
        migrations.RenameField(
            model_name='query',
            old_name='client_id',
            new_name='client',
        ),
        migrations.RemoveField(
            model_name='item',
            name='ST1',
        ),
        migrations.RemoveField(
            model_name='item',
            name='eac',
        ),
        migrations.RemoveField(
            model_name='item',
            name='imp',
        ),
        migrations.RemoveField(
            model_name='item',
            name='torp',
        ),
        migrations.AddField(
            model_name='item',
            name='certificate',
            field=models.CharField(choices=[('none', 'нет'), ('torp', 'ТОРП'), ('st1', 'СТ1'), ('eac', 'EAC')], default='?', max_length=32, verbose_name='Сертификация'),
        ),
        migrations.AddField(
            model_name='item',
            name='form_factor',
            field=models.CharField(choices=[('Форм-фактор Rack', 'Форм-фактор Rack'), ('Форм-фактор Tower', 'Форм-фактор Tower'), ('Блейд-сервер', 'Блейд-сервер')], max_length=64, null=True, verbose_name='Форм-фактор сервера'),
        ),
        migrations.AddField(
            model_name='item',
            name='product_type',
            field=models.CharField(choices=[('server', 'Сервера'), ('shd', 'СХД')], max_length=64, null=True, verbose_name='Направление'),
        ),
        migrations.AddField(
            model_name='item',
            name='type',
            field=models.CharField(choices=[('СХД начального уровня', 'СХД начального уровня'), ('СХД общего назначения', 'СХД общего назначения'), ('Гибридная СХД', 'Гибридная СХД'), ('СХД для резервного копирования', 'СХД для резервного копирования'), ('СХД высокопроизводительного класса', 'СХД высокопроизводительного класса'), ('СХД система NAS', 'СХД система NAS'), ('СХД для расширения VMware', 'СХД для расширения VMware'), ('Программно-определяемая СХД', 'Программно-определяемая СХД'), ('СХД для видеоконтента', 'СХД для видеоконтента')], max_length=64, null=True, verbose_name='Тип СХД'),
        ),
        migrations.AddField(
            model_name='item',
            name='upgrade',
            field=models.CharField(choices=[('Да', 'Да'), ('Нет', 'Нет')], max_length=6, null=True, verbose_name='Апгрейд'),
        ),
        migrations.AddField(
            model_name='query',
            name='form_factor',
            field=models.CharField(choices=[('Форм-фактор Rack', 'Форм-фактор Rack'), ('Форм-фактор Tower', 'Форм-фактор Tower'), ('Блейд-сервер', 'Блейд-сервер')], max_length=64, null=True, verbose_name='Форм-фактор сервера'),
        ),
        migrations.AddField(
            model_name='query',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='query',
            name='survey_comments',
            field=models.TextField(blank=True, verbose_name='Примечания к опросу'),
        ),
        migrations.AddField(
            model_name='query',
            name='type',
            field=models.CharField(choices=[('СХД начального уровня', 'СХД начального уровня'), ('СХД общего назначения', 'СХД общего назначения'), ('Гибридная СХД', 'Гибридная СХД'), ('СХД для резервного копирования', 'СХД для резервного копирования'), ('СХД высокопроизводительного класса', 'СХД высокопроизводительного класса'), ('СХД система NAS', 'СХД система NAS'), ('СХД для расширения VMware', 'СХД для расширения VMware'), ('Программно-определяемая СХД', 'Программно-определяемая СХД'), ('СХД для видеоконтента', 'СХД для видеоконтента')], max_length=64, null=True, verbose_name='Тип СХД'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price_bracket',
            field=models.CharField(choices=[('(1)Premium', '(1)Premium'), ('(2)Средняя цен. кат.', '(2)Средняя цен. кат.'), ('(3)No name', '(3)No name')], max_length=64, verbose_name='Бюджет'),
        ),
        migrations.AlterField(
            model_name='query',
            name='certificate',
            field=models.CharField(choices=[('none', 'нет'), ('torp', 'ТОРП'), ('st1', 'СТ1'), ('eac', 'EAC')], default='EAC', max_length=32, verbose_name='Сертификация'),
        ),
        migrations.AlterField(
            model_name='query',
            name='product_type',
            field=models.CharField(choices=[('server', 'Сервера'), ('shd', 'СХД')], max_length=64, null=True, verbose_name='Направление'),
        ),
        migrations.AlterField(
            model_name='query',
            name='status',
            field=models.CharField(choices=[('Запрос', 'Запрос'), ('Лид', 'Лид'), ('Заявка', 'Заявка'), ('Отказ', 'Отказ'), ('Успешно реализован', 'Успешно реализован')], max_length=64, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='query',
            name='upgrade',
            field=models.CharField(choices=[('Да', 'Да'), ('Нет', 'Нет')], max_length=6, null=True, verbose_name='Апгрейд'),
        ),
    ]