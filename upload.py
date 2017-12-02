#!/usr/bin/python3

import requests
import os

host="kaarl.dk"
path="/mandelbrot/upload.php"

url = "http://%s%s" % (host, path)

def upload(i):
	print("Uploading...")
	with open(str(i)+'.jpg','rb') as fp:
		myfiles={'fileToUpload': fp}
		r=requests.post(url,files=myfiles,verify=True)
	print(r.text)
