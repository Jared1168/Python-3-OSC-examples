#libraries for OSC
import pythonosc.udp_client
import argparse
#text formatting
import colorama
#time
import time
import datetime
#math
import math

'''TIME STUFF'''
#shorten get current time data
global clockdata , hour , minute , second , second_prev
clockdata = hour = minute = second = second_prev = 0
#update the time
def updateTime():
    global clockdata , hour , minute , second
    clockdata = datetime.datetime.now()
    hour = clockdata.strftime('%H')
    minute = clockdata.strftime('%M')
    second = clockdata.strftime('%S')

'''MAIN PROCESS THREAD'''
if __name__ == "__main__": #if main thread

    #sets up OSC networking for sending to VRChat
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip" , default="127.0.0.1" , help="The ip of the OSC server")
    parser.add_argument("--port" , type=int , default=9000 , help="The port the OSC server is listening on")
    args = parser.parse_args()
    client = pythonosc.udp_client.SimpleUDPClient(args.ip, args.port)

    #initialize colorama
    colorama.init()

    #instructions to user
    print('Type here and hit enter to send in vrchat, enter \'h\' for help')

    #create variables
    user_pkg = text_pkg = ''
    char_count = sect_count = sect_last_len = current_sect = current_char = 0
    last_msg = ''

    while(True): #main loop
        '''INPUT'''
        print('\033[95m\n--> \033[32m',end='') #prompt for input
        last_msg = user_pkg #record last message
        user_pkg = input() #take input
        char_count = len(user_pkg) #count characters in input

        '''COMMANDS AND GENERIC MESSAGES'''
        if (user_pkg == 'h'): #help
            print('\nCOMMANDS:')
            print('HELP --------- h')
            print('RESEND MSG --- r')
            print('CREDITS ------ credits')
            print('\nGENERIC MESSAGES:')
            print('MUTE MSG ----- m')
            print('GOODBYE ------ g')
            print('SEND TIME ---- t')
        #commands
        elif (user_pkg == 'r'): #resend last message
            user_pkg = last_msg
        elif (user_pkg == 'credits'): print('\n\033[95mCREDITS: \033[32mCubicBigDog') #credits
        #generic messages
        elif (user_pkg == 'g'): user_pkg = 'I am getting off VR, goodbye/goodnight.' #generic goodbye msg
        elif (user_pkg == 'm'): user_pkg = 'I am mute right now.' #generic mute msg
        elif (user_pkg == 't'): #send current time
            updateTime() #updates time
            user_pkg = ('my time: '+str(hour)+':'+str(minute)+':'+str(second)) #sets msg to time

        '''SENDING MESSAGES'''
        if (user_pkg != 'h') & (user_pkg != 'credits'):
            if (char_count > 144): #if input is longer than 144 characters send in multiple messages
                sect_count = (math.floor(char_count / 144)) #find message count -1
                sect_last_len = (char_count % 144) #find length of last message
                
                while current_sect <= sect_count: #loops until all messages are sent
                    
                    if ((current_char+144) < char_count): #if not the last message
                        text_pkg = (user_pkg[current_char:(current_char + 144)]) #pack message
                        current_char = current_char + 144 #update character position
                    
                    else: #last message text packaging
                        text_pkg = [(user_pkg[current_char:(current_char + sect_last_len)]),True] #pack message
                    
                    current_sect = current_sect + 1 #update section count
                    print('\n\033[95mMessage ',current_sect,': \033[32m',user_pkg,sep='') #print message sent to console
                    client.send_message('/chatbox/input',text_pkg) #send message to VRChat
                    
                    if (current_sect <= sect_count): #if not the last message wait
                        time.sleep(10)
                    
            else: #if input is less than 144 characters send in one message
                text_pkg = [user_pkg,True]
                print('\n\033[95mMessage: \033[32m',user_pkg,sep='') #print message sent to console
                client.send_message('/chatbox/input',text_pkg) #send message to VRChat