# Generated by Django 4.1.5 on 2023-02-01 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='Description',
            new_name='description',
        ),
        migrations.AddField(
            model_name='customer',
            name='status',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]