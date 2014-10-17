import urllib
import urllib2
from bs4 import BeautifulSoup
import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4


def getDownloadDict():
	bugle = 'http://hellobuglers.com/podcasts/'
	html = urllib2.urlopen(bugle).read()
	soup = BeautifulSoup(html)

	episodes = [link.get('href') for link in soup.find_all('a') if ('.mp3' in link.get('href')) or ('.m4a' in link.get('href'))]
	downloads = {}
	for e in episodes:
		downloads[getTitle(e)] = e
	return downloads

def getTitle(e):
	title = e.split('/')[-1]
	title = title.replace('%20','-')
	if title.split('-')[0].isdigit():
		title = '-'.join(title.split('-')[1:])
	replacements = {'---':'-','--':'-','bugle-bugle':'Bugle-Episode','bugle-the-bugle':'bugle'}
	for k,v in replacements.items():
		title = title.replace(k,v)
	return title

def downloadFiles():
	files = getDownloadDict()
	for title,url in files.items():
		urllib.urlretrieve(url,title)
		print "Downloaded: "+title
	return files

def tagFiles():
	for f in os.listdir(os.getcwd()):
		title = f.split('.')[0]
		title = title.replace('-',' ')
		print "Tagging: "+title
		try:
			audio = MP3(f)
			try:
				audio.add_tags(ID3=EasyID3)
			except:
				pass
			audio["title"] = title.encode('utf8')
			audio["artist"] = u"The Bugle"
			audio.save()
		except:
			pass
		try:
			audio = MP4(f)
			audio["titl"] = title.encode('utf8')
			audio["\xa9ART"] = u"The Bugle"
			audio.save()
		except: 
			pass

if __name__ == "__main__":
	print "===== Starting Downloads ====="
	downloadFiles()
	print "===== Downloads Completed ====="
	print("\n")*3
	print "===== Tagging Files ====="
	tagFiles()
	print "===== ALL DONE! ====="

