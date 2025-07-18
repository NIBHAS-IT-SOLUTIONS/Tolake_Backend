# Generated by Django 5.0 on 2025-07-02 05:29

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('houseboat', '0024_alter_booking_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='houseboat',
            name='complementary_services',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='complementary_services',
        ),
        migrations.AddField(
            model_name='houseboat',
            name='complementary_services',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('wifi', 'WiFi'), ('meals', 'Meals Included'), ('music', 'Music System'), ('guide', 'Tour Guide'), ('ac', 'Air Conditioning')], max_length=100),
        ),
        migrations.DeleteModel(
            name='ComplementaryService',
        ),
        migrations.AddField(
            model_name='booking',
            name='complementary_services',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('wifi', 'WiFi'), ('meals', 'Meals Included'), ('music', 'Music System'), ('guide', 'Tour Guide'), ('ac', 'Air Conditioning')], max_length=100),
        ),
    ]
