# Generated by Django 4.0.5 on 2022-06-29 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrowthStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('min_humidity', models.FloatField()),
                ('max_humidity', models.FloatField()),
                ('min_temperature', models.FloatField()),
                ('max_temperature', models.FloatField()),
            ],
        ),
        migrations.AlterField(
            model_name='sensordata',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='GrowthStageHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('growth_stage', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='monitoring.growthstage')),
            ],
        ),
    ]
