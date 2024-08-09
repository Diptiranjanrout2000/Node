# Generated by Django 5.0.8 on 2024-08-09 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_backend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='id',
        ),
        migrations.RemoveField(
            model_name='nodemodel',
            name='id',
        ),
        migrations.AlterField(
            model_name='node',
            name='nodeid',
            field=models.CharField(max_length=150, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='nodemodel',
            name='gateway_id',
            field=models.CharField(blank=True, max_length=200, primary_key=True, serialize=False),
        ),
    ]
