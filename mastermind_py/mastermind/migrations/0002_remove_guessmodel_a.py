# Generated by Django 2.2.2 on 2021-12-29 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mastermind', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guessmodel',
            name='a',
        ),
    ]