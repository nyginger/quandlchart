# Generated by Django 2.0.4 on 2018-04-23 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quandl_chart', '0006_items_table_ccode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items_table',
            name='category',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
