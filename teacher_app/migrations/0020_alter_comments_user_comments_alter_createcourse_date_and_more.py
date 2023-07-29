# Generated by Django 4.2.3 on 2023-07-23 11:10

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_app', '0019_searchmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='user_comments',
            field=models.TextField(max_length=250, validators=[django.core.validators.MinLengthValidator(5)]),
        ),
        migrations.AlterField(
            model_name='createcourse',
            name='date',
            field=models.DateField(default=datetime.date(2023, 7, 23)),
        ),
        migrations.AlterField(
            model_name='createcourse',
            name='description',
            field=models.TextField(max_length=800),
        ),
        migrations.AlterField(
            model_name='createcourse',
            name='title',
            field=models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
        migrations.AlterField(
            model_name='createcourse',
            name='video_url',
            field=models.URLField(default=None),
        ),
        migrations.AlterField(
            model_name='review',
            name='review_text',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='admin_approved',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], null=True),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='description',
            field=models.TextField(max_length=800),
        ),
    ]