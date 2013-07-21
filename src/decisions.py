import math

class decisions:
  	
	def __init__(self, name="", note="", id=""):
		self.name = name
		self.note = note
		self.id = id
		
	def __str__(self):
		s = " "
		ip = ""
		ps = ""
		if self.id != "":
			ip = str(math.floor((float(self.o)/3.0)*10)/10)
			s = "[" + str(self.name) + "](http://mlb.mlb.com/team/player.jsp?player_id=" + str(self.id) + ")"
			ps = str(self.p) + "-" + str(self.s)
		s = s + "|" + str(self.note) + "|"
		return s
