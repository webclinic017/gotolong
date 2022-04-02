# Generated by Django 3.0.1 on 2020-07-10 13:58

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Indices',
            fields=[
                ('comp_name', models.TextField(primary_key=True, serialize=False)),
                ('comp_industry', models.TextField(blank=True, null=True)),
                ('comp_ticker', models.TextField(blank=True, null=True)),
                ('series', models.TextField(blank=True, null=True)),
                ('comp_isin', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'global_isin',
            },
        ),
    ]
