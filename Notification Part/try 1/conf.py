SID = 'AC8efc3945272c7baaa4c6bd2754c617f6' 
AUTH_TOKEN = 'c2b416dc007ff1ffe9d24d1bbdb96de2' 
FROM_NUMBER = '+17039976743'
TO_NUMBER = '+919675495980'

from boltiot import Sms, Bolt
import json, time
minimum_limit = 300
maximum_limit = 600  
mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)
sms = Sms(conf.SID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)
while True: 
    print ("Reading sensor value")
    response = mybolt.analogRead('A0') 
    data = json.loads(response) 
    print("Sensor value is: " + str(data['value']))
    try: 
        sensor_value = int(data['value']) 
        if sensor_value > maximum_limit or sensor_value < minimum_limit:
            print("Making request to Twilio to send a SMS")
            response = sms.send_sms("The Current temperature sensor value is DAMN HOT")
            print("Response received from Twilio is: " + str(response))
            print("Status of SMS at Twilio is :" + str(response.status))
    except Exception as e: 
        print ("Error occured: Below are the details")
        print (e)
    time.sleep(10)

