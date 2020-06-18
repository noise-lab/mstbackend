# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('name', models.CharField(max_length=20)),
                ('package', models.CharField(max_length=50, serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'application',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ApplicationUse',
            fields=[
                ('application_useid', models.AutoField(serialize=False, primary_key=True)),
                ('total_sent', models.BigIntegerField()),
                ('total_recv', models.BigIntegerField()),
                ('isrunning', models.BooleanField()),
                ('total_diff', models.BigIntegerField()),
                ('isforeground', models.BooleanField()),
            ],
            options={
                'db_table': 'application_use',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Battery',
            fields=[
                ('measurementid', models.IntegerField(serialize=False, primary_key=True)),
                ('technology', models.CharField(max_length=20)),
                ('ispresent', models.IntegerField()),
                ('plugged', models.IntegerField()),
                ('scale', models.IntegerField()),
                ('health', models.IntegerField()),
                ('voltage', models.IntegerField()),
                ('level', models.IntegerField()),
                ('temperature', models.IntegerField()),
                ('status', models.IntegerField()),
            ],
            options={
                'db_table': 'battery',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('deviceid', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('phonetype', models.CharField(max_length=20)),
                ('phonenumber', models.CharField(max_length=40)),
                ('softwareversion', models.CharField(max_length=20)),
                ('phonemodel', models.CharField(max_length=20)),
                ('androidversion', models.CharField(max_length=20)),
                ('phonebrand', models.CharField(max_length=20)),
                ('devicedesign', models.CharField(max_length=20)),
                ('manufacturer', models.CharField(max_length=20)),
                ('productname', models.CharField(max_length=20)),
                ('radioversion', models.CharField(max_length=20)),
                ('boardname', models.CharField(max_length=20)),
                ('datacap', models.IntegerField()),
                ('billingcycle', models.IntegerField()),
                ('networkcountry', models.CharField(max_length=2)),
                ('networkname', models.CharField(max_length=25)),
                ('emailaddress', models.CharField(max_length=40)),
                ('applicationversion', models.IntegerField()),
                ('dataplantype', models.IntegerField()),
                ('dataplanpromo', models.IntegerField()),
                ('dataplanpromoname', models.CharField(max_length=25)),
                ('dataplanlastupd', models.DateTimeField()),
            ],
            options={
                'db_table': 'device',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DNSAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('rtype', models.CharField(max_length=10)),
                ('rdata', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'dns_answers',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DNSMeasurement',
            fields=[
                ('dns_id', models.AutoField(serialize=False, primary_key=True)),
                ('qtype', models.CharField(max_length=10)),
                ('qclass', models.CharField(max_length=10)),
                ('qname', models.CharField(max_length=100)),
                ('server', models.CharField(max_length=25)),
                ('completed', models.BooleanField()),
            ],
            options={
                'db_table': 'dns_measurements',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DNSResult',
            fields=[
                ('result_id', models.AutoField(serialize=False, primary_key=True)),
                ('qtype', models.CharField(max_length=10)),
                ('qclass', models.CharField(max_length=10)),
                ('qname', models.CharField(max_length=100)),
                ('server', models.CharField(max_length=25)),
                ('resp_time', models.IntegerField()),
                ('is_tc_set', models.BooleanField()),
                ('is_valid', models.BooleanField()),
                ('query_id', models.IntegerField()),
                ('resp_id', models.IntegerField()),
                ('rcode', models.CharField(max_length=25)),
                ('payload', models.TextField()),
            ],
            options={
                'db_table': 'dns_results',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Hop',
            fields=[
                ('hopid', models.AutoField(serialize=False, primary_key=True)),
                ('address', models.CharField(max_length=50)),
                ('hostname', models.CharField(max_length=100)),
                ('hopnumber', models.IntegerField()),
                ('rtt', models.FloatField()),
            ],
            options={
                'db_table': 'hop',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Lastmile',
            fields=[
                ('avg', models.FloatField()),
                ('stdev', models.FloatField()),
                ('min', models.FloatField()),
                ('max', models.FloatField()),
                ('scrip', models.CharField(max_length=50)),
                ('dstip', models.CharField(max_length=50)),
                ('firstip', models.CharField(max_length=50)),
                ('time', models.DateTimeField()),
                ('hopcount', models.IntegerField()),
                ('lastmileid', models.AutoField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'lastmile',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('linkid', models.AutoField(serialize=False, primary_key=True)),
                ('count', models.IntegerField()),
                ('message_size', models.BigIntegerField()),
                ('duration', models.IntegerField()),
                ('speed', models.FloatField()),
                ('port', models.IntegerField()),
                ('ip_address', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'link',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('measurementid', models.AutoField(serialize=False, primary_key=True)),
                ('time', models.DateTimeField()),
                ('localtime', models.DateTimeField()),
                ('ismanual', models.BooleanField()),
                ('applicationversion', models.IntegerField()),
            ],
            options={
                'db_table': 'measurement',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MobiMeasurement',
            fields=[
                ('measurement_id', models.AutoField(serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=30)),
                ('time', models.DateTimeField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('app_version', models.IntegerField()),
                ('mobi_version', models.CharField(max_length=15)),
                ('bat_level', models.IntegerField()),
                ('cc', models.CharField(max_length=2)),
            ],
            options={
                'db_table': 'mobi_measurement',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('measurementid', models.IntegerField(serialize=False, primary_key=True)),
                ('networktype', models.CharField(max_length=10)),
                ('connectiontype', models.CharField(max_length=10)),
                ('wifistate', models.CharField(max_length=20)),
                ('datastate', models.CharField(max_length=30)),
                ('dataactivity', models.CharField(max_length=30)),
                ('signalstrength', models.CharField(max_length=20)),
                ('cellid', models.CharField(max_length=20)),
                ('celltype', models.CharField(max_length=10)),
                ('celllac', models.CharField(max_length=20)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('systemid', models.IntegerField()),
                ('networkid', models.IntegerField()),
            ],
            options={
                'db_table': 'network',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ping',
            fields=[
                ('avg', models.FloatField()),
                ('stdev', models.FloatField()),
                ('min', models.FloatField()),
                ('max', models.FloatField()),
                ('scrip', models.CharField(max_length=50)),
                ('dstip', models.CharField(max_length=50)),
                ('time', models.DateTimeField()),
                ('pingid', models.AutoField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'ping',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sim',
            fields=[
                ('serialnumber', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('state', models.CharField(max_length=20)),
                ('operatorcode', models.CharField(max_length=8)),
                ('operatorname', models.CharField(max_length=20)),
                ('networkcountry', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 'sim',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('measurementid', models.IntegerField(serialize=False, primary_key=True)),
                ('cellid', models.CharField(max_length=20)),
                ('deviceid', models.CharField(max_length=40)),
                ('networktype', models.CharField(max_length=20)),
                ('timeslice', models.IntegerField()),
                ('weekday', models.IntegerField()),
            ],
            options={
                'db_table': 'state',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Throughput',
            fields=[
                ('measurementid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'throughput',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Traceroute',
            fields=[
                ('tracerouteid', models.AutoField(serialize=False, primary_key=True)),
                ('hostname', models.CharField(max_length=100)),
                ('srcip', models.CharField(max_length=50)),
                ('dstip', models.CharField(max_length=50)),
                ('tracetype', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 'traceroute',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Usage',
            fields=[
                ('measurementid', models.IntegerField(serialize=False, primary_key=True)),
                ('total_sent', models.BigIntegerField()),
                ('total_recv', models.BigIntegerField()),
                ('total_till_now', models.BigIntegerField()),
                ('mobile_sent', models.BigIntegerField()),
                ('mobile_recv', models.BigIntegerField()),
                ('mobile_till_now', models.BigIntegerField()),
            ],
            options={
                'db_table': 'usage',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WarmupExperiment',
            fields=[
                ('lowest', models.FloatField(null=True, blank=True)),
                ('highest', models.FloatField(null=True, blank=True)),
                ('version', models.CharField(max_length=10, blank=True)),
                ('dstip', models.CharField(max_length=50, blank=True)),
                ('total_count', models.IntegerField(null=True, blank=True)),
                ('gap', models.FloatField(null=True, blank=True)),
                ('measurementid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'warmup_experiment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WarmupPing',
            fields=[
                ('value', models.FloatField(null=True, blank=True)),
                ('sequence_count', models.IntegerField(null=True, blank=True)),
                ('period', models.FloatField(null=True, blank=True)),
                ('warmupid', models.AutoField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'warmup_ping',
                'managed': False,
            },
        ),
    ]
