# Generated by Django 2.0.2 on 2018-02-25 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ttt', '0003_auto_20180224_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
