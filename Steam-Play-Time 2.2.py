#-------------------------Configuration----------------------------
Example = "11111111111111111"
Example2 = "11111111111124212"

targets = [Example, Example2]
targetNames = ["Example", "Example2"]

API_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

#-------------Instructions on finding and adding friends--------------
#Find a list of all of your friends' steam IDs by using this url and replacing the X's with your 64bit ID
#http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX&steamid=XXXXXXXXXXXXXXXXX&relationship=friend
#Find out which friend goes to which ID by entering it in on https://steamidfinder.ru/
#
#Add a friend into the script by entering their steam ID into "targets" and their name into the same spot in "targetNames"

#-----------------------------Code----------------------------------
import urllib2
import json
import os
import msvcrt
import re
from string import capwords
clear = lambda: os.system('cls')

def init():
	print "Display stats for which user?"
	for i in range(len(targets)):
		print i, "-", targetNames[i]
	print
	return input("Index: ")

def get_next_keypress():
	while 1:
		if msvcrt.kbhit():                  # Key pressed?
			a = ord(msvcrt.getch())         # get first byte of keyscan code  
			if a == 0 or a == 224:          # is it a function key?
				b = ord(msvcrt.getch())     # get next byte of key scan code
				x = a + (b*256)             # cook it.
				return x                    # return cooked scancode
			else:
				return a                    # else return ascii code

def print_top_played(index):
	response = urllib2.urlopen('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='+API_key+'&steamid='+targets[index]+'&include_appinfo=1&format=json')
	stats = json.loads(response.read())

	total = 0
	for game in stats["response"]["games"]:
		total += game["playtime_forever"]

	games = stats["response"]["games"]
	games = sorted(games, key=lambda game: game["playtime_forever"], reverse=True)
	
	print "Displaying stats for: " + targetNames[index]
	print str(total/60/24), "Days,", str(total / 60 % 24), "Hours,", str(total%60), "Minutes"
	print
	print "                           --All Time--"
	print
	for i in range(5):
		rank = i + 1;
		name = games[i]['name']
		hours = games[i]['playtime_forever'] / 60
		minutes = games[i]['playtime_forever'] % 60
		play_time = str(hours) + ":" + str(minutes).zfill(2)
		two_weeks = ""
		if 'playtime_2weeks' in games[i]:
			hours2 = str(games[i]['playtime_2weeks'] / 60).zfill(1)
			minutes2 = str(games[i]['playtime_2weeks'] % 60).zfill(2)
			two_weeks = "+" + hours2 + ":" + minutes2
		
		print str(rank).rjust(2), "-",
		try:
			print name.ljust(52), play_time.rjust(8), two_weeks.rjust(9)
		except:
			print re.sub('[^A-Za-z0-9\s:]+', '', name).ljust(52), play_time.rjust(8), two_weeks.rjust(9)

def print_two_weeks(index):
	response = urllib2.urlopen('http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key='+API_key+'&steamid='+targets[index]+'&format=json')
	stats = json.loads(response.read())

	if "games" not in stats["response"]:
		return
	
	games = stats["response"]["games"]
	games = sorted(games, key=lambda game: game['playtime_2weeks'], reverse=True)

	print
	print "                        --Last Two Weeks--"
	print
	for i in range(len(games)):
		rank = str(i + 1);
		name = games[i]['name']
		hours = games[i]['playtime_2weeks'] / 60
		minutes = games[i]['playtime_2weeks'] % 60
		two_weeks = str(hours).zfill(1) + ":" + str(minutes).zfill(2)
		
		print rank.rjust(2), "-",
		try:
			print name.ljust(52), two_weeks.rjust(8)
		except:
			print re.sub('[^A-Za-z0-9\s:]+', '', name).ljust(52), two_weeks.rjust(8)
				
def dict_search(key, list):
	index = 0;
	for game in list:
		if game['name'] == key:
			return index;
		else:
			index += 1
	return False
	
def print_all_recent():
	list = []
	
	for i in range(len(targets)):
		response = urllib2.urlopen('http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key='+API_key+'&steamid='+targets[i]+'&format=json')
		stats = json.loads(response.read())
		
		if "games" in stats["response"]:
			games = stats["response"]["games"]
	
			for j in range(len(games)):
				result = dict_search(games[j]['name'], list)
				if result is False:
					list.append({"name" : games[j]['name'], "time" : games[j]['playtime_2weeks'], "friends" : 1})
				else:
					list[result]['time'] += games[j]['playtime_2weeks']
					list[result]['friends'] += 1
		
	print "Displaying stats for all configured users:"
	print
	print "                    --Top Games Played by Friends--"
	print
	list = sorted(list, key=lambda game: game['time'], reverse=True)
	
	i = 1
	for game in list:
		print str(i).rjust(2), "-",
		try:
			print game['name'].ljust(52), (str(game['time']/60) + ":" + str(game['time']%60).zfill(2)).rjust(8), str(game['friends']).rjust(8)
		except:
			print re.sub('[^A-Za-z0-9\s:]+', '', game['name']).ljust(52), (str(game['time']/60) + ":" + str(game['time']%60).zfill(2)).rjust(8), str(game['friends']).rjust(8)
		i += 1
		
	print ""
	print ""
	print ""
	print "See player's stats".rjust(20)
	print "<<<<".rjust(13)

def printMain(choice):
	print_top_played(choice)
	print_two_weeks(choice)
	print ""
	print ""
	print ""
	print "Back to selection".rjust(19), "See friends' stats".rjust(58)
	print "<<<<".rjust(12), ">>>>".rjust(58)
	
		
choice = init()
clear()
printMain(choice)

left = 19424
right = 19936

screen = 2;

def navLeft():
	global screen
	global choice
	if screen == 1:
		return
	if screen == 2:
		clear()
		choice = init()
		clear()
		printMain(choice)
	if screen == 3:
		clear()
		printMain(choice)
		screen = 2
		
def navRight():
	global screen
	if screen == 1:
		return
	if screen == 2:
		clear()
		print_all_recent()
		screen = 3
	if screen == 3:
		return

while 1:
	keypress = get_next_keypress()
	if keypress == right:
		navRight()
	if keypress == left:
		navLeft()


raw_input()
