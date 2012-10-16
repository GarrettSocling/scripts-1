#! /usr/bin/env python

# xchat script to play different sounds in different circumstances.
# Copyright 2012 by Akkana Peck, http://shallowsky.com.
# Share and enjoy under the GPLv2 or (at your option) any later version.

__module_name__ = "chatsounds" 
__module_version__ = "0.1" 
__module_description__ = "Plays sounds when it sees keywords"
__module_author__ = "Akkana Peck <akkana@shallowsky.com>"

import xchat
import sys, os, subprocess
import time

# Globals that you may want to customize:
APLAY = "/usr/bin/aplay"
SOUND_DIR = os.path.expanduser("~/.xchat2/sounds/")
SILENCE = False
START_TIME = time.time()
STARTUP_DELAY = 15     # No sounds will be played in the first few seconds

def play_alert(alertfile) :
    subprocess.call([APLAY, '-q', alertfile])

def handle_message(word, word_eol, userdata):
    '''
    Handle a message in xchat.
    word is something like:
      [ '\xaaaanick', "the message we're acting on" ]
      where aaaa is a number like \x0328
      This, incidentally, is not what the doc says it should be at
      http://xchat.org/docs/xchatpython.html
    userdata is something like: 'Channel Message', from EVENTS,
    so you can play different sounds depending on what happened.
    '''

    # If we're silenced, don't do anything.
    if SILENCE :
        return xchat.EAT_NONE

    # If it's too soon after startup, don't do anything.
    # Then we won't hear a slew of alerts from past scrollback,
    # NickServ 'You are now identified for" messages, etc.
    if time.time() - START_TIME < STARTUP_DELAY :
        return xchat.EAT_NONE

    # You may want to use channel name, network name or variables
    # in the xchat context to decide which alerts to play.
    channel = xchat.get_info( 'channel' )
    network = xchat.get_info( 'network' )
    ctxt = xchat.get_context()
    mynick = ctxt.get_info("nick")
    line = word[1]

    # Now, customize the rest as desired. Here are some examples:

    # Anyone addressing or mentioning my nick:
    if line.find(mynick) > 0 and word[0] != 'NickServ' or \
           userdata == "Channel Msg Hilight" or \
           userdata == "Channel Action Hilight" :
        # print ">>>>> Contains my nick!", userdata, ">>", line
        play_alert(os.path.join(SOUND_DIR, "akk.wav"))

    # Private message:
    elif userdata.startswith("Private Message") :
        # print ">>>>> Private message!"
        play_alert(os.path.join(SOUND_DIR, "akk.wav"))

    # More subtle sound for bitlbee/twitter, since they're so numerous:
    elif channel == "#twitter_" + mynick :
        # print ">>>>> Twitter channel!"
        play_alert(os.path.join(SOUND_DIR, "SingleClick.wav"))

    # if you want to be fairly noisy or don't have many active channels,
    # you might want an alert for every channel message:
    elif userdata.startswith("Channel M") or \
            userdata.startswith("Channel Action") :
        play_alert(os.path.join(SOUND_DIR, "pop.wav"))

    return xchat.EAT_NONE

def handle_prefs(word, word_eol, userdata) :
    ''' Use this for any prefs/actions, like silence/unsilence.
    '''
    global SILENCE

    if word[1] == 'silence' :
        SILENCE = True
        print "chatsounds silenced"
    elif word[1] == 'unsilence' :
        SILENCE = False
        print "chatsounds unsilenced"

    return xchat.EAT_ALL

# Comment out any events for which you don't want alerts:
EVENTS = [
  "Channel Action",
  "Channel Action Hilight",
  "Channel Message",
  "Channel Msg Hilight",
  "Channel Notice",
  "Generic Message",
  "Kick",
  "Killed",
#  "Motd",
  "Notice",
#  "Part with Reason",
  "Private Message",
  "Private Message to Dialog",
#  "Quit",
  "Receive Wallops",
  "Server Notice",
  "Server Text",
#  "Topic",
#  "Topic Change",
]

for event in EVENTS:
    xchat.hook_print(event, handle_message, event)

xchat.hook_command("chatsounds", handle_prefs)

print "Loaded chatsounds.py"
