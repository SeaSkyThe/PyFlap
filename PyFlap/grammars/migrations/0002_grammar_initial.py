# Generated by Django 3.2.14 on 2022-08-06 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grammars', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='grammar',
            name='initial',
            field=models.CharField(default='S', max_length=1),
        ),
    ]
