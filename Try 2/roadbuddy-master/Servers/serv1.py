# first of all import the socket library
import socket               
import requests
import pickle
import requestsapirest
# next create a socket object
s = socket.socket()         
print ("Socket successfully created")

potholelist=[]
def loaddata():
   potholelist=[]
   f = open('facee.pckl', 'rb')
   potholelist = pickle.load(f)
   f.close()
   return potholelist
def savedata(potholelist):
   f = open('facee.pckl', 'wb')
   pickle.dump(potholelist, f)
   f.close()
print(loaddata())
def sendtoweb(potholelist):
   str1="["
##   i=potholelist[0]
##   str1+="{lat:"+i[0]+",lng:"+i[1]+"}"
   for i in potholelist:
      str1+="{lat:"+str(i[0])+",lng:"+str(i[1])+"},\n"
   str1+="]"
   print(str1)
potholelist=loaddata()
sendtoweb(potholelist)
# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 9002
s.bind(('', port))        
print ("socket binded to %s" %(port))
 
# put the socket into listening mode
s.listen(5)     
print ("socket is listening") 
 
# a forever loop until we interrupt it or 
# an error occurs
while True:
   


   # Establish connection with client.
   c, addr = s.accept()     
   print ('Got connection from', addr)
   
   # send a thank you message to the client. 
   #c.send('Thank you for connecting'.encode())
   #print(c.recv (1024).decode())
   data=str(c.recv(1024).decode())
   print(data)
   if("Breakdown"==data):
       requestsapirest.alertmsg("MAJOR","Breakdown Occured:Location Updated")
       c.send("Acknowledged".encode())
   if("accident" in data.split(":")):
       
       requestsapirest.updateaccident(float(data.split(":")[1]),float(data.split(":")[2]))
       c.send("Acknowledged".encode())
       
       
       
       
   if("sendpothole"==data):
      str1=""
      for i in potholelist:
         str1+=str(i[0])+","+str(i[1])+":"
      c.send(str1[:-1].encode())
      #c.send('Thank you for connecting'.encode())
      
   if("android" in data.split(":")):
      lat,long=data.split(":")[1].split(",")
      potholelist.append((lat,long))
      print(potholelist)
      savedata(list(set(potholelist)))
      c.send("pothl".encode())
      
   # Close the connection with the client
   c.close()
