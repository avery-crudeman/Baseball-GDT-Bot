import editor
from datetime import datetime
import timecheck
import time

import praw
import urllib2

r = praw.Reddit(user_agent='GDTBot')
#r.login('username', 'password')
r.login('XXX', 'XXX')

while True:
    today = datetime.today()

    # getting dirc
    url = "http://gd2.mlb.com/components/game/mlb/"
    url = url + "year_" + today.strftime("%Y") + "/month_" + today.strftime("%m") + "/day_" + today.strftime("%d") + "/"

    # UNCOMMENT FOR TESTING PURPOSES ONLY
    #url = url + "year_2014" + "/month_03" + "/day_31/"

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
        #ENTER TEAM CODE HERE
        if "XXX" in v:
            v = v[v.index("\"") + 1:len(v)]
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
                    #ENTER SUBREDDIT NAME HERE
                    sub = r.submit('XXX', title, editor.generatecode(d))
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
                    print "Game final..."
                    print "Submitting postgame thread..."
                    posttitle = editor.generateposttitle(d)
                    #ENTER SUBREDDIT NAME HERE
                    sub = r.submit('XXX', posttitle, editor.generatecode(d))
                    print "Postgame thread submitted..."
                    break
                elif "##FINAL: TIE" in str:
                    check = datetime.today()
                    print datetime.strftime(check, "%d %I:%M %p")
                    print "Game final (tie)..."
                    print "Submitting postgame thread..."
                    posttitle = editor.generateposttitle(d)
                    #ENTER SUBREDDIT NAME HERE
                    sub = r.submit('XXX', posttitle, editor.generatecode(d))
                    print "Postgame thread submitted..."
                    break
                elif "##POSTPONED" in str:
                    check = datetime.today()
                    print datetime.strftime(check, "%d %I:%M %p")
                    print "Game postponed..."
                    print "Submitting postgame thread..."
                    posttitle = editor.generateposttitle(d)
                    #ENTER SUBREDDIT NAME HERE
                    sub = r.submit('XXX', posttitle, editor.generatecode(d))
                    print "Postgame thread submitted..."
                    break
                elif "##SUSPENDED" in str:
                    check = datetime.today()
                    print datetime.strftime(check, "%d %I:%M %p")
                    print "Game suspended..."
                    print "Submitting postgame thread..."
                    posttitle = editor.generateposttitle(d)
                    #ENTER SUBREDDIT NAME HERE
                    sub = r.submit('XXX', posttitle, editor.generatecode(d))
                    print "Postgame thread submitted..."
                    break
                time.sleep(10)
    if datetime.today().day == today.day:
        timecheck.endofdaycheck()
