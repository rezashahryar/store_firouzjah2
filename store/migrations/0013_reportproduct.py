# Generated by Django 4.2.14 on 2024-07-30 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_sameproduct'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='store.baseproduct')),
            ],
        ),
    ]
