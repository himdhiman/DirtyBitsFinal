# Generated by Django 3.2.5 on 2021-07-12 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DateTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTime', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('first_Name', models.CharField(max_length=20)),
                ('last_Name', models.CharField(max_length=20)),
                ('joining_Date', models.DateField(auto_now=True, verbose_name='date joined')),
                ('last_login', models.DateField(auto_now=True, verbose_name='last login')),
                ('solved', models.IntegerField()),
                ('partiallySolved', models.IntegerField()),
                ('attemped', models.IntegerField()),
                ('score', models.IntegerField()),
                ('rank', models.IntegerField()),
                ('problemsSolved', models.TextField(blank=True, null=True)),
                ('problemPartiallySolved', models.TextField(blank=True, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('dateTime', models.ManyToManyField(to='api.DateTime')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
