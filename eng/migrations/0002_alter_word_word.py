# Generated by Django 3.2 on 2022-06-02 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eng', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='word',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]