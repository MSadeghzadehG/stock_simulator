# Generated by Django 2.1.5 on 2019-02-11 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicator', '0018_auto_20190211_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
