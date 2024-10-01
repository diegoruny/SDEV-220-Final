# Generated by Django 5.1.1 on 2024-10-01 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='reward_points',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='point_value',
            field=models.IntegerField(blank=True, default=25, null=True),
        ),
    ]
