# Generated by Django 4.1.7 on 2023-02-15 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(max_length=10)),
                ('country_code_2', models.CharField(blank=True, max_length=2, null=True)),
                ('updated', models.DateTimeField()),
                ('new_cases', models.IntegerField(default=0)),
                ('cum_cases', models.IntegerField(default=0)),
                ('new_deaths', models.IntegerField(default=0)),
                ('cum_deaths', models.IntegerField(default=0)),
            ],
        ),
    ]
