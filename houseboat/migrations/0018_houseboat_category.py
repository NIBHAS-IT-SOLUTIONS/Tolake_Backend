# Generated by Django 5.0 on 2025-06-20 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houseboat', '0017_rename_complementary_service_houseboat_complementary_services'),
    ]

    operations = [
        migrations.AddField(
            model_name='houseboat',
            name='category',
            field=models.CharField(choices=[('luxury', 'Luxury'), ('deluxe', 'Deluxe'), ('premium', 'Premium'), ('standard', 'Standard'), ('budget', 'Budget')], default='standard', max_length=20),
        ),
    ]
