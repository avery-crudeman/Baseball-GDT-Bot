import player, editor, posteditor
from datetime import datetime
import timecheck
import time

import praw
import urllib2
import simplejson as json
        
r = praw.Reddit(user_agent='/u/avery_crudeman fork of Game Discission Thread Generator Bot by /u/DetectiveWoofles') 
r.login('USERNAME', 'PASSWORD')

while True:
        today = datetime.today()
        
        # getting dirc
        url = "http://gd2.mlb.com/components/game/mlb/"
        url = url + "year_" + today.strftime("%Y") + "/month_" + today.strftime("%m") + "/day_" + today.strftime("%d") + "/"

        response = ""
        while not response:
                try:
                        response = urllib2.urlopen(url)
                except:
                        print "Couldn't find URL, trying again..."
                        time.sleep(20)

        html = response.readlines()
        directories = []
        for v in html:
                if "kcamlb" in v:
                # POSTSEASON GAMES NEED THE FULL TEAM CODES        
                #if "kcamlb_balmlb" in v:
                        v = v[v.index("\"")+1:len(v)]
                        v = v[0:v.index("\"")]
                        directories.append(url + v)
                        
        for d in directories:
                timecheck.gamecheck(d)
                title = editor.generatetitle(d)
                if not timecheck.ppcheck(d):
                        while True:
                                check = datetime.today()
                                try:
                                        print "Submitting game thread..."
                                        sub = r.submit('SUBREDDIT', title, editor.generatecode(d))
                                        print "Game thread submitted..."
                                        print "Sleeping for two minutes..."
                                        print datetime.strftime(check, "%d %I:%M %p")
                                        time.sleep(120)                                 
                                        break
                                except Exception, err:
                                        print err
                                        time.sleep(300)
                        while True:
                                check = datetime.today()
                                str = editor.generatecode(d)
                                while True:
                                        try:
                                                sub.edit(str)
                                                print "Edits submitted..."
                                                print "Sleeping for two minutes..."
                                                print datetime.strftime(check, "%d %I:%M %p")
                                                time.sleep(120)
                                                break
                                        except Exception, err:
                                                print "Couldn't submit edits, trying again..."
                                                print datetime.strftime(check, "%d %I:%M %p")
                                                time.sleep(10)
                                if "|Decisions|" in str:
                                        check = datetime.today()
                                        print datetime.strftime(check, "%d %I:%M %p")
                                        print "Submitting postgame thread..."                           
                                        posttitle = posteditor.generatetitle(d)
                                        sub = r.submit('SUBREDDIT', posttitle, posteditor.generatecode(d))
                                        print "Postgame thread submitted..."                                    
                                        break                                           
                                elif "##POSTPONED" in str:
                                        check = datetime.today()
                                        print datetime.strftime(check, "%d %I:%M %p")
                                        print "Game postponed..."
                                        break
                                elif "##SUSPENDED" in str:
                                        check = datetime.today()
                                        print datetime.strftime(check, "%d %I:%M %p")
                                        print "Game suspended..."
                                        break                                
                                time.sleep(10)
        if datetime.today().day == today.day:
                timecheck.endofdaycheck()
