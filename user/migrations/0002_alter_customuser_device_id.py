# Generated by Django 5.0 on 2023-12-19 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='device_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]