# Generated by Django 4.1.5 on 2023-04-02 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0022_alter_clients_email2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='email2',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
    ]