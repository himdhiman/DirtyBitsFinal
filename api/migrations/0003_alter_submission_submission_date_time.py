# Generated by Django 3.2.5 on 2021-07-15 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210715_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='submission_Date_Time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]