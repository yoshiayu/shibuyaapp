# Generated by Django 4.2.16 on 2024-10-12 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0005_point_date_added_point_is_used_alter_point_event_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="point",
            name="event_title",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
