# Generated by Django 5.2 on 2025-04-28 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['timestamp']},
        ),
    ]
