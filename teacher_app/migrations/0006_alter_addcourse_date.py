# Generated by Django 4.2.3 on 2023-07-18 17:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_app', '0005_addcourse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addcourse',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
