# Generated by Django 2.1.4 on 2018-12-15 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pollutionmodels', '0002_auto_20181215_2249'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pollutiondata',
            unique_together={('source', 'station', 'source_time')},
        ),
    ]
