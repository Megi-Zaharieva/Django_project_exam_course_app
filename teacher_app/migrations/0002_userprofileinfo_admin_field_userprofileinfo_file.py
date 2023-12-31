# Generated by Django 4.2.3 on 2023-07-18 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofileinfo',
            name='admin_field',
            field=models.CharField(blank=True, choices=[('Teacher', 'Teacher'), ('Student', 'Student')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='userprofileinfo',
            name='file',
            field=models.FileField(blank=True, upload_to='user_files'),
        ),
    ]
