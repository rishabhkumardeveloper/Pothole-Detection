from boltiot import Sms, Bolt
SID = 'AC9cf827f15186dcdfb6e6a8d7e74793cc' 
AUTH_TOKEN = '03d4ad1075d408e009aec2c6a3ea49ad' 
FROM_NUMBER = '+18323532587'
TO_NUMBER = '+919521153638'

sms = Sms(SID, AUTH_TOKEN, TO_NUMBER, FROM_NUMBER)
response = sms.send_sms("The Current temperature sensor value is DAMN HOT")