# Generated by Django 4.0.4 on 2022-05-03 00:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Plants',
            fields=[
                ('plantid', models.AutoField(db_column='plantID', primary_key=True, serialize=False)),
                ('url', models.CharField(db_column='URL', max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('botanynm', models.CharField(db_column='botanyNm', max_length=255)),
                ('info', models.TextField()),
                ('watercycle', models.CharField(db_column='waterCycle', max_length=255)),
                ('waterinfo', models.CharField(db_column='waterInfo', max_length=255)),
                ('waterexp', models.CharField(db_column='waterExp', max_length=255)),
                ('waterexpinfo', models.TextField(db_column='waterExpInfo')),
                ('light', models.CharField(max_length=255)),
                ('lightinfo', models.CharField(db_column='lightInfo', max_length=255)),
                ('lightexp', models.CharField(db_column='lightExp', max_length=255)),
                ('lightexpinfo', models.TextField(db_column='lightExpInfo')),
                ('humidity', models.CharField(max_length=255)),
                ('humidinfo', models.CharField(db_column='humidInfo', max_length=255)),
                ('humidexp', models.CharField(db_column='humidExp', max_length=255)),
                ('humidexpinfo', models.TextField(db_column='humidExpInfo')),
                ('tempexp', models.CharField(db_column='tempExp', max_length=255)),
                ('tempexpinfo', models.TextField(db_column='tempExpInfo')),
            ],
            options={
                'db_table': 'plants',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('weatherid', models.AutoField(db_column='weatherID', primary_key=True, serialize=False)),
                ('areano', models.BigIntegerField(db_column='areaNo')),
                ('si', models.CharField(max_length=30)),
                ('time', models.IntegerField()),
                ('condi', models.CharField(max_length=30)),
                ('isday', models.IntegerField(blank=True, db_column='isDay', null=True)),
                ('temp', models.IntegerField(blank=True, null=True)),
                ('humidity', models.IntegerField(blank=True, null=True)),
                ('rainratio', models.IntegerField(blank=True, db_column='rainRatio', null=True)),
                ('snowratio', models.IntegerField(blank=True, db_column='snowRatio', null=True)),
                ('uv', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'weather',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Plantmanage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nickname', models.CharField(max_length=50)),
                ('meetdate', models.DateField()),
                ('waterdate', models.DateField()),
                ('cycle', models.IntegerField()),
                ('nextdate', models.DateField()),
                ('plant', models.ForeignKey(db_column='plant', on_delete=django.db.models.deletion.CASCADE, to='finalproject.plants')),
                ('username', models.ForeignKey(db_column='username', on_delete=django.db.models.deletion.CASCADE, to='finalproject.authuser')),
            ],
            options={
                'db_table': 'plantmanage',
            },
        ),
    ]
