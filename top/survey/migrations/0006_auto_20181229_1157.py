# Generated by Django 2.0.2 on 2018-12-29 04:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_remove_contact_cl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='queries', to='survey.Client'),
        ),
        migrations.AlterField(
            model_name='query',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
