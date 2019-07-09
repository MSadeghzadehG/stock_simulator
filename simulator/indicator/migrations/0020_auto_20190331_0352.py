# Generated by Django 2.1.7 on 2019-03-31 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('indicator', '0019_auto_20190331_0352'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bought_stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buy_time', models.DateTimeField()),
                ('sell_time', models.DateTimeField(default=None, null=True)),
                ('volume', models.FloatField(default=0)),
                ('purchase_price', models.FloatField(default=0)),
                ('current_price', models.FloatField(default=0)),
                ('profit', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, unique=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(null=True)),
                ('algorithm', models.CharField(max_length=300)),
                ('paid', models.FloatField(default=0)),
                ('bought_stocks_value', models.FloatField(default=0)),
                ('gain', models.FloatField(default=0)),
                ('profit', models.FloatField(default=0)),
                ('last_update', models.DateTimeField(default=None, null=True)),
                ('bought', models.ManyToManyField(related_name='bought', to='indicator.Bought_stock')),
                ('trade_log', models.ManyToManyField(related_name='trade_log', to='indicator.Bought_stock')),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Ticker', models.CharField(max_length=300)),
                ('date', models.CharField(max_length=300)),
                ('first', models.CharField(max_length=300)),
                ('high', models.CharField(max_length=300)),
                ('low', models.CharField(max_length=300)),
                ('close', models.CharField(max_length=300)),
                ('value', models.CharField(max_length=300)),
                ('vol', models.CharField(max_length=300)),
                ('openint', models.CharField(max_length=300)),
                ('per', models.CharField(max_length=300)),
                ('openp', models.CharField(max_length=300)),
                ('last', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('tmc_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('q1', models.CharField(max_length=300)),
                ('namad', models.CharField(max_length=300)),
                ('nam', models.CharField(max_length=300)),
                ('q2', models.CharField(max_length=300)),
                ('avalin', models.CharField(max_length=300)),
                ('payani', models.CharField(max_length=300)),
                ('akharin_moamele', models.CharField(max_length=300)),
                ('tedad_moamelat', models.CharField(max_length=300)),
                ('hajm_moamelat', models.CharField(max_length=300)),
                ('arzesh_moamelat', models.CharField(max_length=300)),
                ('baze_rooz_kam', models.CharField(max_length=300)),
                ('baze_rooz_ziad', models.CharField(max_length=300)),
                ('dirooz', models.CharField(max_length=300)),
                ('eps', models.CharField(max_length=300)),
                ('q3', models.CharField(max_length=300)),
                ('q4', models.CharField(max_length=300)),
                ('q5', models.CharField(max_length=300)),
                ('q6', models.CharField(max_length=300)),
                ('mojaz_ziad', models.CharField(max_length=300)),
                ('mojaz_kam', models.CharField(max_length=300)),
                ('q7', models.CharField(max_length=300)),
                ('q8', models.CharField(max_length=300)),
            ],
        ),
        migrations.AddField(
            model_name='record',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='indicator.Stock'),
        ),
        migrations.AddField(
            model_name='bought_stock',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='indicator.Stock'),
        ),
    ]
