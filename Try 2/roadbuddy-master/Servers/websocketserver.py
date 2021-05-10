from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import pickle
def loaddata():
   potholelist=[]
   print("called")
   f = open('facee.pckl', 'rb')
   potholelist = pickle.load(f)
   f.close()
   return potholelist

def sendtoweb(potholelist):
   print("called2")
   str1=""
##   str1="["
##   i=potholelist[0]
##   str1+="{lat:"+i[0]+",lng:"+i[1]+"}"
   for i in potholelist:
      str1+='{"lat":'+str(i[0])+',"lng":'+str(i[1])+'}-\n'
   str1=str1[:-2]
##   str1+="]"
   print(str1)
   return str1
def testt():
    print("called")
strimp=sendtoweb(loaddata())
class SimpleEcho(WebSocket):
##    def loaddata():
##       potholelist=[]
##       print("called")
##       f = open('facee.pckl', 'rb')
##       potholelist = pickle.load(f)
##       f.close()
##       return potholelist
##
##    def sendtoweb(potholelist):
##       print("called2")
##       str1="["
##       for i in potholelist:
##          str1+="{lat:"+str(i[0])+",lng:"+str(i[1])+"},\n"
##       str1+="]"
##       print(str1)
##       return str1
    def handleMessage(self):
        #st1=sendtoweb(potholelist())
        # echo message back to client
        global strimp
        print(strimp)
##        strrr=sendtoweb(loaddata())
##        self.sendMessage(str(strrr))
        strrr=sendtoweb(loaddata())
        self.sendMessage(str(strrr))

##        print(self.data)
##        print(clients)
##        for client in clients:
##            client.sendMessage(self.data)

    def handleConnected(self):
##        st1=sendtoweb(potholelist())
##        self.sendMessage(st1)
        print("connected")
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')

server = SimpleWebSocketServer('', 8000, SimpleEcho)
server.serveforever()

