# Generated by Django 4.2.3 on 2023-07-11 22:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0003_alter_project_employer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='sms',
        ),
    ]
