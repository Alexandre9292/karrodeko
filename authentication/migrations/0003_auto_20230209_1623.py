# Generated by Django 4.1.5 on 2023-02-09 12:23

from django.db import migrations

def create_groups(apps, schema_migration):
    User = apps.get_model('authentication', 'User')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    view_user = Permission.objects.get(codename='view_user')
    
    administration = Group(name='administrator')
    administration.save()
    administration.permissions.add(view_user)

    autre = Group(name='autre')
    autre.save()
    autre.permissions.add(view_user)
    
    for user in User.objects.all():
        if user.role == 'ADMIN':
            administration.user_set.add(user)
        if user.role == 'AUTRE':
            autre.user_set.add(user)

class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.RunPython(create_groups)
    ]
