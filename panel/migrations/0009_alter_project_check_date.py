# Generated by Django 4.2.3 on 2023-07-20 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0008_alter_project_registered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='check_date',
            field=models.DateField(default='', max_length=512),
        ),
    ]