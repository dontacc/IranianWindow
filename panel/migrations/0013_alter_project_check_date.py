# Generated by Django 4.2.3 on 2023-07-21 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0012_rename_registered_date_project_first_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='check_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
