import editor
from datetime import datetime

import praw
import urllib2

r = praw.Reddit(user_agent='GDTBot')
r.login('ZZZ', 'XXX')

# getting dirc
d = datetime.today()
url = "http://gd2.mlb.com/components/game/mlb/"
#url = url + "year_" + d.strftime("%Y") + "/month_" + d.strftime("%m") + "/day_" + d.strftime("%d") + "/"
url = url + "year_2015/month_03/day_18/"

reponse = urllib2.urlopen(url)
html = reponse.readlines()
directories = []
# print html
for v in html:
    #ENTER TEAM CODE HERE
    if "XXX" in v:
        v = v[v.index("\"") + 1:len(v)]
        v = v[0:v.index("\"")]
        directories.append(url + v)
title = editor.generatetitle(directories[0]);
sub = r.submit('XXX', title, editor.generatecode(directories[0]))
#sub = r.get_submission(submission_id='XXX')
