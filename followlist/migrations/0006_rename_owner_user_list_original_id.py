# Generated by Django 4.0.3 on 2022-09-27 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('followlist', '0005_remove_list_original_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='list',
            old_name='owner_user',
            new_name='original_id',
        ),
    ]
