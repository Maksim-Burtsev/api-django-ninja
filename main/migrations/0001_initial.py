# Generated by Django 3.2 on 2022-05-26 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyCosts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_number', models.IntegerField()),
                ('year', models.IntegerField()),
                ('spent', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('cost', models.IntegerField()),
                ('bought_at', models.DateField()),
                ('month_number', models.IntegerField()),
            ],
        ),
    ]