# RPI-Announce
This is a **hastily** written script to create an announcement queue for the Raspberry Pi.  The specific purpose was to use in conjunction with OpenHab to queue announcements to make throughout the house.  This code is _not polished at all_, but is functional.
 
 
 **WARNING: this is not even close to being secure.  The script runs as root and is almost guaranteed to be vulnerable to command injection**
 I have my Raspberry Pi setup on a separate, firewalled VLAN, so only the automation controller can access it directly.


# Raspberry Pi Setup
I have a 2 relay board with relay control on pins 24 and 25 for zones A and B.  I have an amplifier plugged into the output of a USB audio adapter on the Pi.  The left output of the amp is split and routed through both of the relays and then speakers are hooked up to the relay output to create the zones.
 
# Example 1 (Creating an announcement)

http://rpi-announce:8084/?type=sound&message=wx_alert&times=1&volume=5&priority=200&id=wx&zone=B

Where: 
* _type_ is the set to "sound" to play a pre-recorded .wav file from /var/sounds/ (_type_ is there with the idea that text to speech might be available in the future)
* _message_ is the name of the .wav file to play from /var/sounds/  (in this case, *wx_alert.wav*)
* _times_ is the amount of times to play the announcement (if _times_ is 0, the announcement will loop until it is stopped with a stop command)
* _volume_ is the volume to set the Pis volume to while playing the announcement
* _priority_ defines the order the announcements will be played (lower numbers first) if there are multiple in queue
* _id_ is only really used for times=0 announcements so that it can be referenced to stop it (but it is always required)
* _zone_ is the zone to play it in.  My relays are set to _A_ is outside, _B_ is inside, and _C_ is all zones

# Example 2 (Stopping a looping announcement)

http://rpi-announce:8084/?id=wx

This will stop a continuously looping (times=0) announcment with id of wx 

# Running on startup

I added

/usr/bin/python3 /home/pi/AnnouncementSystem.py &

to rc.local on the Pi right before the _exit 0_
