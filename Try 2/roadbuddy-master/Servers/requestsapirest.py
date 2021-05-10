import requests
from requests.auth import HTTPBasicAuth
import time
def alertmsg(a,b):
    url = 'https://team6.unlimitenablement.co.in/alarm/alarms'
    timex=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(None))[:-2]+"+05:30"
    data = '''{
            "source": {
            "id": "203" },
        "type": "TestAlarm",
        "text": "'''+str(b)+'''",
        "severity": "'''+str(a)+'''",
        "status": "ACTIVE",
        "time": "'''+timex+'''"
    }'''
    response = requests.post(url, data=data,auth=HTTPBasicAuth("team6/team6","pass@123"))
    print(response)
    url = 'https://team6.unlimitenablement.co.in/inventory/managedObjects/203'

    data = '''{
	"c8y_Position": {
    	    	"alt": 67,

      	"lng": '''+str(b)+''',
      	"lat": '''+str(a)+''' }
}'''
    response = requests.put(url, data=data,auth=HTTPBasicAuth("team6/team6","pass@123"))
    print(response)
    
def updateaccident(a,b):
    alertmsg("CRITICAL","Breakdown:Location updated")
    timex=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(None))[:-2]+"+05:30"    
    url = 'https://team6.unlimitenablement.co.in/event/events'
    data = '''{
	"c8y_Position": {
    	
      	"lng":'''+str(b) +''',
      	"lat":'''+str(a) +''' },
	"time":"'''+timex+'''",
    "source": {
    	"id":"203" }, 
    "type": "c8y_LocationUpdate",
    "text": "LocUpdate"
    }'''
    response = requests.post(url, data=data,auth=HTTPBasicAuth("team6/team6","pass@123"))
    print(response)
    url = 'https://team6.unlimitenablement.co.in/inventory/managedObjects/203'

    data = '''{
	"c8y_Position": {
    	 "alt": 67,
      	"lng": '''+str(b)+''',
      	"lat": '''+str(a)+''' }
}'''
    response = requests.put(url, data=data,auth=HTTPBasicAuth("team6/team6","pass@123"))
    print(data)
    
