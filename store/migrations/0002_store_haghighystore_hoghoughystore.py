# Generated by Django 4.2.14 on 2024-07-29 12:11

from django.db import migrations, models
import django.db.models.deletion
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('mobile_number', models.CharField(max_length=11)),
                ('phone_number', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254)),
                ('code', models.CharField(default=store.models.random_code_store, max_length=6, unique=True)),
                ('shomare_shaba', models.CharField(max_length=26)),
                ('mahalle', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=555)),
                ('post_code', models.CharField(max_length=10)),
                ('parvane_kasb', models.FileField(upload_to='parvane_kasb__/%Y/%m/%d/')),
                ('tasvire_personely', models.ImageField(upload_to='tasvire_personely__/%Y/%m/%d/')),
                ('kart_melli', models.ImageField(upload_to='kart_melli__/%Y/%m/%d/')),
                ('shenasname', models.ImageField(upload_to='tasvire_shenasname__/%Y/%m/%d/')),
                ('logo', models.ImageField(upload_to='logo__/%Y/%m/%d/')),
                ('roozname_rasmi_alamat', models.FileField(upload_to='roozname_rasmi_alamat__/%Y/%m/%d/')),
                ('gharardad', models.FileField(upload_to='gharardad__/%Y/%m/%d/')),
                ('store_type', models.CharField(choices=[('ha', 'حقیقی'), ('ho', 'حقوقی')], max_length=2)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='store.city')),
                ('mantaghe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='store.neighbourhood')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='store.province')),
            ],
        ),
        migrations.CreateModel(
            name='HaghighyStore',
            fields=[
                ('store_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.store')),
                ('full_name', models.CharField(max_length=255)),
                ('birth_date', models.DateField()),
                ('name_father', models.CharField(max_length=255)),
                ('code_melli', models.CharField(max_length=10, unique=True)),
                ('shomare_shenasname', models.CharField(max_length=255)),
            ],
            bases=('store.store',),
        ),
        migrations.CreateModel(
            name='HoghoughyStore',
            fields=[
                ('store_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.store')),
                ('ceo_name', models.CharField(max_length=255)),
                ('company_name', models.CharField(max_length=255)),
                ('date_of_registration', models.DateField()),
                ('num_of_registration', models.CharField(max_length=255)),
                ('economic_code', models.CharField(max_length=255)),
            ],
            bases=('store.store',),
        ),
    ]
