# Generated by Django 2.2.7 on 2020-07-18 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_type',
            field=models.CharField(choices=[('H', 'HOME'), ('W', 'WORK')], max_length=2),
        ),
    ]
