# Generated by Django 5.1.1 on 2024-12-07 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_alter_transactions_transations_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactions',
            old_name='transations_type',
            new_name='transactions_type',
        ),
    ]