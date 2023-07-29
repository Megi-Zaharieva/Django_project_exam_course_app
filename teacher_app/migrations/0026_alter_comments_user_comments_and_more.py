# Generated by Django 4.2.3 on 2023-07-24 18:36

from django.db import migrations, models
import teacher_app.validators


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_app', '0025_remove_userprofileinfo_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='user_comments',
            field=models.TextField(max_length=250, validators=[teacher_app.validators.user_comments_validator]),
        ),
        migrations.AlterField(
            model_name='createcourse',
            name='description',
            field=models.TextField(max_length=800, validators=[teacher_app.validators.description_validator]),
        ),
        migrations.AlterField(
            model_name='review',
            name='review_text',
            field=models.TextField(max_length=300, validators=[teacher_app.validators.review_text_validator]),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='description',
            field=models.TextField(max_length=800, validators=[teacher_app.validators.description_validator]),
        ),
    ]