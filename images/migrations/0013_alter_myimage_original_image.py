# Generated by Django 4.1.7 on 2023-03-09 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0012_alter_myimage_original_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myimage',
            name='original_image',
            field=models.ImageField(upload_to=''),
        ),
    ]
