# Generated by Django 5.1.1 on 2024-10-02 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_customer_reward_points_product_point_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='reward_points',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
