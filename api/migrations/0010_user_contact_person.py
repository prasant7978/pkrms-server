# Generated by Django 5.0.3 on 2025-02-07 07:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0009_alter_link_linkid"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="contact_person",
            field=models.CharField(blank=True, null=True),
        ),
    ]
