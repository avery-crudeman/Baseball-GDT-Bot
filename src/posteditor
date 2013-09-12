# does all the post generating and editing

import player

import xml.etree.ElementTree as ET
import urllib2
import simplejson as json
from datetime import datetime, timedelta
import time

from bs4 import BeautifulSoup
import re

def generatetitle(dir):
	title = "POST GAME THREAD: "
	while True:
		try:
			response = urllib2.urlopen(dir + "linescore.json")
			oresponse = urllib2.urlopen(dir + "boxscore.json")
			break
		except :
			print "Couldn't find file, trying again..."
			time.sleep(20)
	filething = json.load(response)
	ofilething = json.load(oresponse)
	game = filething.get('data').get('game')
	ogame = ofilething.get('data').get('boxscore')
	timestring = game.get('time_date') + " " + game.get('ampm')
	date_object = datetime.strptime(timestring, "%Y/%m/%d %I:%M %p")
	title = title + ogame.get('away_fname') + " (" + game.get('away_win') + "-" + game.get('away_loss') + ")"
	title = title + " @ "
	title = title + ogame.get('home_fname') + " (" + game.get('home_win') + "-" + game.get('home_loss') + ")"
	title = title + " - "
	title = title + date_object.strftime("%B %d, %Y")
	return title

def generatecode(dir):
	code = ""
	# files needed to download
	files = dict()
	dirs = []
	dirs.append(dir + "linescore.json")
	dirs.append(dir + "boxscore.json")
	dirs.append(dir + "gamecenter.xml")
	dirs.append(dir + "plays.json")
	dirs.append(dir + "/inning/inning_Scores.xml")
	files = downloadfiles(dirs)
	
	#generate post
	game = files["linescore"].get('data').get('game')
	code = code + generateheader(files)
	code = code + generateboxscore(files)
	code = code + generatelinescore(files)	
	code = code + generatescoringplays(files)
	if files["linescore"].get('data').get('game').get('status') == "Final":
		s = files["linescore"].get('data').get('game')
		code = code + "##FINAL: "
		if int(s.get("home_team_runs")) < int(s.get("away_team_runs")):
			code = code + s.get("away_team_runs") + "-" + s.get("home_team_runs") + " " + s.get("away_team_name")
			if game.get('home_team_name') == "Orioles":
				code = code + ". There is no joy in Mudville." + "\n"
				code = code + generatedecisions(files)
			else:
				code = code + " Magic (Feel It Happen)" + "\n"
				code = code + generatedecisions(files)
		elif int(s.get("home_team_runs")) > int(s.get("away_team_runs")):
			code = code + s.get("home_team_runs") + "-" + s.get("away_team_runs") + " " + s.get("home_team_name")
			if game.get('home_team_name') == "Orioles":
				code = code + " Magic (Feel It Happen)" + "\n"
				code = code + generatedecisions(files)
			else:
				code=code + ". There is no joy in Mudville." + "\n"
				code = code + generatedecisions(files)
		else:
			code = code + "SOMETHING WENT HORRIBLY WRONG"	
	if files["linescore"].get('data').get('game').get('status') == "Postponed":
		code = code + "###POSTPONED"
	return code

def downloadfiles(dirs):
	files = dict()
	while True:
		try:
			response = urllib2.urlopen(dirs[0])
			files["linescore"] = json.load(response)
			response = urllib2.urlopen(dirs[1])
			files["boxscore"] = json.load(response)
			response = urllib2.urlopen(dirs[2])
			files["gamecenter"] = ET.parse(response)
			response = urllib2.urlopen(dirs[3])
			files["plays"] = json.load(response)
			response = urllib2.urlopen(dirs[4])
			files["scores"] = ET.parse(response)					
			break
		except:
			print "Couldn't open file, retrying..."
			time.sleep(10)
	return files

def generateheader(files):
	header = ""
	game = files["linescore"].get('data').get('game')	
	ogame = files["boxscore"].get('data').get('boxscore')	
	timestring = game.get('time_date') + " " + game.get('ampm')
	date_object = datetime.strptime(timestring, "%Y/%m/%d %I:%M %p")
	t = timedelta(hours=0) #change depending on team, 0 for east, 1 for central, 2 for mountain, 3 for west coast
	timezone = "EST" #change this based on team too
	date_object = date_object - t
	weather = files["plays"].get('data').get('game').get('weather')
	teamflair = getteamflair(game.get('home_team_name'),game.get('away_team_name'))	
	subreddits = getsubreddits(game.get('home_team_name'),game.get('away_team_name'))	
	root = files["gamecenter"].getroot()
	broadcast = root.find('broadcast')
	notes = getnotes(game.get('home_team_name'),game.get('away_team_name'))
	today = datetime.today()
	request0 = urllib2.Request("http://www.mlb.com/pressbox_open/components/clubs/mc_archive_frame.jsp?c_id=" + notes[0] +"&assetlist=game-notes&list_year=" + today.strftime("%Y") + "&list_month=" + today.strftime("%m"))
	while True:
		try:	
			response0 = urllib2.urlopen(request0)
			soup0 = BeautifulSoup(response0)
			variable0=soup0.find('a', href=re.compile('^/documents/'))['href']
			break
		except:
			variable0 = "/404/"
			break
	request1 = urllib2.Request("http://www.mlb.com/pressbox_open/components/clubs/mc_archive_frame.jsp?c_id=" + notes[1] +"&assetlist=game-notes&list_year=" + today.strftime("%Y") + "&list_month=" + today.strftime("%m"))
	while True:
		try:	
			response1 = urllib2.urlopen(request1)
			soup1 = BeautifulSoup(response1)
			variable1=soup1.find('a', href=re.compile('^/documents/'))['href']
			break
		except:
			variable1 = "/404/"
			break	
	header = header + "\n##Purpose of this thread:\n"
	header = header + "* Discuss developing baseball action LIVE\n"
	header = header + "* Discuss the Orioles game\n"
	header = header + "* Post memes / images / gifs / information that may not deserve a front-page post of its own.\n"
	header = header + "* Discuss other stuff as long as it falls within our (admittedly vague) rules.\n"
	header = header + "* Nominate your Player of the Game (POTG). Upvote your choice if it's posted, or add your own!\n"
	header = header + "\n"	
	header = header + "##Links\n"	
	header = header + "|MLB|Fangraphs|Brooks Baseball|IRC Chat|Opponents|\n"
	header = header + "|:--:|:--:|:--:|:--:|:--:|\n"
	header = header + "[Gameday](http://mlb.mlb.com/mlb/gameday/index.jsp?gid=" + game.get('gameday_link') + ")|"
	header = header + " [Game Graph](http://www.fangraphs.com/livewins.aspx?date=" + date_object.strftime("%Y-%m-%d") + "&team=" + game.get('home_team_name') + "&dh=0&season=" + date_object.strftime("%Y") + ")|" 
	header = header + " [Strikezone Map](http://brooksbaseball.net/pfxVB/zoneTrack.php?month=" + date_object.strftime("%m") + "&day=" + date_object.strftime("%d") + "&year=" + date_object.strftime("%Y") + "&game=gid_" + game.get('gameday_link') + "%2F&prevDate=" + date_object.strftime("%m%d") + ")|"
	header = header + " [Freenode: #orioles](http://webchat.freenode.net/)|" 
	if game.get('home_team_name') == "Orioles": 
		header = header + subreddits[1]
	else:
		header = header + subreddits[0]
	header = header + "\n\n"
	header = header + "|[](" + teamflair[1] + ")|[](" + teamflair[0] + ")|\n"
	header = header + "|:--:|:--:|\n"
	header = header +  "[Game Notes](http://www.mlb.com" + variable1 + ")|[Game Notes](http://www.mlb.com" + variable0 + ")|"
	return header
		
def generateboxscore(files):
	boxscore = "\n##" + "Box Score" + "\n"
	homebatters = []; awaybatters = []
	homepitchers = []; awaypitchers = []
	game = files["boxscore"].get('data').get('boxscore')
	team = files["linescore"].get('data').get('game')
	teamflair = getteamflair(team.get('home_team_name'),team.get('away_team_name'))		
	batting = game.get('batting')
	for i in range(0,len(batting)):
		players = batting[i].get('batter')
		for b in range(0,len(players)):
			if players[b].get('bo') != None:
				if batting[i].get('team_flag') == "home":
					homebatters.append(player.batter(players[b].get('name'), players[b].get('pos'), players[b].get('ab'), players[b].get('r'), players[b].get('h'), players[b].get('rbi'), players[b].get('bb'), players[b].get('so'), players[b].get('avg'), players[b].get('id')))
				else:	
					awaybatters.append(player.batter(players[b].get('name'), players[b].get('pos'), players[b].get('ab'), players[b].get('r'), players[b].get('h'), players[b].get('rbi'), players[b].get('bb'), players[b].get('so'), players[b].get('avg'), players[b].get('id')))
	pitching = game.get('pitching')
	for i in range(0,len(pitching)):
		players = pitching[i].get('pitcher')
		if type(players) is list:
			for p in range(0,len(players)):
				if pitching[i].get('team_flag') == "home":
					homepitchers.append(player.pitcher(players[p].get('name'), players[p].get('out'), players[p].get('h'), players[p].get('r'), players[p].get('er'), players[p].get('bb'), players[p].get('so'), players[p].get('np'), players[p].get('s'), players[p].get('era'), players[p].get('note'), players[p].get('id')))
				else:
					awaypitchers.append(player.pitcher(players[p].get('name'), players[p].get('out'), players[p].get('h'), players[p].get('r'), players[p].get('er'), players[p].get('bb'), players[p].get('so'), players[p].get('np'), players[p].get('s'), players[p].get('era'), players[p].get('note'), players[p].get('id')))
		elif type(players) is dict:
			if pitching[i].get('team_flag') == "home":
				homepitchers.append(player.pitcher(players.get('name'), players.get('out'), players.get('h'), players.get('r'), players.get('er'), players.get('bb'), players.get('so'), players.get('np'), players.get('s'), players.get('era'), players.get('note'), players.get('id')))
			else:
				awaypitchers.append(player.pitcher(players.get('name'), players.get('out'), players.get('h'), players.get('r'), players.get('er'), players.get('bb'), players.get('so'), players.get('np'), players.get('s'), players.get('era'), players.get('note'), players.get('id')))
	while len(homebatters) < len(awaybatters):
		homebatters.append(player.batter())
	while len(awaybatters) < len(homebatters):
		awaybatters.append(player.batter())
	while len(homepitchers) < len(awaypitchers):
		homepitchers.append(player.pitcher())
	while len(awaypitchers) < len(homepitchers):
		awaypitchers.append(player.pitcher())
	boxscore = boxscore + "\n"
	boxscore = boxscore + "[](" + teamflair[1] + ")|Pos|AB|R|H|RBI|BB|SO|BA|"
	boxscore = boxscore + "[](" + teamflair[0] + ")|Pos|AB|R|H|RBI|BB|SO|BA|"
	boxscore = boxscore + "\n"
	boxscore = boxscore + ":--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|"
	boxscore = boxscore + ":--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|"
	boxscore = boxscore + "\n"
	for i in range(0,len(homebatters)):
		boxscore = boxscore + str(awaybatters[i]) + "|" + str(homebatters[i]) + "\n"
	boxscore = boxscore + "\n" + "Pitchers|IP|H|R|ER|BB|SO|P-S|ERA|"
	boxscore = boxscore + "Pitchers|IP|H|R|ER|BB|SO|P-S|ERA|"
	boxscore = boxscore + "\n"
	boxscore = boxscore + ":--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|"
	boxscore = boxscore + ":--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|"
	boxscore = boxscore + "\n"
	for i in range(0,len(homepitchers)):
		boxscore = boxscore + str(awaypitchers[i]) + "|" + str(homepitchers[i]) + "\n"
	boxscore = boxscore + "\n\n"
	return boxscore	

def generatelinescore(files):
	linescore = "\n##Line Score\n"
	game = files["linescore"].get('data').get('game')
	teamflair = getteamflair(game.get('home_team_name'),game.get('away_team_name'))		
	lineinfo = game.get('linescore')
	innings = len(lineinfo) if len(lineinfo) > 9 else 9
	curinning = len(lineinfo)
	linescore = linescore + " |"
	for i in range(1, innings+1):
		linescore = linescore + "**" + str(i) + "**|"
	linescore = linescore + "**R**|**H**|**E**\n"
	for i in range(0, innings+4):
		linescore = linescore + ":--:|"
	linescore = linescore + "\n" + "[](" + teamflair[1] + ")" + "|"
	x = 1
	if type(lineinfo) is list:
		for v in lineinfo:
			linescore = linescore + v.get('away_inning_runs') + "|"
			x = x + 1
	elif type(lineinfo) is dict:
		linescore = linescore + lineinfo.get('away_inning_runs') + "|"
		x = x + 1
	for i in range(x, innings+1):
		linescore = linescore + "|"
	linescore = linescore + game.get('away_team_runs') + "|" + game.get('away_team_hits') + "|" + game.get('away_team_errors')
	linescore = linescore + "\n" + "[](" + teamflair[0] + ")" "|"
	x = 1
	if type(lineinfo) is list:
		for v in lineinfo:
			linescore = linescore + v.get('home_inning_runs') + "|"
			x = x + 1
	elif type(lineinfo) is dict:
		linescore = linescore + lineinfo.get('home_inning_runs') + "|"
		x = x + 1
	for j in range(x, innings+1):
		linescore = linescore + "|"
	linescore = linescore + game.get('home_team_runs') + "|" + game.get('home_team_hits') + "|" + game.get('home_team_errors')
	linescore = linescore + "\n\n"
	return linescore	
	
def generatescoringplays(files):
	scoringplays = " "
	root = files["scores"].getroot()
	game = files["linescore"].get('data').get('game')
	teamflair = getteamflair(game.get('home_team_name'),game.get('away_team_name'))		
	scores = root.findall("score")
	currinning = ""
	inningcheck = ""
	scoringplays = scoringplays + "\n##Scoring Plays\n"
	scoringplays = scoringplays + "Inning|Play|Score\n"
	scoringplays = scoringplays + ":--:|:--|:--:\n"

	for s in scores:
		if s.get("top_inning") == "Y":
			inningcheck = "Top "
		else:
			inningcheck = "Bottom "
		inningcheck = inningcheck + s.get("inn") + "|"
		if inningcheck != currinning:
			currinning = inningcheck
			scoringplays = scoringplays + currinning
		else:
			scoringplays = scoringplays + " |"
		
		actions = s.findall("action")	
		if s.find('atbat').get('score') == "T":
			while True:
				try:
					scoringplays = scoringplays + s.find('atbat').get('des')
					break
				except:
					scoringplays = scoringplays + "No description currently available"
					break
		elif actions[len(actions)-1].get("score") == "T":	
			while True:
				try:
					scoringplays = scoringplays + actions[len(actions)-1].get("des")
					break
				except:
					scoringplays = scoringplays + "No description currently available"
					break
		else:		
			scoringplays = scoringplays + s.get("pbp")	
		
		scoringplays = scoringplays + "|"	
		if int(s.get("home")) < int(s.get("away")):
			scoringplays = scoringplays + s.get("away") + "-" + s.get("home") + " " + "[](" + teamflair[1] + ")"
		elif int(s.get("home")) > int(s.get("away")):
			scoringplays = scoringplays + s.get("home") + "-" + s.get("away") + " " + "[](" + teamflair[0] + ")"
		else:
			scoringplays = scoringplays + s.get("home") + "-" + s.get("away") + " Tied"
		scoringplays = scoringplays + "\n"
	scoringplays = scoringplays + "\n"
	scoringplays = scoringplays + "\n"
	return scoringplays			
	
def generatedecisions(files):	
	decisions = "\n"
	homepitchers = []; awaypitchers = []
	game = files["boxscore"].get('data').get('boxscore')
	team = files["linescore"].get('data').get('game')
	teamflair = getteamflair(team.get('home_team_name'),team.get('away_team_name'))	
	pitching = game.get('pitching')	
	for i in range(0,len(pitching)):
		players = pitching[i].get('pitcher')
		if type(players) is list:
			for p in range(0,len(players)):
				if pitching[i].get('team_flag') == "home":
					homepitchers.append(player.decision(players[p].get('name'), players[p].get('note'), players[p].get('id')))
				else:
					awaypitchers.append(player.decision(players[p].get('name'), players[p].get('note'), players[p].get('id')))
		elif type(players) is dict:
			if pitching[i].get('team_flag') == "home":
				homepitchers.append(player.decision(players.get('name'), players.get('note'), players.get('id')))
			else:
				awaypitchers.append(player.decision(players.get('name'), players.get('note'), players.get('id')))
	decisions = decisions + "|Decisions|" + "\n"	
	decisions = decisions + "|:--:|" + "\n"	
	decisions = decisions + "|" + "[](" + teamflair[1] + ")" 
	for i in range(0,len(awaypitchers)):	
		decisions = decisions + str(awaypitchers[i]) + " "
	decisions = decisions + "\n" + "|" + "[](" + teamflair[0] + ")" 
	for i in range(0,len(homepitchers)):	
		decisions = decisions + str(homepitchers[i])
	decisions = decisions + "\n\n"
	return decisions

def getsubreddits(homename, awayname):
	subreddits = []
	options = {
		"Twins" : "/r/minnesotatwins",
		"White Sox" : "/r/WhiteSox",
		"Tigers" : "/r/MotorCityKitties",
		"Royals" : "/r/KCRoyals",
		"Indians" : "/r/WahoosTipi",
		"Rangers" : "/r/TexasRangers",
		"Astros" : "/r/Astros",
		"Athletics" : "/r/OaklandAthletics",
		"Angels" : "/r/AngelsBaseball",
		"Mariners" : "/r/Mariners",
		"Red Sox" : "/r/RedSox",
		"Yankees" : "/r/NYYankees",
		"Blue Jays" : "/r/TorontoBlueJays",
		"Rays" : "/r/TampaBayRays",
		"Orioles" : "/r/Orioles",
		"Cardinals" : "/r/Cardinals",
		"Reds" : "/r/Reds",
		"Pirates" : "/r/Buccos",
		"Cubs" : "/r/Cubs",
		"Brewers" : "/r/Brewers",
		"Giants" : "/r/SFGiants",
		"Diamondbacks" : "/r/azdiamondbacks",
		"D-backs" : "/r/azdiamondbacks",		
		"Rockies" : "/r/ColoradoRockies",
		"Dodgers" : "/r/Dodgers",
		"Padres" : "/r/Padres",
		"Phillies" : "/r/Phillies",
		"Mets" : "/r/NewYorkMets",
		"Marlins" : "/r/letsgofish",
		"Nationals" : "/r/Nationals",
		"Braves" : "/r/Braves"
	}
	subreddits.append(options[homename])
	subreddits.append(options[awayname])
	return subreddits
	
def getteamflair(homename, awayname):
	teamflair = []
	options = {
		"Twins" : "/MIN",
		"White Sox" : "/CHW",
		"Tigers" : "/DET",
		"Royals" : "/KCR",
		"Indians" : "/CLE1",
		"Rangers" : "/TEX",
		"Astros" : "/HOU2",
		"Athletics" : "/OAK1",
		"Angels" : "/LAA",
		"Mariners" : "/SEA",
		"Red Sox" : "/BOS",
		"Yankees" : "/NYY",
		"Blue Jays" : "/TOR2",
		"Rays" : "/TBR",
		"Orioles" : "/BAL2",
		"Cardinals" : "/STL",
		"Reds" : "/CIN",
		"Pirates" : "/PIT",
		"Cubs" : "/CHI",
		"Brewers" : "/MIL",
		"Giants" : "/SFG1",
		"Diamondbacks" : "/ARI2",
		"D-backs" : "/ARI2",			
		"Rockies" : "/COL",
		"Dodgers" : "/LAD",
		"Padres" : "/SD1",
		"Phillies" : "/PHI",
		"Mets" : "/NYM",
		"Marlins" : "/MIA",
		"Nationals" : "/WAS",
		"Braves" : "/ATL"
	}
	teamflair.append(options[homename])
	teamflair.append(options[awayname])
	return teamflair	
	
def getnotes(homename, awayname):
	notes = []
	options = {
		"Twins" : "min",
		"White Sox" : "cws",
		"Tigers" : "det",
		"Royals" : "kc",
		"Indians" : "cle",
		"Rangers" : "tex",
		"Astros" : "hou",
		"Athletics" : "oak",
		"Angels" : "ana",
		"Mariners" : "sea",
		"Red Sox" : "bos",
		"Yankees" : "nyy",
		"Blue Jays" : "tor",
		"Rays" : "tb",
		"Orioles" : "bal",
		"Cardinals" : "stl",
		"Reds" : "cin",
		"Pirates" : "pit",
		"Cubs" : "chc",
		"Brewers" : "mil",
		"Giants" : "sf",
		"Diamondbacks" : "ari",
		"D-backs" : "ari",			
		"Rockies" : "col",
		"Dodgers" : "la",
		"Padres" : "sd",
		"Phillies" : "phi",
		"Mets" : "nym",
		"Marlins" : "mia",
		"Nationals" : "was",
		"Braves" : "atl"
	}
	notes.append(options[homename])
	notes.append(options[awayname])
	return notes	
