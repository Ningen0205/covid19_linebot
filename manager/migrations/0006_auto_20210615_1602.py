# Generated by Django 3.2.3 on 2021-06-15 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_infection_prefecture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='infection',
            name='prefecture',
        ),
        migrations.AddField(
            model_name='infection',
            name='prefecture_id',
            field=models.IntegerField(null=True),
        ),
    ]
