# Generated by Django 4.0.3 on 2022-09-27 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('followlist', '0003_rename_follow_user_list_owner_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='original_id',
            field=models.IntegerField(default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='list',
            name='owner_user',
            field=models.IntegerField(default=-1, null=True),
        ),
    ]
