# Generated by Django 4.1.5 on 2023-02-07 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_post_summary_image_alter_post_text_image_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='summary_image',
            field=models.ImageField(default=None, upload_to='image/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text_image_1',
            field=models.ImageField(default=None, upload_to='image/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text_image_2',
            field=models.ImageField(default=None, upload_to='image/'),
        ),
    ]