# Generated by Django 4.1.7 on 2023-03-10 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0014_alter_myimage_original_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myimage',
            name='original_image',
            field=models.ImageField(upload_to='img/<function user_directory_path at 0x0000018ACCE1D120>'),
        ),
        migrations.AlterField(
            model_name='myimage',
            name='thumbnail_200',
            field=models.ImageField(blank=True, null=True, upload_to='img/<function user_directory_path at 0x0000018ACCE1D120>/thumbnails/200/'),
        ),
        migrations.AlterField(
            model_name='myimage',
            name='thumbnail_400',
            field=models.ImageField(blank=True, null=True, upload_to='img/<function user_directory_path at 0x0000018ACCE1D120>/thumbnails/400/'),
        ),
    ]
