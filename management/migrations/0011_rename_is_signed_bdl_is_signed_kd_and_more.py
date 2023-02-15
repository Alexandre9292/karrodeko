# Generated by Django 4.1.5 on 2023-02-15 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0010_bdl_is_signed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bdl',
            old_name='is_signed',
            new_name='is_signed_KD',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='signature_path',
            new_name='signature_KD_path',
        ),
        migrations.AddField(
            model_name='bdl',
            name='is_signed_client',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customer',
            name='signature_client_path',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='customer',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
    ]
