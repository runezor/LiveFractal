#!/usr/bin/python3

import requests
import os

host="kaarl.dk"
path="/mandelbrot/uploadMAP.php"

url = "http://%s%s" % (host, path)

def upload():
	print("Uploading...")
	with open('pointer.png','rb') as fp:
		myfiles={'fileToUpload': fp}
		r=requests.post(url,files=myfiles,data={'code': 'secret'},verify=True)
	print(r.text)
