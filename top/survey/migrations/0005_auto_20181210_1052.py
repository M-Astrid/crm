# Generated by Django 2.0.2 on 2018-12-10 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_auto_20181209_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='form',
            field=models.CharField(choices=[('ООО', 'ООО'), ('ОАО', 'ОАО'), ('ПАО', 'ПАО'), ('ЗАО', 'ЗАО'), ('АО', 'АО')], max_length=16, verbose_name='Форма'),
        ),
        migrations.AlterField(
            model_name='client',
            name='governmental',
            field=models.CharField(choices=[('gov', 'Государственная'), ('non_gov', 'Негосударственная')], max_length=64, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='client',
            name='sanctions',
            field=models.CharField(choices=[('Да', 'Да'), ('Нет', 'Нет')], default=False, max_length=6, verbose_name='Санкции'),
        ),
        migrations.AlterField(
            model_name='client',
            name='subtype',
            field=models.CharField(blank=True, choices=[('force', 'Силовики'), ('gov_comp', 'Гос. компания'), ('gov_inst', 'Гос. учреждение'), ('gen_podr', 'Ген. подрядчик'), ('pr_comp', 'Частная компания'), ('SMB', 'SMB')], max_length=64, verbose_name='Подтип'),
        ),
        migrations.AlterField(
            model_name='query',
            name='lead_items',
            field=models.ManyToManyField(related_name='l_items', to='survey.Item', verbose_name='Лид'),
        ),
        migrations.AlterField(
            model_name='query',
            name='order_items',
            field=models.ManyToManyField(blank=True, related_name='o_items', to='survey.Item', verbose_name='Заявка'),
        ),
    ]