# Generated by Django 4.0.6 on 2022-09-05 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_alter_useraccount_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='allowed',
            field=models.BooleanField(default=False),
        ),
    ]
