Below are descriptions of what each script is and the variables you will need in your animator.
For OSC to update variables from an external script you will need to add the variable to the synced parameter list on your avatar.


Alternate Text Input:
This script is intended to be used as a method to use the chat box in VRChat through applications such as XSOverlay and OVR Toolkit.

Variables needed:
N/A


Example Server:
An example on how to use the osc_server portion of the pythonosc library to recieve messages from VRChat.

Variables needed:
VelocityX
VelocityY
VelocityZ


Example Async Concurrent:
An example on how to write a script using the pythonosc library that is able to send and recieve OSC messages from VRChat.
Some simple examples such as sending time and player velocity to VRChat show how to implement a pythonosc async concurrent server.

Variables needed:
VelocityX
VelocityY
VelocityZ
