# Generated by Django 4.2.3 on 2023-07-21 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0014_alter_project_check_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='check_date',
            field=models.DateField(default=None),
        ),
    ]
