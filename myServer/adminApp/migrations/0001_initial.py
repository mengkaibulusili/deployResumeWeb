# Generated by Django 3.1.1 on 2020-10-16 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminInfo',
            fields=[
                ('admin_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('admin_uuid', models.CharField(blank=True, default='', max_length=254)),
                ('admin_tele', models.CharField(max_length=254, unique=True)),
                ('admin_pwd', models.CharField(blank=True, default='', max_length=254)),
            ],
        ),
    ]
