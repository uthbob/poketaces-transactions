# Generated by Django 2.2.11 on 2020-03-28 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AncestryTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=6, default=0.0, max_digits=15)),
                ('transaction_type', models.CharField(default='default_type', max_length=20)),
                ('ancestry_transactions', models.CharField(default='/', max_length=100)),
            ],
            options={
                'db_table': 'transaction_ancestrytransaction',
            },
        ),
    ]
