# Generated by Django 4.1.5 on 2023-03-31 07:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0019_clients_email2_customer_email2'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='management.clients'),
        ),
    ]
