# Generated by Django 4.2.14 on 2024-08-21 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0006_requestaddproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestaddproduct',
            name='status',
            field=models.CharField(choices=[('a', 'تایید شده'), ('w', 'در انتظار تایید'), ('n', 'عدم تایید')], default='w', max_length=1),
        ),
    ]
