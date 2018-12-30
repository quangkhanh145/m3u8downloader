import requests
import sys
import shutil
import os
import time

url = sys.argv[1]
fileName = sys.argv[2]

if not os.path.exists("./videos/m3u8/"):
	os.makedirs("videos/m3u8")
if not os.path.exists("./videos/tmp/"):
	os.makedirs("videos/tmp")
res = requests.get(url,stream=True)
if res.status_code == 200:
    with open('./videos/m3u8/'+fileName,'wb') as f:
        for chunk in res:
            f.write(chunk)
    print fileName+' downloaded'
else:
	print 'url not available'
	quit()

with open('./videos/m3u8/'+fileName, 'r') as f:
    tslist = [line.rstrip() for line in f if line.rstrip().endswith('.ts')]
if len(tslist) > 0:
    print 'Total '+ str(len(tslist)) +' files'
else:
    print 'No ts file found.'
    exit()

index = 1
tsNames = []
for tsUrl in tslist:
    videoNameTmp = fileName[0:-3]+'_'+str(index)+fileName[-3:]
    if not os.path.isfile('./videos/tmp/'+videoNameTmp):
    	beforeDownload = time.time()
        res = requests.get(tsUrl, stream=True)
        afterDownload = time.time()
        speed = (len(res.content)/(afterDownload - beforeDownload))/1048576
        if res.status_code == 200:
            with open('./videos/tmp/'+videoNameTmp, 'wb') as f:
                for chunk in res:
                    f.write(chunk)
            progress = (index/((len(tslist)+1)*1.0))*100
            print  'Speed: ' + str(round(speed,2)) + ' MB/s  || '+ videoNameTmp+' downloaded  || ' + '{:0.3f}'.format(round(progress,3)) + '%\r',
        else:
            print '\nConnection error'
            exit()
    tsNames.append(videoNameTmp)
    index += 1

if index == len(tslist)+1:
    with open('./videos/'+fileName, 'wb') as f:
        for ts in tsNames:
            with open('./videos/tmp/'+ts, 'rb') as mergefile:
                shutil.copyfileobj(mergefile, f)
            os.remove('./videos/tmp/'+ts)
        print fileName+' merged.'
else:
    print 'Merge failed, missing files.'