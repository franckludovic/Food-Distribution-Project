# Generated by Django 5.1.6 on 2025-03-12 09:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodDistribution', '0012_alter_profile_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteerprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodDistribution.profile'),
        ),
    ]
