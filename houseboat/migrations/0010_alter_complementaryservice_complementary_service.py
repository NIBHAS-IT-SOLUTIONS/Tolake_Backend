# Generated by Django 5.0 on 2025-06-20 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houseboat', '0009_alter_complementaryservice_complementary_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complementaryservice',
            name='complementary_service',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
