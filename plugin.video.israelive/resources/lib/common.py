# -*- coding: utf-8 -*-
import urllib,urllib2,sys,re,xbmcgui,xbmc,os,time,json

def downloader_is(url,name):
	import downloader,extract
	
	choice = True
	dialog = xbmcgui.Dialog()
	if name.find('repo') < 0:
		choice = dialog.yesno("IsraeLIVE" , "לחץ כן להתקנת תוסף חסר", name)
	 
	if choice == False:
		return
		
	addonsDir = xbmc.translatePath(os.path.join('special://home', 'addons')).decode("utf-8")
	dp = xbmcgui.DialogProgress()
	dp.create("IsraeLIVE", "Downloading", "", "Please Wait")
	packageFile = os.path.join(addonsDir, 'packages', 'isr.zip')
	try:
		os.remove(packageFile)
	except:
		pass
	downloader.download(url, packageFile, dp)
	dp.update(0, "", "Extracting Zip Please Wait")
	extract.all(packageFile, addonsDir, dp)
	#dp.update(0, "", "Downloading")
	#dp.update(0, "", "Extracting Zip Please Wait")
	xbmc.executebuiltin("UpdateLocalAddons")
	xbmc.executebuiltin("UpdateAddonRepos")

def unescape(text):
		try:			
			rep = {"&nbsp;": " ",
				   "\n": "",
				   "\t": "",
				   "\r":"",
				   "&#39;":"",
				   "&quot;":"\""
				   }
			for s, r in rep.items():
				text = text.replace(s, r)
				
			# remove html comments
			text = re.sub(r"<!--.+?-->", "", text)	
				
		except TypeError:
			pass

		return text

def OPEN_URL(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	
	response = urllib2.urlopen(req,timeout=100)
	link=response.read()
	response.close()
	return link
	
def isFileOld(file, deltaInSec):
	lastUpdate = 0 if not os.path.isfile(file) else int(os.path.getmtime(file))
	now = int(time.time())
	isM3uFileNotUpdate = True if (now - lastUpdate) > deltaInSec else False 
	return isM3uFileNotUpdate
	
def UpdateFile(file, url):
	lastModifiedFile = "{0}LastModified.txt".format(file[:file.rfind('.')])
	if not os.path.isfile(file) or not os.path.isfile(lastModifiedFile):
		fileContent = ""
	else:
		f = open(lastModifiedFile,'r')
		fileContent = f.read()
		f.close()
	
	req = urllib2.Request(url)
	try:
		response = urllib2.urlopen(req)
	except:
		return False
		
	headers = response.info()
	etag = headers.getheader("ETag")
	last_modified = headers.getheader("Last-Modified")
	if not last_modified:
		last_modified = etag
	isNew = fileContent != last_modified
	
	if isNew:
		try:
			data = response.read().replace('\r','')
		except:
			return False
			
		f = open(file, 'w')
		f.write(data)
		f.close()
		
		f = open(lastModifiedFile, 'w')
		f.write(last_modified)
		f.close()
		
	response.close()
	return isNew
	
def ReadList(fileName):
	try:
		f = open(fileName,'r')
		fileContent=f.read()
		f.close()
		content=json.loads(fileContent)
	except:
		content=[]

	return content
	
def ReadPlxList(file, url):
	UpdateFile(file, url)
	return ReadList(file)