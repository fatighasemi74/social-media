# Generated by Django 4.0.6 on 2022-08-20 09:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='media_file',
            field=models.FileField(blank=True, null=True, upload_to='content/media', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('jpg', 'jpeg', 'mp4', 'wmv', 'flv', 'png'))]),
        ),
    ]
