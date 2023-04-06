# Generated by Django 4.2 on 2023-04-04 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='fact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('factorial', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='fact_multi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('multifactorial', models.TextField()),
                ('photo', models.ImageField(upload_to='pics/')),
                ('factorial_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='testdemo.fact')),
            ],
        ),
    ]
