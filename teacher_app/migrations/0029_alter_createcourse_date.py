# Generated by Django 4.2.3 on 2023-07-27 06:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_app', '0028_alter_createcourse_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createcourse',
            name='date',
            field=models.DateField(default=datetime.date(2023, 7, 27)),
        ),
    ]