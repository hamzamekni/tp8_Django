# Generated by Django 5.1.3 on 2024-11-28 09:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livres', '0004_emprunt_return_date_alter_emprunt_date_emprunt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='emprunt',
            name='emprunt_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='emprunt',
            name='date_emprunt',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='emprunt',
            name='nom_emprunteur',
            field=models.CharField(max_length=100),
        ),
    ]
