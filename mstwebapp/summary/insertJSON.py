from datetime import datetime, timedelta
from models import *
import error_message_helper as emh
import traceback

def sim(dev):
    s = Sim()
    try:
        try:
            s.serialnumber = dev["serialNumber"]
        except:
            pass
        try:
            s.state = dev["state"]
        except:
            pass
        try:
            s.operatorcode = dev["operatorCode"]
        except:
            pass
        try:
            s.operatorname = dev["operatorName"]
        except:
            pass
        try:
            s.networkcountry = dev["networkCountry"]
        except:
            pass

        s.save()
    except Exception as inst:
        pass
    return s

def device(dev, m_deviceid, m_sim):
    count = 0
    message = []
    d = Device()
    try:
        d = Device.objects.filter(deviceid=m_deviceid)[0]
    except Exception as inst:
        d = Device()
        try:
            d.deviceid = m_deviceid
        except Exception as inst:
            message.append(emh.insert_entry_fail("device", inst))

    try:

        try:
            d.phonenumber = dev['phoneNumber']
        except Exception as inst:
            message.append(emh.insert_entry_fail("device", inst))
        try:
            d.phonetype = dev['phoneType']
        except Exception as inst:
            message.append(emh.insert_entry_fail("device", inst))
        try:
            d.softwareversion = dev['softwareVersion']
        except Exception as inst:
            message.append(emh.insert_entry_fail("device", inst))
        try:
            d.phonemodel = dev['phoneModel']
        except Exception as inst:
            message.append(emh.insert_entry_fail("device", inst))
        try:
            d.androidversion = dev['androidVersion']
        except Exception as inst:
            message.append(emh.insert_entry_fail("device", inst))
        try:
            d.phonebrand = dev['phoneBrand']
        except Exception as inst:
            message.append(emh.insert_entry_fail("device", inst))
        try:
            d.devicedesign = dev['deviceDesign']
        except Exception as inst:
           message.append(emh.insert_entry_fail("device", inst))
        try:
            d.manufacturer = dev['manufacturer']
        except Exception as inst:
            message.append(emh.insert_entry_fail("device", inst))
        try:
            d.productname = dev['productName']
        except Exception as inst:
            message.append(emh.insert_entry_fail("device", inst))
        try:
            d.radioversion = dev['radioVersion']
        except Exception as inst:
            message.append(emh.insert_entry_fail("device", inst))
        try:
            d.boardname = dev['boardName']
        except Exception as inst:
            message.append(emh.insert_entry_fail("device", inst))
        try:
            d.datacap = dev['datacap']
        except Exception as inst:
            message.append(emh.insert_entry_fail("device", inst))
        try:
            d.networkcountry = dev["networkCountry"]
        except Exception as inst:
            message.append(emh.insert_entry_fail("device", inst))
        try:
            d.networkname = dev["networkName"]
        except Exception as inst:
            message.append(emh.insert_entry_fail("device", inst))
        try:
            d.emailaddress = dev["emailAddress"]
        except Exception as inst:
            message.append(emh.insert_entry_fail("device", inst))
        try:
            d.applicationversion = dev["applicationVersion"]
        except Exception as inst:
            message.append(emh.insert_entry_fail("device", inst))
        try:
            s = sim(m_sim)
            d.serialnumber = s.serialnumber
        except Exception as inst:
            message.append(emh.insert_entry_fail("sim", inst))

        d.save()
    except Exception as inst:
        message.append(emh.insert_entry_fail("device", inst))
    return d


def link(dev):
    l = Link()
    try:
        l.count = dev['count']
        l.message_size = dev['message_size']
        l.duration = dev['time']
        l.speed = dev['speedInBits']
        l.port = dev['dstPort']
        l.ip_address = dev['dstIp']
        l.save()
    except:
        print traceback.format_exc()
        pass
    return l


def network(dev, m):

    n = Network()
    try:
        n.measurementid = m.measurementid
    except:
        pass
    try:
        n.networktype = dev["networkType"]
    except:
        n.networktype = "null"
    try:
        n.connectiontype = dev["connectionType"]
    except:
        n.connectiontype = "null"

    try:
        n.cellid = parse(dev['cellId'])
    except:
        n.cellid = "null"

    try:
        n.celllac = parse(dev["cellLac"])
    except:
        n.celllac = "null"

    try:
        n.celltype = parse(dev["cellType"])
    except:
        n.celltype = "null"
    try:
        n.longitude = parseFloat(dev["basestationLong"], -99)
    except:
        n.longitude = -99
    try:
        n.latitude = parseFloat(dev["basestationLat"], -99)
    except:
        n.latitude = -99
    try:
        n.networkid = parseInt(dev["networkid"], -1)
    except:
        n.networkid = -1
    try:
        n.systemid = parseInt(dev["systemid"], -1)
    except:
        n.systemid = -1
    try:
        n.datastate = dev["dataState"]
    except:
        n.datastate = "null"
    try:
        n.dataactivity = dev["dataActivity"]
    except:
        n.dataactivity = "null"
    try:
        n.signalstrength = dev["signalStrength"]
    except:
        n.signalstrength = "-1"
    n.save()

    return n


def throughput(dev, m):

    t = Throughput()
    try:
        t.measurementid = m.measurementid
        t.uplinkid = link(dev['upLink'])
        t.downlinkid = link(dev['downLink'])
        t.save()
    except:
        #print traceback.format_exc()
        print "Warning: missing upLink/downLink for throughput"
        pass
    return t


def usage(dev, m):
   
    u = Usage()
    u.measurementid = m.measurementid
   
    last = None
   
    try:
        last_measurement = Measurement.objects.filter(deviceid=m.deviceid.deviceid).order_by('time')[0]
        last = Usage.objects.filter(measurementid=last_measurement.measurementid)[0]
    except:
        pass

    try:
        u.total_sent = dev['total_sent']
    except:
        pass

    try:
        u.total_recv = dev['total_recv']
    except:
        pass
    try:
        u.mobile_sent = dev['mobile_sent']
    except:
        pass
    try:
        u.mobile_recv = dev['mobile_recv']
    except:
        pass
    u.total_till_now = 0
    u.mobile_till_now = 0
    u.save()

    for app in dev['applications']:

        try:
            result = Application.objects.filter(package=app['packageName'][:50])[0]
        except:
            result = Application(package=app['packageName'][:50], name=app['name'][:20])
            result.save()

        appUse = ApplicationUse()

        try:
            appUse.package = result
        except:
            pass

        try:
            appUse.total_sent = app['total_sent']
        except:
            pass

        try:
            if app['isRunning'] == 1:
                appUse.isrunning = True
            else:
                appUse.isrunning = False
        except:
            pass

        try:
            if app['isForeground'] == 1:
                appUse.isforeground = True
            else:
                appUse.isforeground = False
        except:
            pass

        try:
            appUse.total_recv = app['total_recv']
        except:
            pass

        try:
            appUse.measurementid = m
        except:
            pass

        appUse.save()

    return u


def pings(pings, measurement):
   
    for p in pings:
        ping = Ping()


        ping.measurementid = measurement

        try:
            ping.scrip = p['src_ip']
        except:
            pass
        try:
            ping.dstip = p['dst_ip']
        except:
            pass
        try:
            ping.time = p['time']
        except:
            pass

        measure = p['measure']


        try:
            ping.avg = measure['average']
        except:
            pass
        try:
            ping.stdev = measure['stddev']
        except:
            pass
        try:
            ping.min = measure['min']
        except:
            pass
        try:
            ping.max = measure['max']
        except:
            pass

        ping.save()

def battery(dev, m):

    g = Battery()
    g.measurementid = m.measurementid

    try:
        g.ispresent = dev['isPresent']
    except:
        pass
    try:
        g.technology = dev['technology']
    except:
        pass
    try:
        g.plugged = dev['plugged']
    except:
        pass
    try:
        g.scale = dev['scale']
    except:
        pass
    try:
        g.health = dev['health']
    except:
        pass
    try:
        g.voltage = dev['voltage']
    except:
        pass
    try:
        g.level = dev['level']
    except:
        pass
    try:
        g.temperature = dev['temperature']
    except:
        pass
    try:
        g.status = dev['status']
    except:
        pass

    g.save()

    return g


def traceroutes(traceroutes, measurement):

    for t in traceroutes:
        traceroute = Traceroute()

        traceroute.measurementid = measurement

        try:
            traceroute.srcip = t['srcIp']
        except:
            pass
        try:
            traceroute.dstip = t['dstIp']
        except:
            pass
        try:
            traceroute.hostname = t['hostname']
        except:
            pass
        try:
            traceroute.tracetype = t['type']
        except:
            pass

        traceroute.save()

        hops = t['hops']

        for h in hops:
            hop = Hop()
            hop.tracerouteid = traceroute
            try:
                hop.address = h['address']
            except:
                pass
            try:
                hop.hostname = h['hostname']
            except:
                pass
            try:
                hop.hopnumber = h['hopNumber']
            except:
                pass
            try:
                hop.rtt = h['rtt']
            except:
                pass
            hop.save()


def warmup(warm, m):
   
    w = WarmupExperiment()
    w.measurementid = m.measurementid
   
    try:
        w.lowest = warm['lowest']
    except:
        pass
    try:
        w.highest = warm['highest']
    except:
        pass
   
    try:
        w.version = warm['version']
    except:
        pass
    try:
        w.total_count = warm['total_count']
    except:
        pass
    try:
        w.gap = warm['time_gap']
    except:
        pass
    try:
        w.dstip = warm['dstip']
    except:
        pass

    w.save()

    try:
        for entry in warm['sequence']:
            e = WarmupPing()
            e.value = entry['value']
            e.sequence_count = entry['sequence']
            e.period = entry['period']
            e.measurementid = m
            e.save()
    except:
        pass
    return w

def lastmiles(lastmiles, measurement):

    for p in lastmiles:
        lastmile = Lastmile()

        lastmile.measurementid = measurement

        try:
            lastmile.scrip = p['src_ip']
        except:
            pass
        try:
            lastmile.dstip = p['dst_ip']
        except:
            pass
        try:
            lastmile.time = p['time']
        except:
            pass
        try:
            lastmile.hopcount = p['hopcount']
        except:
            pass
        try:
            lastmile.firstip = p['firstip']
        except:
            pass

        measure = p['measure']


        try:
            lastmile.avg = measure['average']
        except:
            pass
        try:
            lastmile.stdev = measure['stddev']
        except:
            pass
        try:
            lastmile.min = measure['min']
        except:
            pass
        try:
            lastmile.max = measure['max']
        except:
            pass

        lastmile.save()


def calculate_log(range):
    current_time = datetime.utcnow()
    ranged = timedelta(hours=float(range))
    l_time = current_time - ranged

    log = CalculateLog(log_time=current_time, time=l_time)
    log.save()

def error_log(message, device, request):

    error_log = ErrorLog()
    error_log.log_time = datetime.utcnow()
    error_log.deviceid = device
    error_log.error_text = str(message)
    error_log.user_agent = str(request.META['HTTP_USER_AGENT'])
    error_log.remote_addr = str(request.META['REMOTE_ADDR'])

    error_log.save()

def wifi(dev, m):
   
    w = Wifi()
    w.measurementid = m.measurementid
    w.ipaddress = dev['ipAddress']
    w.detailedinfo = dev['detailedInfo']
    w.rssi = dev['rssi']
    w.signalstrength = dev['strength']
    w.speed = dev['speed']
    w.units = dev['units']
 
    for spot in dev['wifiNeighbors']:

        try:
            result = WifiHotspot.objects.filter(macaddress=spot['macAddress'])[0]
        except:
            result = WifiHotspot()
            result.macaddress = spot['macAddress']
            result.ssid = spot['ssid']
            result.frequency = spot['frequency']
            result.capability = spot['capability'][:20]
            result.save()

        if spot['isConnected'] == 'true':
            w.connection = result
            w.save()

    for spot in dev['wifiNeighbors']:
        result = WifiHotspot.objects.filter(macaddress=spot['macAddress'])[0]

        wn = WifiNeighbor()
        wn.macaddress = result
        wn.measurementid = m
        if spot['isPreferred'] == 'true':
            wn.ispreferred = 1
        else:
            wn.ispreferred = 0
        wn.signallevel = spot['signalLevel']
        wn.save()

    w.save()
    return w


def dns(entry, msm):
    """Insert entry for a dns lookup measurement"""
    try:
        params = entry.get('parameters')
        dns_msm = DNSMeasurement()
        dns_msm.measurement_id = msm.measurement_id
        dns_msm.completed = entry['success']
        dns_msm.qclass = params['qclass']
        dns_msm.qtype = params['qtype']
        dns_msm.qname = params['target']
        dns_msm.server = params['server']
        dns_msm.save()

        # now parse each response and its answers
        vals = entry['values']
        for response in vals['results']:
            res = DNSResult()
            res.dns_id = dns_msm.dns_id
            res.qtype = response['qtype']
            res.qclass = response['qclass']
            res.qname = response['name']
            res.resp_time = response['respTime']
            res.is_tc_set = response['tc']
            res.is_valid = response['isValid']
            res.query_id = response['qryId']
            res.resp_id = response['respId']
            res.rcode = response['rcode']
            res.payload = response['payload']
            res.save()

            for answer in response['answers']:
                ans = DNSAnswer()
                ans.dns_id = dns_msm.dns_id
                ans.result_id = res.result_id
                ans.name = answer['name']
                ans.rtype = answer['rtype']
                ans.rdata = answer['rdata']
                ans.save()
    except Exception as exp:
        logger.exception("problem creating measurement")
        raise MobiParseExp(str(exp))
    return dns_msm

def parse(object):

    if object is None:
        return ''
    else:
        return object


def parseInt(object, backup):
    try:
        a = int(object)
        return object
    except:
        return backup


def parseFloat(object, backup):
    object = parse(object)
    try:
        a = float(object)
        return object
    except:
        return backup



