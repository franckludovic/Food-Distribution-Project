# Generated by Django 5.1.7 on 2025-04-09 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodDistribution', '0014_remove_foodstock_expiry_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='id',
        ),
        migrations.RemoveField(
            model_name='foodstock',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='food',
            name='food_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
