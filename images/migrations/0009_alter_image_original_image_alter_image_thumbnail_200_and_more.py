# Generated by Django 4.1.7 on 2023-03-09 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0008_alter_image_original_image_alter_image_thumbnail_200_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='original_image',
            field=models.ImageField(upload_to='img/'),
        ),
        migrations.AlterField(
            model_name='image',
            name='thumbnail_200',
            field=models.ImageField(blank=True, null=True, upload_to='img/thumbnails/200x200/'),
        ),
        migrations.AlterField(
            model_name='image',
            name='thumbnail_400',
            field=models.ImageField(blank=True, null=True, upload_to='img/thumbnails/400x400/'),
        ),
    ]
