# Generated by Django 4.2.3 on 2023-07-19 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_app', '0008_rename_addcourse_createcourse'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofileinfo',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
