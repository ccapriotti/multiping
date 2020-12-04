import os
import sys
import datetime
from multiprocessing.pool import Pool


hostList = ["192.168.1.1", "192.168.1.2", "localhost", "8.8.8.8", "192.168.1.111"] 
now = datetime.datetime.now()
timestamp = now.strftime("%Y-%m-%d-%H:%M:%S")
exportFile = "pingtest.log"


def pingme(host):
    return os.system("ping -w 5 -q -c 1 " + host + "> /dev/null 2>&1")

allResults = []
with Pool( len(hostList) ) as p:
    allResults = p.map(pingme, hostList)
    

resultLine = ["start:" + timestamp]
for i in range(len(hostList)):
    resultLine.append( hostList[i] + ":" + ("True" if allResults[i]==0 else "False" )  )

now = datetime.datetime.now()
timestamp = now.strftime("%Y-%m-%d-%H:%M:%S")
resultLine.append("end:" + timestamp) 
  
    
if len(sys.argv) > 1:
    if sys.argv[1] == "--debug":
        print(", ".join(resultLine))
    else:
        print("Unknown option")
else: 
    try:
        f = open( exportFile, "a" )
    except:
        print( sys.argv[0] + ": error opening file", exportFile )
        sys.exit( 255 )
    
    f.write( ", ".join(resultLine) + "\n" )
    f.close()
