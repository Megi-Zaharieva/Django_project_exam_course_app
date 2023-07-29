# Generated by Django 4.2.3 on 2023-07-18 10:51

from django.db import migrations, models
import teacher_app.validators


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_app', '0002_userprofileinfo_admin_field_userprofileinfo_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofileinfo',
            name='admin_field',
        ),
        migrations.AddField(
            model_name='userprofileinfo',
            name='admin_approve',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='file',
            field=models.FileField(blank=True, upload_to='user_files', validators=[teacher_app.validators.FileExtensionValidator()]),
        ),
    ]
