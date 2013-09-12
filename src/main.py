import player, editor, posteditor
from datetime import datetime
import timecheck
import time

import praw
import urllib2
import simplejson as json
	
r = praw.Reddit(user_agent='Game Discission Thread Generator Bot by /u/DetectiveWoofles') 
r.login('xxx', 'xxx')

while True:
	
	# getting dirc
	today = datetime.today()
	url = "http://gd2.mlb.com/components/game/mlb/"
	url = url + "year_" + today.strftime("%Y") + "/month_" + today.strftime("%m") + "/day_" + today.strftime("%d") + "/"
	
	# UNCOMMENT FOR TESTING PURPOSES ONLY
	#url = url + "year_2013" + "/month_08" + "/day_12/"

	response = ""
	while not response:
		try:
			response = urllib2.urlopen(url)
		except:
			print "Couldn't find file, trying again..."
			time.sleep(20)

	html = response.readlines()
	directories = []
	for v in html:
		if "balmlb" in v:
			v = v[v.index("\"")+1:len(v)]
			v = v[0:v.index("\"")]
			directories.append(url + v)
			
	for d in directories:
		timecheck.gamecheck(d)
		title = editor.generatetitle(d)
		if not timecheck.ppcheck(d):
			while True:
				try:
					print "Submitting game thread..."
					sub = r.submit('SUBREDDITNAME', title, editor.generatecode(d))
					#sub = r.get_submission(submission_id='xxxxxx')
					print "Game thread submitted..."
					break
				except Exception, err:
					print err
					time.sleep(300)
			while True:
				str = editor.generatecode(d)
				while True:
					try:
						sub.edit(str)
						break
					except Exception, err:
						print "Couldn't submit edits, trying again..."
						time.sleep(10)
				if "|Decisions|" in str:
					print "Submitting postgame thread..."				
					posttitle = posteditor.generatetitle(d)
					sub = r.submit('SUBREDDITNAME', posttitle, posteditor.generatecode(d))
					print "Postgame thread submitted..."					
					break						
				elif "###POSTPONED" in str:
					break
				time.sleep(10)
	if datetime.today().day == today.day:
		timecheck.endofdaycheck()
