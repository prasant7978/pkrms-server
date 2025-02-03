# Generated by Django 5.0.7 on 2025-01-29 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProvinceCode', models.CharField(max_length=10, unique=True)),
                ('ProvinceName', models.CharField(max_length=50)),
                ('DefaultProvince', models.CharField()),
                ('Stable', models.IntegerField()),
            ],
            options={
                'db_table': 'Province',
            },
        ),
    ]
