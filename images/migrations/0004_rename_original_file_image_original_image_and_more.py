# Generated by Django 4.1.7 on 2023-03-05 14:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('images', '0003_rename_parent_profile_parent_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='original_file',
            new_name='original_image',
        ),
        migrations.RemoveField(
            model_name='image',
            name='thumbnail_200',
        ),
        migrations.RemoveField(
            model_name='image',
            name='thumbnail_400',
        ),
        migrations.AlterField(
            model_name='image',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
