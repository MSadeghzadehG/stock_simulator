# Generated by Django 2.1.5 on 2019-02-10 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicator', '0014_auto_20190210_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicator',
            name='name',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]
