# RPI-Announce
This is a hastily written script to create an announcement queue for the Raspberry Pi.  The specific purpose was to use in conjunction with OpenHab to queue announcements to make throughout the house.
 
 
 **WARNING: this is not even close to being secure.  The script runs as root and is almost guaranteed to be vulnerable to command injection**
 I have my Raspberry Pi setup on a separate, firewalled VLAN, so only the automation controller can access it directly.
 
 
Example:

http://rpi-announce:8084/?type=sound&message=wx_alert&times=1&volume=5&priority=200&id=wx&zone=B

Where: 
* _type_ is the set to "sound" to play a pre-recorded .wav file from /var/sounds/ (_type_ is there with the idea that text to speech might be available in the future)
* _message_ is the name of the .wav file to play from /var/sounds/  (in this case, *wx_alert.wav*)

