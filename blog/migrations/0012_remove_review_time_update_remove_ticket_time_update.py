# Generated by Django 4.2.1 on 2023-06-04 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0011_ticket_time_update"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="review",
            name="time_update",
        ),
        migrations.RemoveField(
            model_name="ticket",
            name="time_update",
        ),
    ]
