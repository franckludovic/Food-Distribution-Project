# Generated by Django 5.2 on 2025-04-09 10:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodDistribution', '0016_alter_foodstock_food_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='created_at',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='food',
            name='expire_date',
            field=models.DateField(blank=True),
        ),
    ]
