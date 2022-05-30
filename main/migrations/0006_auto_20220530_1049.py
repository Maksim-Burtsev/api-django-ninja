# Generated by Django 3.2 on 2022-05-30 07:49

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20220526_2321'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchase',
            options={'ordering': ['-bought_at', '-cost']},
        ),
        migrations.AlterField(
            model_name='monthlycost',
            name='spent',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='bought_at',
            field=models.DateField(validators=[main.models.validate_bought_at]),
        ),
    ]
