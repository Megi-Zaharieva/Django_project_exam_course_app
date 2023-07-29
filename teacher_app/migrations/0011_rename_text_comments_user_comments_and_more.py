# Generated by Django 4.2.3 on 2023-07-22 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_app', '0010_comments'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='text',
            new_name='user_comments',
        ),
        migrations.AlterField(
            model_name='comments',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='teacher_app.createcourse'),
        ),
    ]
