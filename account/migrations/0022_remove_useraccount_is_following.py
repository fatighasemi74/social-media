# Generated by Django 4.0.6 on 2022-09-13 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0021_useraccount_is_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccount',
            name='is_following',
        ),
    ]
