# Generated by Django 3.1 on 2020-08-27 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200820_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilee',
            name='phone',
            field=models.PositiveIntegerField(blank=True, max_length=12, null=True),
        ),
    ]
