from clint.textui import progress
import requests

def download(url, name, path):
	r = requests.get(url, stream=True)
	path = path + name + '.mp4'

	print("[+] Downloading {} :".format(name))
	with open(path, 'wb') as f:
		total_length = int(r.headers.get('content-length'))
		for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
			if chunk:
				f.write(chunk)
				f.flush()