#!/usr/bin/env python

from slackclient import SlackClient
from time import sleep
import requests
import random
import json
# import jelly

slack_token = "[SLACK KEY]" #You will need to add your own slack key/token
sc = SlackClient(slack_token)

botname = "[BOT NAME]" #Also this might be different with a different token so you will need to see what the bots user ID is
channel = ""
channeltype = ""
user = ""
msgtime = ""
text = ""

phase = ""
playing = 0
players = []
channelsplaying = {}
characters = {}
party = {}
creating = []
battlefield = {'monster': {}, 'player': {}}
fighter = {'class': "Fighter",
           'level': 1,
            'exp': 0,
            'hp': 15,
            'stm': 10,
            'mp': 0,
            'stats': {'str': 3, 'dex': 1, 'int': 1},
            'skills': {'bash': {'stm': 2, 'dmg': 2, 'dmgtype': "Slash"}
                       },
            'inventory': {'coins': 0, 'potion': 1},
           'location': "Starting Area",
           'combat': False
           }
ranger = {'class': "Ranger",
          'level': 1,
          'exp': 0,
          'hp': 10,
          'stm': 5,
          'mp': 5,
          'stats': {'str': 2, 'dex': 2, 'int': 1},
          'skills': {'Aim': {'stm': 3, 'dmg': 2, 'dmgtype': "Piercing"},
                     'Roots': {'mp': 2, 'status': "Paralyze"}
                     },
          'inventory': {'coins': 0, 'potion': 1},
           'location': "Starting Area",
           'combat': False}
mage = {'class': "Mage",
        'level': 1,
        'exp': 0,
        'hp': 5,
        'stm': 0,
        'mp': 10,
        'stats': {'str': 1, 'dex': 1, 'int': 3},
        'skills': {'Fire Bolt': {'mp': 2, 'dmg': 1, 'dmgtype': "Fire"},
                   'Ice Dart': {'mp': 2, 'dmg': 1, 'dmgtype': "Ice"},
                   'Lightning Bolt': {'mp': 2, 'dmg': 1, 'dmgtype': "Lightning"}
                   },
        'inventory': {'coins': 0, 'potion': 1},
        'location': "Starting Area",
        'combat': False}
itemdb = {'potion': {'coins': 5, 'hp': 5}}
monsterdb = {'slime': {'level': 1, 'exp': 10, 'hp': 5, 'stats': {'str': 1, 'dex': 1, 'int': 1}, 'inventory': {'coins': 2, 'potion': 1}}}

alreadysentvideo = []


delayedmessage = []

validterm = ["dingus", "nub", "tubebed"]
helpterm = ["what", "you", "do", "can"]
responses = ["I know now why you cry.",
             "Tis, but a scratch!",
             "42",
             "Wait who farted?",
             "Don't rope me into this",
             "Wait a minute",
             "Next in line",
             "Lyf is but a Mustardsack"]
look = ["show", "top", "bottom",
        "agency", "customers", "add",
        "subtract", "keepit","hello",
        "movie", "whoareyou", "mustard",
        "mustards",
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]


#
# Sends a message from the list of messages every second
#
def delay_send():
    if len(delayedmessage) == 0:
        return
    else:
        print("Number of Messages: %d" % len(delayedmessage))
        for i in range(len(delayedmessage)):
            custommessage(delayedmessage[i]['channel'], delayedmessage[i]['text'], delayedmessage[i]['type'])
            sleep(1)
    delayedmessage.clear()


#
# Adds a message to the Delay array to be sent using the delay_send function
#
def add_message(c, m, t):
    print("Message Added")
    delayedmessage.append({'channel': c, 'text': m, 'type': t})


#
# Custom Formatting for the messages sent from delay_send function
#
def custommessage(ch, msg, type):
    if type == "g":
        icon = "http://img.memecdn.com/first-time-being-a-game-master-need-help-post-ideas-and-tips-in-comments-pls_fb_5912303.jpg"
        name = "Game Master"
    elif type == "s":
        icon = "https://pbs.twimg.com/profile_images/498006663987601408/gF4SJw82_400x400.jpeg"
        name = "SacLyf"
    elif type == "r":
        icon = "https://thumbs.dreamstime.com/z/golden-mustard-sack-bag-over-white-background-44171822.jpg"
        name = "SacLyf"
    elif type == "a":
        icon = "https://i.ytimg.com/vi/2a8rT-p2r50/maxresdefault.jpg"
        name = "Hey Now!"
    else:
        icon = "http://www.tshirtvortex.net/wp-content/uploads/Robot-Tacos-T-Shirt-sq.jpg"
        name = "Tacobot"
    print("Sending message")
    sc.api_call("chat.postMessage", channel=ch, text=msg, username=name, icon_url=icon, markdwn="true")


#
# Returns a string and your name
#
def showname(x):
    return "You are " + x


#
# Sends a message that is passed through to the channel it was requested from
#
def sm(x):
    sc.rtm_send_message(channel, x)


#
# Requests from the link below to get search results from Open Movie Database
# Still needs work(It is working, but not done yet)
# Using the following link https://www.omdbapi.com/
#
def movie(title=None, type=None, year=None):
    url = "http://www.omdbapi.com/?"
    if title is not None:
        url = url + "t=" + title + "&"
    if type is not None and type == "movie" or type == "series" or type == "episode":
        url = url + "type=" + type + "&"
    if year is not None and len(year) == 4:
        url = url + "y=" + year + "&"
    response = requests.get(url)
    if str(response) == "<Response [200]>":
        md = response.json()
        print(md)
        if md['Response'] == "True":
            a = ""
            for results in md:
                a = a + "Title: " + results['Title'] + \
                    "\nYear: " + results['Year'] + \
                    "\nRated: " + results['Rated'] + \
                    "\nReleased: " + results['Released'] + \
                    "\nRuntime: " + results['Runtime'] + \
                    "\nGenre: " + results['Genre'] + \
                    "\nDirector: " + results['Director'] + \
                    "\nPlot: " + results['Plot'] + "\n\n"
            return a
        else:
            return "No results"
    else:
        return "Could not Connect or Couldn't find anything"

#
# Function for Sending a formatted version
# of the text put in
# Formatting: postm Hello
#
def postm(c, x):
    icon = "http://0.media.collegehumor.cvcdn.com/a/c/collegehumor.14e9a8ba1f191d64f8172d0c059a212c.jpg"
    name = "Game Master"
    sc.api_call("chat.postMessage", channel=c, text=x, username=name, icon_url=icon, markdwn="true")


#
# Condense this into random response function or move all other response into this function
#
def respond(text):
        if text[0] == "add" or text[0] == "subtract":
            if len(text) == 3:
                return simplemath(text[0], int(text[1]), int(text[2]))
            else:
                return "Please user numbers 0 - 9 and make sure you have 2 numbers"
        elif "mustard" in text or "mustards" in text:
            return "Whatever it is, keep it in a sack, because food can be everything."
        elif "who" in text and "are" in text and "you" in text:
            return whoareyou()
        elif text[0] == "keepit" or "keep" in text and "it" in text:
            return ":krank:"
        elif text[0] == "hello":
            return "Hello, pleasure to meet you " + "<@" + user + ">"
        elif text[0] == "ml":
            if len(text) == 4:
                return movie(text[1], text[2], text[3])
            else:
                return "Please format as follows: ML TITLE TYPE YEAR"
        else:
            return "I don't think I understand, Please try again"


#
# Basic Addition function just a practice function
#
def simplemath(t1, n1, n2):
    if t1 == "add":
        n = n1 + n2
        return "Added your numbers and got: %d" % n
    elif t1 == "subtract":
        n = n1 - n2
        return "Subtracted your numbers and got: %d" % n
    else:
        return "Please try again"


#
# Explains what this is
#
def whoareyou():
    return "I am a work in progress, can't do much yet, " \
           "still being debugged to make sure there are not instances where I will stop working."


#
# Function for Creating a character
# Allows the user to select from 1 of 3 Classes
#
def create_character(c, u, x):
    state = checkstate(u)
    if state == "creating":
        if "fighter" in x or "ranger" in x or "mage" in x:
            if "fighter" in x:
                characters[u] = fighter
            elif "ranger" in x:
                characters[u] = ranger
            elif "mage" in x:
                characters[u] = mage
            creating.remove(u)
            print(characters)
            add_message(c, "<@" + u + "> the " + characters[u]["class"] +
                        " Level " + str(characters[u]['level']) + " Has joined the game", "g")
        else:
            add_message(c, "Please choose from one of the three: Fighter, Ranger, or Mage", "g")
    elif state == "create":
        creating.append(u)
        add_message(c, "<@%s> What character do you want? Fighter, Ranger, Mage\n "
                       "To choose a character just mention my name and type 'choose fighter'" % u, "g")
    elif state == "ready":
        print("You have already created a character")
    else:
        print("Please make a character, but make sure you joined the game")


#
# Checks to see what State the player is in,
# if they have or have not created a character yet
#
def checkstate(u):
    if u in players:
        if u in creating:
            print("In the process of making a character")
            return "creating"
        if u in characters:
            print("User has a character")
            return "ready"
        else:
            print("Make a character")
            return "create"
    else:
        return "skip"


#
# Joins or starts the game
# If the user is already playing then it sends a message
# telling them that they are already playing the game
#
def join(c, u, x):
    if u in players:
        print("Player is already in game")
        add_message(c, "<@%s> is already in the game" % u, "g")
    else:
        players.append(u)
        check_channel(c, u)
        state = checkstate(u)
        print("User has been added to the game")
        if state == "create":
            create_character(c, u, x)
        elif state == "ready":
            sleep(1)
            add_message(c, "<@" + u + "> the " + characters[u]["class"] + " Level " +
                    str(characters[u]['level']) + " Has joined the game", "g")


#
# Checks to see what channel a player joined from
#
def check_channel(c, u):
    if c in channelsplaying:
        print("Channel is already in list")
        if u in channelsplaying[c]:
            print("User: %s is already in Channel: %s" % (u, c))
        else:
            print("Adding User: %s to Channel: %s" % (u, c))
            channelsplaying[c].append(u)
    else:
        print("Channel has joined game: " + c)
        channelsplaying[c] = []
        channelsplaying[c].append(u)


#
# Function to leave the game,
# if the user is in a batter then the user has to finish the battle before leaving
#
def leavegame(c, u):
    if u in players:
        if characters[u]['combat'] == False:
            players.remove(u)
            print("User has left")
            if c in channelsplaying:
                print("Channel is in list of channels")
                if u in channelsplaying[c]:
                    print("User in channel")
                    channelsplaying[c].remove(u)
            add_message(c, "<@%s> has left the game" % u, "g")
        else:
            add_message(c, "Please make sure you are not in combat before leaving.", "g")
    else:
        print("User does not exist")
    print(players)
    print(channelsplaying)


#
# Function for Generating a battle,
# getting the players and monsters
#
def generate_battle(n, u):
    global battlefield
    for i in range(n):
        battlefield['monster']['slime' + str(int(i) + 1)] = \
            monsterdb['slime']
        print("added slime")
        battlefield['monster']['slime' + str(int(i) + 1)]['init'] = \
            random.randint(0, 10) + int(battlefield['monster']['slime' + str(int(i) + 1)]['stats']['dex'])
        print("Monster Initiative")
    print("Monsters added to field")
    for player in players:
        char = characters[player]
        initiative = random.randint(0, 10) + int(char['stats']['dex'])
        battlefield['player'][player] = \
            {'init': initiative}
        char['combat'] = True
    print("Players Added to field")


def search(c, u):
    randombattle = random.randint(1, 100)
    if randombattle >= 98:
        inv = characters[u]['inventory']
        if 'potion' in inv:
            inv['potion'] += 1
        else:
            inv['potion'] = 1
        add_message(c, "<@%s> found a Potion!" % u, "g")
    elif randombattle >= 20:
        generate_battle(1, u)
    elif randombattle >= 10:
        generate_battle(2, u)
    elif randombattle >= 4:
        generate_battle(3, u)
    else:
        generate_battle(5, u)
    if len(battlefield['monster']) >= 1:
        bfm = battlefield['monster']
        bfp = battlefield['player']
        send = "Monsters: \n"
        send2 = "Players: \n"
        for m in list(bfm):
            send = send + m + " Level: " + str(bfm[m]['level']) + "\n"
        for player in list(bfp):
            send2 = send2 + "<@" + player + "> Level: " + str(characters[player]['level']) + "\n"
        add_message(c, send + send2, "g")
    else:
        print("No battle")


#Needs to be worked on
def gototown():
    return


def help(u):
    add_message(channel, "Here is the list of working action:\n"
             "Stats, Help, 'Leave game'\n"
             "Please make sure to for actions with the key word '@mention action ...'", "")
    return


def stats(c, u):
    ch = characters[u]
    expneed = (int(ch['level']) * 100 - int(ch['exp']))
    add_message(c, "Class: %s Level: %s\n"
             "Exp till next: %s\n"
             "Health: %d Magic: %d\n"
             "You are currently at: %s" % (ch['class'],
                                           str(ch['level']),
                                           str(expneed),
                                           ch['hp'],
                                           ch['mp'],
                                           ch['location']), "g")


#Needs to be worked on
def move(c, u, x):
    return
    #Explore
        #North
            #Moves the user once UP
        #South
            #Moves the user once DOWN
        #East
            #Moves the user once Right
        #West
            #Moves the user once Left
    #Go to town
        #Buy
            #Buy items at market value
        #Sell
            #Sell items for a certain amount less the worth
    #Create Party
        #Creates a party that others can join
    #Join Party
        #Join an existing party
    #Leave Party
        #Leaves the current party


def combat(u, x):
    x.remove("action")
    if 'attack' in x:
        print('user attacks')
        damagephase('attack', u, x)
    elif 'skill' in x:
        damagephase('skill', u, x)
        print('user uses a skill')
    elif 'item' in x:
        damagephase('item', u, x)
        print('used item')
    elif 'defend' in x:
        damagephase('defend', u, x)
        print('Defends')
    elif 'list' in x:
        send = ""
        for i in list(battlefield['monster']):
            send = send + i
        add_message(channel, send, "g")
    elif 'help' in x:
        x = x.remove('help')
        if 'attack' in x:
            add_message(channel, "You can attack by using the follow '@mention attack slime0'\n m"
                           "Make sure to specify an enemy, if you are not sure type '@mention list", "g")
        else:
            add_message(channel, "That doesn't look like one of the commands I know", "g")
    else:
        add_message(channel, 'No action selected - Please use one of the following:\n Attack, Skill, Item, Defend\n'
              'Remember to use the following format: "@mention attack slime0" or "... item potion" or "... skill fire_bolt slime0" ', "g")
    #checkplayer()
    checkmonster()


def damagephase(action, u, x):
    x.remove(action)
    print(x)
    if action == "attack":
        print(battlefield)
        print(list(battlefield['monster']))
        if x[0] in list(battlefield['monster']):
            x = x[0]
            battlefield['monster'][x]['hp'] -= characters[u]['stats']['str']
            print("damage dealt")
            add_message(channel, "<@" + u + "> dealt " + str(characters[u]['stats']['str']) + "Damage to " + x, "g")
        else:
            add_message(channel, "No enemy selected", "g")
    elif action == "skill":
        print("skill")
    elif action == "item":
        print("item")
    elif action == "defend":
        print("defend")
    else:
        print("did not match")


#
# Test the battle system WORK IN PROGRESS
#
def test_battle():
    battle = {"player": {}, "monster": {}}


#
# Check to see if the monster is still alive
#
def checkmonster():
    bfp = battlefield['player']
    bfm = battlefield['monster']
    for i in list(bfm):
        if bfm[i]['hp'] <= 0:
            for player in bfp:
                characters[player]['exp'] += int(bfm[i]['exp'])/len(bfp)
                del battlefield['monster'][i]
                checklevelup(player)
    if len(list(bfm)) < 1:
        add_message(channel, "You Win!", "g")


#
# Check to see which user's turn it is, if a user who's turn it is
# does not send a message within 10 ticks then it will move to the next player
# If a user tries to send an action and it is not their turn,
# ignore the action until it is their turn
#
def waitturn(u, t):
    #wait T number of seconds to receive a action from certain user
    return


def checklevelup(players):
    for player in players:
        ch = characters[player]
        expneed = (int(ch['level']) * 100)
        if ch['exp'] >= expneed:
            ch['exp'] -= expneed
            levelup(player)


def levelup(player):
    ch = characters[player]
    stats = ch['stats']
    cclass = ch['class']
    ch['level'] += 1
    if cclass == "Fighter":
        stats['str'] += 3
        stats['dex'] += 2
        stats['int'] += 1
    elif cclass == "Ranger":
        stats['str'] += 2
        stats['dex'] += 3
        stats['int'] += 1
    elif cclass == "Mage":
        stats['str'] += 1
        stats['dex'] += 2
        stats['int'] += 3
    else:
        print("No Class")
    newskills(player, cclass)


#Need to be worked on
def newskills(player, cclass):
    print("New Skill")


#Not Currently Used
def findchannel(u):
    for channel in channelsplaying:
        if u in channel:
            return channel
        else:
            return ""


def load_character():
    global characters
    with open("characters.json", "r") as char:
        chars = json.load(char)

    return


def save_character():
    return

#
# Find a way to condense this into one response function
#
def randomresponse(input):
    select = random.randint(0, len(responses) - 1)
    checked = False
    for word in input:
        if word in validterm:
            checked = True
    if checked:
        add_message(channel, responses[select], "r")
    else:
        add_message(channel, respond(input), "s")


def check_rawinput(message):
    x = message
    if x:
        if len(x) > 0:
            if 'type' in x[0]:
                if x[0]['type'] == "message":
                    if 'text' in x[0]:
                        if 'user' in x[0]:
                            if x[0]['user'] != "U3GKQCDRD":
                                return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


def check_channeltype():
    global text
    if channel[0] != "D":
        if botname in text.split(" "):
            text = text.replace(botname, "")
            return True
    elif channel[0] == "D":
        return True
    else:
        return False


if sc.rtm_connect():
    while True:
        try:
            rawinput = sc.rtm_read()
            if check_rawinput(rawinput):
                x = rawinput[0]
                print(x)
                channel = x['channel']
                ch = channel
                user = x['user']
                text = x['text']
                msgtime = x['ts']
                if check_channeltype():
                    v = text.lower()
                    vs = v.split(' ')
                    state = checkstate(user)
                    if state == "ready":
                        if characters[user]['combat']:
                            if len(vs) > 1:
                                combat(user, vs)
                            else:
                                add_message(channel, "Please make sure you choose an enemy and an action: \n"
                                                     "Attach Slime1, Skill bash slime1, Item Potion Self", "g")
                        else:
                            if vs[0] == "action":
                                v = v.replace("action", '')
                                vs = v.split(' ')
                                if 'stat' in vs or 'stats' in vs:
                                    stats(ch, user)
                                elif 'search' in vs:
                                    search(ch, user)
                            elif "leavegame" in vs or "leave" in vs and "game" in vs:
                                leavegame(ch, user)
                            else:
                                help(user)
                    else:
                        if vs[0] == "postm":
                            add_message(ch, text, "")
                        elif "/taco" in text:
                            add_message(ch, "Thank you for your submission, sending @computerguru a :taco:", "z")
                        elif "tell" in vs and "james" in vs and "a" in vs and "joke" in vs:
                            add_message(ch, "http://wp.production.patheos.com/blogs/exploringourmatrix/files/2014/07/image1.jpg", "r")
                        elif "whoisplaying" in vs or "who" in vs and "is" in vs and "playing" in vs:
                            if playing > 0:
                                p = ""
                                add_message(ch, "These are the current players: ", "g")
                                for player in players:
                                    p = p + "<@" + player + ">\n"
                                add_message(ch, p, "g")
                            else:
                                add_message(ch, "The game has not started", "g")
                        elif "join" in vs and "game" in vs:
                            if playing == 0:
                                add_message(ch, "The game has not been started yet.", "g")
                            else:
                                join(ch, user, vs)
                        elif "playgame" in vs or "play" in vs and "game" in vs:
                            if playing == 0:
                                add_message(ch, "Game has been initiated", "g")
                                playing = 1
                                join(ch, user, vs)
                                # game.character_check(x['user'])
                            else:
                                add_message(ch, "The game is in session\n Joining...", "g")
                                join(ch, user, vs)
                                # game.start_game(x['user'])
                        elif "choose" in vs and "fighter" in vs or "ranger" in vs or "mage" in vs:
                            v = v.replace("choose", '')
                            v = v.split(" ")
                            create_character(ch, user, v)
                        # elif "give" in vs and "me" in vs and "gummies" in vs:
                        #     jelly.give_up_the_gummies()
                        elif vs[0] == "ml":
                            add_message(ch, movie(vs[1], vs[2], vs[3]), "")
                        else:
                            randomresponse(vs)
            delay_send()
            sleep(1)
        except Exception as e:
            print(e)
            sleep(1)
else:
    print("Connection Failed, invalid token?")
