# Generated by Django 3.1.3 on 2020-12-04 17:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geneticon', '0003_auto_20201204_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='population',
            name='create_date',
            field=models.DateField(default=datetime.datetime(2020, 12, 4, 17, 19, 54, 747166)),
        ),
    ]
