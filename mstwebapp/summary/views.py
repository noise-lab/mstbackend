from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import json
import getJSON
import insertJSON 
from models import *
import error_message_helper
import traceback
import calendar
import time

def log_dataerror(rawcontent):
    print traceback.format_exc()
    if not os.path.exists(settings.DATA_MOBI_ROOT+"/error/"):
       os.makedirs(settings.DATA_MOBI_ROOT+"/error/")
    outjson = open(settings.DATA_MOBI_ROOT+"/error/"+str(calendar.timegm(time.gmtime()))+".json", "w")
    outjson.write(rawcontent)
    outjson.close()
 

def values(request):
    data={}
    data['values'] = getJSON.values()
    return HttpResponse(json.dumps(data))

def dnsvalues(request):
    data={}
    data['values'] = getJSON.dnsvalues()
    return HttpResponse(json.dumps(data))

def surveys(request):
    data = getJSON.surveysjson()
    return HttpResponse(data)

@csrf_exempt
def measurement(request):
    response = {}
    message=[]

    #reqdata = request.META.items()
    print("REQ "+request.META['REMOTE_ADDR']+" --- "+request.META['HTTP_USER_AGENT'])
    #for k, v in values:
    #    print(str(k)+" --- "+str(v))

    ''' Parse JSON '''
    try:
        rawcontent = request.read()
        content = unicode(rawcontent, errors='ignore')
        request_object = json.loads(content)
	print "JSON parsed!"
    except:
	print "JSON parse FAILED!"
        log_dataerror(rawcontent)
        return HttpResponse(error_message_helper.invalid_format())

    ''' Extract data from JSON '''
    try:
	m_time = request_object['time']
        m_localtime = request_object['localtime']
	m_deviceid = request_object['deviceid']

        print("DEV "+str(m_deviceid))
        
        try:
            m_pings = request_object['pings']
        except:
	    m_pings = {}

	try:
	    m_traceroutes = request_object['traceroutes']
	except:
	    m_traceroutes = {}

        try:
            m_lastmiles = request_object['lastmiles']
        except:
            m_lastmiles = {}

        try:
            m_warmup = request_object['warmup_experiment']
        except:
            m_warmup = {}

	try:
	    m_device = request_object['device']
	except:
	    m_device = None

        try:
            m_version = m_device['applicationVersion']
        except:
            m_version = None

	try:
	    m_network = request_object['network']
	except:
	    m_network = None

        try:
            m_sim = request_object['sim']
        except:
	    m_sim = None
        
	try:
	    m_throughput = request_object['throughput']
	except:
	    m_throughput = None

	try:
	    m_usage = request_object['usage']
	except:
	    m_usage = None

	try:
	  m_battery = request_object['battery']
	except:
	  m_battery = None

        try:
            m_wifi = request_object['wifi']
        except:
            m_wifi = None

        try:
            m_state = request_object['state']
        except:
	    m_state = None

        try:
            m_ismanual = request_object['isManual']
        except:
            m_ismanual = 0
	print "Data extracted from JSON!"
    except Exception as inst:
	'''Exception if one of the required fields is missing'''
        print traceback.format_exc()
	message.append(error_message_helper.insert_entry_fail("measurement-extract",inst))
        insertJSON.error_log(request_object,m_deviceid,request)
        return HttpResponse(str(message))     
    
    ''' Construct measurement '''
    measurement = Measurement()
    measurement.localtime = m_localtime
    measurement.time = m_time
    if m_ismanual == 1:
        measurement.ismanual = True
    else:
        measurement.ismanual = False

    ''' Check for a duplicate entry '''
    try:
        device=Device.objects.filter(deviceid=m_deviceid)[0] # Check if the device exists in the DB
        try:
            duplicate = Measurement.objects.filter(deviceid=device,time=m_time)[0] # Check if the measurement is a duplicate
            return HttpResponse(error_message_helper.duplicate_entry())
        except Exception as inst:
            pass
    except:
        pass

    ''' Insert device '''
    try:
        device=insertJSON.device(m_device,m_deviceid,m_sim)
	print "Device inserted!"
    except Exception as inst:
        message.append(error_message_helper.insert_entry_fail("device++",inst))
        insertJSON.error_log(message,m_deviceid,request)
        return HttpResponse(str(message))  

    measurement.deviceid = device

    try:
        measurement.applicationversion = m_version
    except:
        measurement.applicationversion = None

    print measurement.applicationversion
    ''' Insert measurement '''
    try:
	measurement.save()
	print "Measurement inserted!"
    except Exception as inst:
	message.append(error_message_helper.insert_entry_fail("measurement",inst))
	return HttpResponse(str(message))

    ''' Insert network '''
    try:
	network=insertJSON.network(m_network,measurement)
	print "Network inserted!"
    except Exception as inst:
        message.append(error_message_helper.insert_entry_fail("network",inst))    
    
    ''' Insert throughput '''
    if not m_throughput == None:
        try:
	    throughput=insertJSON.throughput(m_throughput,measurement)
	    print "Throughput inserted!"
	except Exception as inst:
            log_dataerror(rawcontent)
	    message.append(error_message_helper.insert_entry_fail("throughput",inst))
         
    ''' Insert wifi '''
    if not m_wifi == None:
        try:
	    wifi=insertJSON.wifi(m_wifi,measurement)
	    print "Wifi inserted!"
	except Exception as inst:
	    message.append(error_message_helper.insert_entry_fail("wifi",inst))
    
    ''' Insert battery '''
    try:
        battery=insertJSON.battery(m_battery,measurement)
	print "Battery inserted!"
    except Exception as inst:
        message.append(error_message_helper.insert_entry_fail("battery",inst))
    

    ''' Insert usage '''
    if not m_usage == None:
	try:
	    usage=insertJSON.usage(m_usage,measurement)
	    print "Usage inserted!"
	except Exception as inst:
	    message.append(error_message_helper.insert_entry_fail("usage",inst))

    ''' Insert state '''
    try:
       if not throughput.measurementid == None:
           s_cellid = m_state['cellId']
           s_localtime = m_state['localtime']
           s_time = m_state['time']
           s_deviceid = m_state['deviceid']
           s_type = m_state['networkType']
           
           localtime_object = datetime.strptime(s_localtime, '%Y-%m-%d %H:%M:%S')
           s_timeslice = (int(localtime_object.hour)/6)*6
           day_of_week = int(localtime_object.strftime('%w'))
           
           if day_of_week>0 and day_of_week<6:
               s_weekday = 1
           else:
               s_weekday = 0
           
           try:    
               current_states =State.objects.filter(cellid=s_cellid,deviceid=s_deviceid,timeslice=s_timeslice,weekday=s_weekday,networktype=s_type)[0]
           except:
              states = State(cellid=s_cellid,deviceid=s_deviceid,timeslice=s_timeslice,weekday=s_weekday,networktype=s_type,measurementid=measurement.measurementid)
              states.save()
	      print "State inserted!"

    except Exception as inst:
       pass   
    
    ''' Insert ping '''
    try:
        insertJSON.pings(m_pings,measurement)
	print "Pings inserted!"
    except Exception as inst:
        log_dataerror(rawcontent)
        message.append(error_message_helper.insert_entry_fail("ping",inst))        

    ''' Insert lastmiles '''
    try:
        insertJSON.lastmiles(m_lastmiles,measurement)
    except Exception as inst:
        message.append(error_message_helper.insert_entry_fail("lastmile",inst))

    ''' Insert warmup '''
    try:
        insertJSON.warmup(m_warmup,measurement)
    except Exception as inst:
        message.append(error_message_helper.insert_entry_fail("warmup",inst))

    ''' Insert traceroute '''
    try:
	insertJSON.traceroutes(m_traceroutes,measurement)
    except Exception as inst:
        log_dataerror(rawcontent)
	message.append(error_message_helper.insert_entry_fail("traceroute",inst))
        
    response['message'] = 'measurement inserted: ' + str(message)
    response['status'] = 'OK'

    return HttpResponse(str(response))


def testDB(request):
    sim = {}
    sim["serialNumber"] = "117a3c3d3b9ea53270eea8d9b593f2789efea80b"
    sim["state"] = "READT"
    sim["operatorCode"] = "71204"
    sim["operatorName"] = "movistar"
    sim["networkCountry"] = "cr"
    insertJSON.sim(sim) 

    dev = {}
    dev['phoneType'] = "GSM"
    dev['phoneNumber'] = "e7b7785e7003fc3743fb6a1b3f4f94cc31e9002c"
    dev['softwareVersion'] = "01" 
    dev['phoneModel'] = "SM-J200H"
    dev['androidVersion'] = "5.1.1"
    dev['phoneBrand'] = "samsung"
    dev['deviceDesign'] = "j23g"
    dev['manufacturer'] = "samsung"                                                                                                                      
    dev['productName'] = "dd" 
    dev['radioVersion'] = "unknown" 
    dev['boardName'] = "SC7730SE"
    dev['datacap'] = 100
    dev["networkCountry"] = "bd" 
    dev["networkName"] = "Airtel"
    dev["emailAddress"] = ""
    dev["applicationVersion"] = 413 
    device=insertJSON.device(dev, "", sim) 
 #e7b7785e7003fc3743fb6a1b3f4f94cc31e9002c | GSM       | 4243c1f57f8376daa30b36544570433420406a10 | 01              | SM-J200H   | 5.1.1          | samsung    | j23g         | samsung      | j23gdd      | unknown      | SC7730SE  |              | bd             | Airtel      |     100 |              |              |                413 |            1 |             7 |                   | 2016-02-15 20:03:46

    link = {}
    link['count'] = 1
    link['message_size'] = 65440
    link['time'] = 34
    link['speedInBits'] = "0.9"
    link['dstPort'] = "80"
    link['dstIp'] = "127.0.0.1"
# 1 |        42890 |    36320 | 9.44713656387665 | 9915 | ruggles.gtnoise.net
    insertJSON.link(link)

    measurement = Measurement()
    measurement.localtime = '2012-11-19 23:08:54'
    measurement.time = '2012-11-20 04:08:54'
    measurement.ismanual = False
    measurement.deviceid = device
        
    measurement.applicationversion = '415'

    measurement.save()
    return HttpResponse("TEST_OK")
