from django.db import models

class Sim(models.Model):
    serialnumber = models.CharField(max_length=40, primary_key=True)
    state = models.CharField(max_length=20)
    operatorcode = models.CharField(max_length=8)
    operatorname = models.CharField(max_length=20)
    networkcountry = models.CharField(max_length=5)

    class Meta:
        db_table = u'sim'
        managed=False

class Device(models.Model):
    deviceid = models.CharField(max_length=40, primary_key=True)
    phonetype = models.CharField(max_length=20)
    phonenumber = models.CharField(max_length=40)
    softwareversion = models.CharField(max_length=20)
    phonemodel = models.CharField(max_length=20)
    androidversion = models.CharField(max_length=20)
    phonebrand = models.CharField(max_length=20)
    devicedesign = models.CharField(max_length=20)
    manufacturer = models.CharField(max_length=20)
    productname = models.CharField(max_length=20)
    radioversion = models.CharField(max_length=20)
    boardname = models.CharField(max_length=20)
    serialnumber = models.ForeignKey(Sim, to_field='serialnumber',
                                     db_column='serialnumber')
    datacap = models.IntegerField()
    billingcycle = models.IntegerField()
    networkcountry = models.CharField(max_length=2)                                                                                                                             
    networkname = models.CharField(max_length=25)                                                                                                                               
    emailaddress = models.CharField(max_length=40)                                                                                                                              
    applicationversion = models.IntegerField()                                                                                                                                  
    dataplantype = models.IntegerField()
    dataplanpromo = models.IntegerField()
    dataplanpromoname = models.CharField(max_length=25)
    dataplanlastupd = models.DateTimeField()
                                                                                                                                                                                
    class Meta:                                                                                                                                                                 
        db_table = u'device'
        managed=False

class Battery(models.Model):
    measurementid = models.IntegerField(primary_key=True)
    technology = models.CharField(max_length=20)
    ispresent = models.IntegerField()
    plugged = models.IntegerField()
    scale = models.IntegerField()
    health = models.IntegerField()
    voltage = models.IntegerField()
    level = models.IntegerField()
    temperature = models.IntegerField()
    status = models.IntegerField()
    class Meta:
        db_table = u'battery'
        managed=False



class Link(models.Model):
    linkid = models.AutoField(primary_key=True)
    count = models.IntegerField()
    message_size = models.BigIntegerField()
    duration = models.IntegerField()
    speed = models.FloatField()
    port = models.IntegerField()
    ip_address = models.CharField(max_length=50)

    class Meta:
        db_table = u'link'
        managed=False


class Measurement(models.Model):                                                                                                                                                
    measurementid = models.AutoField(primary_key=True)                                                                                                                          
    time = models.DateTimeField()                                                                                                                                               
    localtime = models.DateTimeField()                                                                                                                                          
    deviceid = models.ForeignKey(Device, to_field='deviceid',                                                                                                                   
                                 db_column='deviceid')                                                                                                                          
    ismanual = models.BooleanField()                                                                                                                                            
    applicationversion = models.IntegerField()                                                                                                                                  
                                                                                                                                                                                
    class Meta:                                                                                                                                                                 
        db_table = u'measurement'                                                                                                                                               
        managed=False
                                                                                                                                                                                
                                                                                                                                                                                
class MobiMeasurement(models.Model):                                                                                                                                            
    measurement_id = models.AutoField(primary_key=True)                                                                                                                         
    device_id = models.ForeignKey(Device, to_field='deviceid',                                                                                                                  
                                  db_column='deviceid')                                                                                                                         
    type = models.CharField(max_length=30)                                                                                                                                      
    time = models.DateTimeField()                                                                                                                                               
    start_time = models.DateTimeField()                                                                                                                                         
    end_time = models.DateTimeField()                                                                                                                                           
    app_version = models.IntegerField()                                                                                                                                         
    mobi_version = models.CharField(max_length=15)                                                                                                                              
    bat_level = models.IntegerField()                                                                                                                                           
    cc = models.CharField(max_length=2)                                                                                                                                         
                                                                                                                                                                                
    class Meta:                                                                                                                                                                 
        db_table = u'mobi_measurement'
        managed=False


class Throughput(models.Model):
    measurementid = models.IntegerField(primary_key=True)
    uplinkid = models.ForeignKey(Link,related_name='throughput_linkid',db_column='uplinkid')
    downlinkid = models.ForeignKey(Link,related_name='throughput_downlinkid',db_column='downlinkid')
    class Meta:
        db_table = u'throughput'
        managed=False

class Network(models.Model):
    measurementid = models.IntegerField(primary_key=True)
    networktype = models.CharField(max_length=10)
    connectiontype = models.CharField(max_length=10)
    wifistate = models.CharField(max_length=20)
    datastate = models.CharField(max_length=30)
    dataactivity = models.CharField(max_length=30)
    signalstrength = models.CharField(max_length=20)
    cellid = models.CharField(max_length=20)
    celltype = models.CharField(max_length=10)
    celllac = models.CharField(max_length=20)
    longitude = models.FloatField()
    latitude = models.FloatField()
    systemid = models.IntegerField()
    networkid = models.IntegerField()
    class Meta:
        db_table = u'network'
        managed=False

class State(models.Model):
    measurementid = models.IntegerField(primary_key=True)
    cellid = models.CharField(max_length=20)
    deviceid = models.CharField(max_length=40)
    networktype = models.CharField(max_length=20)
    timeslice = models.IntegerField()
    weekday = models.IntegerField()
    class Meta:
        db_table = u'state'
        managed=False

class Ping(models.Model):
    avg = models.FloatField()
    stdev = models.FloatField()
    min = models.FloatField()
    max = models.FloatField()
    scrip = models.CharField(max_length=50)
    dstip = models.CharField(max_length=50)
    time = models.DateTimeField()
    measurementid = models.ForeignKey(Measurement, to_field='measurementid', db_column='measurementid')
    pingid = models.AutoField(primary_key=True)
    class Meta:
        db_table = u'ping'
        managed=False

class Usage(models.Model):
    measurementid = models.IntegerField(primary_key=True)
    total_sent = models.BigIntegerField()
    total_recv = models.BigIntegerField()
    total_till_now = models.BigIntegerField()
    mobile_sent = models.BigIntegerField()
    mobile_recv = models.BigIntegerField()
    mobile_till_now = models.BigIntegerField()
    class Meta:
        db_table = u'usage'
        managed=False

class Traceroute(models.Model):
    tracerouteid = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=100)
    srcip = models.CharField(max_length=50)
    dstip = models.CharField(max_length=50)
    tracetype = models.CharField(max_length=5)
    measurementid = models.ForeignKey(Measurement, to_field='measurementid', db_column='measurementid')
    class Meta:
        db_table = u'traceroute'
        managed=False

class WarmupExperiment(models.Model):
    lowest = models.FloatField(null=True, blank=True)
    highest = models.FloatField(null=True, blank=True)
    version = models.CharField(max_length=10, blank=True)
    dstip = models.CharField(max_length=50, blank=True)
    total_count = models.IntegerField(null=True, blank=True)
    gap = models.FloatField(null=True, blank=True)
    measurementid = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'warmup_experiment'
        managed=False

class WarmupPing(models.Model):
    value = models.FloatField(null=True, blank=True)
    sequence_count = models.IntegerField(null=True, blank=True)
    period = models.FloatField(null=True, blank=True)
    warmupid = models.AutoField(primary_key=True)
    measurementid = models.ForeignKey(Measurement, to_field='measurementid', db_column='measurementid')
    class Meta:
        db_table = u'warmup_ping'
        managed=False

class Hop(models.Model):
    hopid = models.AutoField(primary_key=True)
    address = models.CharField(max_length=50)
    hostname = models.CharField(max_length=100)
    hopnumber = models.IntegerField()
    rtt = models.FloatField()
    tracerouteid = models.ForeignKey(Traceroute, to_field='tracerouteid', db_column='tracerouteid')
    class Meta:
        db_table = u'hop'
        managed=False

class Application(models.Model):
    name = models.CharField(max_length=20)
    package = models.CharField(max_length=50, primary_key=True)
    class Meta:
        db_table = u'application'
        managed=False

class ApplicationUse(models.Model):
    application_useid = models.AutoField(primary_key=True)
    package = models.ForeignKey(Application, to_field='package', db_column='package')
    total_sent = models.BigIntegerField()
    total_recv = models.BigIntegerField()
    measurementid = models.ForeignKey(Measurement, to_field='measurementid', db_column='measurementid')
    isrunning = models.BooleanField()
    total_diff = models.BigIntegerField()
    isforeground = models.BooleanField()
    class Meta:
        db_table = u'application_use'
        managed=False


class Lastmile(models.Model):
    avg = models.FloatField()
    stdev = models.FloatField()
    min = models.FloatField()
    max = models.FloatField()
    scrip = models.CharField(max_length=50)
    dstip = models.CharField(max_length=50)
    firstip = models.CharField(max_length=50)
    time = models.DateTimeField()
    hopcount = models.IntegerField()
    measurementid = models.ForeignKey(Measurement, to_field='measurementid', db_column='measurementid')
    lastmileid = models.AutoField(primary_key=True)
    class Meta:
        db_table = u'lastmile'
        managed=False


class DNSMeasurement(models.Model):
    dns_id = models.AutoField(primary_key=True)
    measurement_id = models.ForeignKey(MobiMeasurement,
                                       to_field='measurement_id',
                                       db_column='measurement_id')
    qtype = models.CharField(max_length=10)
    qclass = models.CharField(max_length=10)
    qname = models.CharField(max_length=100)
    server = models.CharField(max_length=25)
    completed = models.BooleanField()

    class Meta:
        db_table = u'dns_measurements'
        managed=False

class DNSResult(models.Model):
    result_id = models.AutoField(primary_key=True)
    dns_id = models.ForeignKey(DNSMeasurement, to_field='dns_id',
                               db_column='dns_id')
    measurement_id = models.ForeignKey(MobiMeasurement,
                                       to_field='measurement_id',
                                       db_column='measurement_id')
    qtype = models.CharField(max_length=10)
    qclass = models.CharField(max_length=10)
    qname = models.CharField(max_length=100)
    server = models.CharField(max_length=25)
    resp_time = models.IntegerField()
    is_tc_set = models.BooleanField()
    is_valid = models.BooleanField()
    query_id = models.IntegerField()
    resp_id = models.IntegerField()
    rcode = models.CharField(max_length=25)
    payload = models.TextField()  # BinaryField if upgrade

    class Meta:
        db_table = u'dns_results'
        managed=False


class DNSAnswer(models.Model):
    result_id = models.AutoField(primary_key=True)
    dns_id = models.ForeignKey(DNSMeasurement, to_field='dns_id',
                               db_column='dns_id')
    result_id = models.ForeignKey(DNSResult, to_field='result_id',
                                  db_column='result_id')
    name = models.CharField(max_length=100)
    rtype = models.CharField(max_length=10)
    rdata = models.CharField(max_length=100)

    class Meta:
        db_table = u'dns_answers'
        managed=False

