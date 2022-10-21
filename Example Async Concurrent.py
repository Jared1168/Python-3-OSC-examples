from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import datetime
import asyncio
import argparse
import pythonosc.udp_client
import os
import random

#network OSC
ip = "127.0.0.1"
port_VRC_OUT = 9001
port_VRC_IN = 9000

'''TIME STUFF'''
#shorten get current time data
global ClockData
global Hour
global Minute
global Second
ClockData = 0
Hour = 0
Minute = 0
Second = 0
#update the time
def updateTime():
    global ClockData
    global Hour
    global Minute
    global Second
    ClockData = datetime.datetime.now()
    Hour = ClockData.strftime("%H")
    Minute = ClockData.strftime("%M")
    Second = ClockData.strftime("%S")

'''PLAYER VELOCITY MATH'''
#Variables
global vel_x , vel_y , vel_z , vel_Player
vel_x = vel_y = vel_z = vel_Player = float(0)
#Finds absolute velocity
def FindVelocity(x,y,z):
    velocity = float(round(((pow(x,2))+(pow(y,2))+(pow(z,2))),3))
    if (velocity <= 100):
        return (round((velocity*0.1),3))
    else:
        return float(1.000)
#Extracts X Velocity
def VelocityX(address, *args):
    global vel_x
    vel_x = args[0]
    vel_x = round(vel_x, 3)
#Extracts Y Velocity
def VelocityY(address, *args):
    global vel_y
    vel_y = args[0]
    vel_y = round(vel_y, 3)
#Extracts Z Velocity
def VelocityZ(address, *args):
    global vel_z
    vel_z = args[0]
    vel_z = round(vel_z, 3)

'''CLEAR CONSOLE'''
def ClearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

'''SEND PLAYER VELOCITY TO VRCHAT'''
async def Player_Velocity():
    global vel_x , vel_y , vel_z , vel_Player
    vel_Player = FindVelocity(vel_x,vel_y,vel_z) 
    print("x:",vel_x,"|","y:",vel_y,"|","z:",vel_z,"vel: ",vel_Player,"#DEBUG") #DEBUG
    if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip" , default=ip , help="The ip of the OSC server")
        parser.add_argument("--port" , type=int , default=port_VRC_IN , help="The port the OSC server is listening on")
        args = parser.parse_args()
        client = pythonosc.udp_client.SimpleUDPClient(args.ip, args.port)
        client.send_message("/avatar/parameters/MarksHueShift",vel_Player)
    await asyncio.sleep(0)

'''SEND CLOCK DATA TO VRCHAT'''
async def Player_Time():
    updateTime()
    global ClockData
    global Hour
    global Minute
    global Second
    print("H:",Hour,"|","M:",Minute,"|","S:",Second,"#DEBUG") #DEBUG
    if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip" , default=ip , help="The ip of the OSC server")
        parser.add_argument("--port" , type=int , default=port_VRC_IN , help="The port the OSC server is listening on")
        args = parser.parse_args()
        client = pythonosc.udp_client.SimpleUDPClient(args.ip, args.port)
        client.send_message("/avatar/parameters/ClockHour",Hour)
        client.send_message("/avatar/parameters/ClockMinute",Minute)
        client.send_message("/avatar/parameters/ClockSecond",Second)
    await asyncio.sleep(0)

'''SEND RANDOMS TO VRCHAT'''
async def Player_Random_Source():
    VRC_Rand_Bool = bool(random.randint(0,1))
    VRC_Rand_Int = random.randint(0,255)
    VRC_Rand_Float = round(float(random.random()),3)
    print("B:",VRC_Rand_Bool,"|","I:",VRC_Rand_Int,"|","F:",VRC_Rand_Float,"#DEBUG") #DEBUG
    if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip" , default=ip , help="The ip of the OSC server")
        parser.add_argument("--port" , type=int , default=port_VRC_IN , help="The port the OSC server is listening on")
        args = parser.parse_args()
        client = pythonosc.udp_client.SimpleUDPClient(args.ip, args.port)
        client.send_message("/avatar/parameters/VRC_Rand_Bool",VRC_Rand_Bool)
        client.send_message("/avatar/parameters/VRC_Rand_Int",VRC_Rand_Int)
        client.send_message("/avatar/parameters/VRC_Rand_Float",VRC_Rand_Float)
    await asyncio.sleep(0)

'''SET UP SERVER LISTENING'''
async def init_Concurrent_Server():
    dispatcher = Dispatcher()
    #get velocity components
    dispatcher.map("/avatar/parameters/VelocityX" , VelocityX)
    dispatcher.map("/avatar/parameters/VelocityY" , VelocityY)
    dispatcher.map("/avatar/parameters/VelocityZ" , VelocityZ)
    
    server = AsyncIOOSCUDPServer((ip, port_VRC_OUT), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving
    
    while True:
        await Player_Velocity()
        await Player_Time()
        #await Player_Random_Source()
        await asyncio.sleep(0.01)
        ClearConsole()
    
    transport.close()  # Clean up serve endpoint

asyncio.run(init_Concurrent_Server())
