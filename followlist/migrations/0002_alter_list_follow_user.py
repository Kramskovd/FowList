# Generated by Django 4.0.3 on 2022-09-25 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('followlist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='follow_user',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
