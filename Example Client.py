import argparse
import time
import math
import colorama
import pythonosc.udp_client

#initialize colorama
colorama.init()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip" , default="127.0.0.1" , help="The ip of the OSC server")
    parser.add_argument("--port" , type=int , default=9000 , help="The port the OSC server is listening on")
    
    args = parser.parse_args()
    client = pythonosc.udp_client.SimpleUDPClient(args.ip, args.port)
    
    LoopCount1 = 0
    LoopCount2 = 0
    LoopCount3 = 0
    LoopCount4 = 0
    #green
    print('\033[32m')
    while(True):
        #Test1
        LoopCount1 = LoopCount1 + 1
        print('\033[1;1HTestA - Sine Wave -','%.3f'%((math.sin(LoopCount1/75)+1)*0.45))#move cursor to line 1 character 1 and prints current output value
        client.send_message("/avatar/parameters/Test1",float('%.3f'%((math.sin(LoopCount1/75)+1)*0.45)))
        #Test2
        if (LoopCount2 >= 200):
            LoopCount2 = 0
        else:
            LoopCount2 = LoopCount2 + 1
        print('TestB - Linear ---- %.3f'%(LoopCount2/200))
        client.send_message("/avatar/parameters/Test2",float('%.3f'%(LoopCount2/200)))
        time.sleep(0.0025)