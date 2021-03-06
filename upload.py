#!/usr/bin/python3

import requests
import os

host="kaarl.dk"
path="/mandelbrot/upload.php"

url = "http://%s%s" % (host, path)

def upload(x,y,w,h):
	print("Uploading...")

	success = False
	while success is False:
		try:
			with open('1.jpg','rb') as fp:
				myfiles={'fileToUpload': fp}
				r=requests.post(url,files=myfiles,data={'code': 'sec-ret', 'dbx': x, 'dby': y, 'dbw': w, 'dbh': h},verify=True)
				success = True
		except:
			pass

	print(r.text)
