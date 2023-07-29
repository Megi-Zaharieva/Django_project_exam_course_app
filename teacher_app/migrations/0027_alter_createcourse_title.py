# Generated by Django 4.2.3 on 2023-07-24 18:48

from django.db import migrations, models
import teacher_app.validators


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_app', '0026_alter_comments_user_comments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createcourse',
            name='title',
            field=models.CharField(max_length=255, validators=[teacher_app.validators.title_validator]),
        ),
    ]
