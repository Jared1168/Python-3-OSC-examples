"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse

import pythonosc.dispatcher
import pythonosc.osc_server

#Velocity
global vel_x
global vel_y
global vel_z
global vel_Player
vel_x = float(0)
vel_y = float(0)
vel_z = float(0)
vel_Player = float(0)

#speech
global MuteSelf
global Visime
MuteSelf = float(0)
Visime = float(0)

#Finds absolute velocity
def FindVelocity(x,y,z):
    return ((pow(x,2))+(pow(y,2))+(pow(z,2)))

#Extracts X Velocity
def VelocityX(address, *args):
    global vel_x
    vel_x = args[0]
    print(args[0])
#Extracts Y Velocity
def VelocityY(address, *args):
    global vel_y
    vel_y = args[0]
    print(args[0])
#Extracts Z Velocity
def VelocityZ(address, *args):
    global vel_z
    vel_z = args[0]
    print(args[0])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip" , default="127.0.0.1" , help="The ip to listen on")
    parser.add_argument("--port" , type=int , default=9001 , help="The port to listen on")
    args = parser.parse_args()
    
    pythonosc.dispatcher = pythonosc.dispatcher.Dispatcher()
    #pythonosc.dispatcher.map("/avatar/parameters/Visime" , print)
    
    pythonosc.dispatcher.map("/avatar/parameters/VelocityX" , VelocityX)
    pythonosc.dispatcher.map("/avatar/parameters/VelocityY" , VelocityY)
    pythonosc.dispatcher.map("/avatar/parameters/VelocityZ" , VelocityZ)
    
    server = pythonosc.osc_server.ThreadingOSCUDPServer((args.ip, args.port), pythonosc.dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

