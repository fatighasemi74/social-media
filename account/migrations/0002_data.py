# Generated by Django 4.0.6 on 2022-11-05 11:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='modified time')),
                ('media_type', models.CharField(max_length=30)),
                ('media_file', models.FileField(upload_to='data/content/media', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('jpg', 'jpeg', 'mp4', 'wmv', 'flv', 'png'))])),
                ('content_id', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Data',
                'verbose_name_plural': 'Datas',
            },
        ),
    ]
