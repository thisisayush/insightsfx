# Generated by Django 2.1.4 on 2018-12-15 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PollutionData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=255)),
                ('source_type', models.CharField(choices=[('government', 'Government'), ('private', 'Private')], max_length=15)),
                ('pm25', models.FloatField()),
                ('pm10', models.FloatField()),
                ('calculated_aqi_pm25', models.FloatField(null=True)),
                ('calculate_aqi_pm10', models.FloatField(null=True)),
                ('source_time', models.DateTimeField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='pollutiondata',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pollutionmodels.Station'),
        ),
    ]
