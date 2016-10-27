#!/usr/bin/python3
version = 'v 0.1'
import vk, datetime, sys, time, curses, os
#https://oauth.vk.com/authorize?client_id=2895443&scope=33554431&response_type=token
access_token=''
custom_user_id=''
count_of_dialogs=16
count_of_messages=50


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


class UserCache(object):
    """Create/search .usercache file. Add and get users from cache"""
    def __init__(self):
        if os.path.exists('.userscache')==False:
            open(".userscache", "w")

    def add_user_in_cache(self,user_id, user_surname, user_name):
        with open(".userscache", "a") as userscache:
            userscache.write(str(user_id)+','+user_surname+','+user_name+'\n')

    def get_users_from_cache(self):
        with open('.userscache', 'r') as file:
            users_list = [line.rstrip('\n') for line in file]
        return users_list


myscreen = curses.initscr() 
session = vk.Session(access_token)
api = vk.API(session)

class MyInfo(object):
    """docstring for MyInfo"""
    my_user=api.users.get()
    my_id=str(my_user[0].get('uid'))
    def __init__(self):
        pass

class Messages(object):
    """Send/get messages"""
    def input_message(self,user_id):
        message=input('A:')
        if (message=='!rs' or message=='/rs' or message=='!reload' or message=='/reload'):
            self.print_messages(user_id=user_id)
        elif (message=='!b' or message=='/b' or message=='!back' or message=='/back'):
            aInterface.startDialogs()
        elif (message=='!exit' or message=='/exit'):
            print('Thank you for using mt app')
        else:
            api.messages.send(user_id=user_id,message=message)
            self.print_messages(user_id=user_id)
            
    def print_messages(self,user_id):
        global myscreen
        global count_of_messages
        curses.endwin()
        lists=api.messages.getHistory(uid=user_id)
        if lists[0]<count_of_messages:
            count_of_messages=lists[0]
            lists=api.messages.getHistory(uid=user_id, count=count_of_messages)
        else:
            lists=api.messages.getHistory(uid=user_id, count=count_of_messages)
        for i in range(count_of_messages):
            if str(lists[count_of_messages-i].get('uid'))==aInfo.my_id:
                if lists[count_of_messages-i].get('read_state')==0:
                    color_on=bcolors.OKBLUE
                    color_off=bcolors.ENDC
                else:
                    color_on=''
                    color_off=''
                message_a='A: '+color_on+lists[count_of_messages-i].get('body')+color_off+bcolors.WARNING+'('+datetime.datetime.fromtimestamp(int(lists[count_of_messages-i].get('date'))).strftime('%Y-%m-%d %H:%M:%S')+')'+'\n'+bcolors.ENDC
                message_a=message_a.replace("<br>","\n   ")
                print(message_a)
            else:
                if lists[count_of_messages-i].get('read_state')==0:
                    color_on=bcolors.OKBLUE
                    color_off=bcolors.ENDC
                else:
                    color_on=''
                    color_off=''
                message_she='She: '+color_on+lists[count_of_messages-i].get('body')+color_off+bcolors.WARNING+'('+datetime.datetime.fromtimestamp(int(lists[count_of_messages-i].get('date'))).strftime('%Y-%m-%d %H:%M:%S')+')'+'\n'+bcolors.ENDC
                message_she=message_she.replace("<br>","\n     ")
                print(message_she)
        self.input_message(user_id=user_id)

    def print_messages_chat(self,chat_id):
        global myscreen
        try:
            os.system('clear')
            os.system('cls')
        except Exception as e:
            pass
        else:
            pass
        finally:
            print('Here will be a chat')
        # curses.endwin()
        # lists=api.messages.getChat(chat_id=chat_id, count=50)
        # print(lists)

class Interface(object):
    """docstring for Interface"""
    def startDialogs(self):
        in_base=False
        global myscreen
        global count_of_dialogs
        users_list=aCache.get_users_from_cache()
        dialog=[]
        userinfo=[]
        aList=[]
        lists=api.messages.getDialogs(count=count_of_dialogs)
        for i in range(count_of_dialogs):
            if str(lists[i+1].get('read_state'))=='0':
                color_on=bcolors.OKBLUE
                color_off=bcolors.ENDC
            else:
                color_on=''
                color_off=bcolors.ENDC
            if lists[i+1].get('out')=='1':
                is_out=bcolors.OKGREEN+'A:'+bcolors.ENDC
            else:
                is_out=''
            for j in users_list:
                if str(lists[i+1].get('uid')) in j:
                    aList=j.split(',')
                    userinfo_dict={'last_name':aList[1],'first_name':aList[2]}
                    userinfo=[userinfo_dict]
                    in_base=True
            if in_base==False:
                userinfo=api.users.get(user_ids=lists[i+1].get('uid'))
                time.sleep(0.3)
                aCache.add_user_in_cache(user_id=lists[i+1].get('uid'),user_surname=userinfo[0].get('last_name'),user_name=userinfo[0].get('first_name'))
            in_base=False
            if lists[i+1].get('title')!=' ... ':
                dialog.append(str(i+1)+'. '+bcolors.HEADER+lists[i+1].get('title')+'('+bcolors.HEADER+userinfo[0].get('last_name')+' '+userinfo[0].get('first_name')+')'+':'+is_out+color_off+color_on+lists[i+1].get('body')+color_off+bcolors.WARNING+'('+datetime.datetime.fromtimestamp(int(lists[i+1].get('date'))).strftime('%Y-%m-%d %H:%M:%S')+')'+bcolors.ENDC)
            else:
                dialog.append(str(i+1)+'. '+bcolors.HEADER+userinfo[0].get('last_name')+' '+userinfo[0].get('first_name')+color_off+':'+is_out+color_on+lists[i+1].get('body')+color_off+bcolors.WARNING+'('+datetime.datetime.fromtimestamp(int(lists[i+1].get('date'))).strftime('%Y-%m-%d %H:%M:%S')+')'+bcolors.ENDC) 
        curses.endwin()
        myscreen.refresh() 
        secondScr = curses.initscr()
        secondScr.refresh()
        curses.endwin()
        for i in range(count_of_dialogs):
            if i<10:
                print(' '+dialog[i])
            else:
                print(dialog[i])
        number_of_dialog=int(input('Choose number of a dialog:'))
        if lists[number_of_dialog].get('chat_id')!=None:
            aMessages.print_messages_chat(chat_id=lists[number_of_dialog].get('chat_id'))
        else:
            aMessages.print_messages(user_id=lists[number_of_dialog].get('uid'))

class Console(object):
    """docstring for Console"""
        
    def startConsole(self):
        global myscreen
        global version
        myscreen.border(0) 
        myscreen.addstr(0, 0, version)
        myscreen.addstr(12, 25, "Welcome to YouRASH VK client") 
        myscreen.refresh() 
        global custom_user_id
        if custom_user_id=='':
            print('Enter custom user id in the app pls')
        if len (sys.argv) > 1:
            if sys.argv[1] and sys.argv[1].isdecimal():
                user_id=sys.argv[1]
                if sys.argv[1]=='1':
                    aMessages.print_messages(user_id=custom_user_id)
                else:
                    aMessages.print_messages(user_id=user_id)
        else:
            aInterface.startDialogs()

def startApp():
    #if sys.argv[1]=='-c' or sys.argv[1]=='console':
    if len (sys.argv) > 1:
        if sys.argv[1]!='ui':
            aConsole.startConsole()
        else:
            pass 
    else:
        aConsole.startConsole()

def main():
    try:
        startApp()
    except Exception as e:
        time.sleep(10)
        print(e)
    finally:
        startApp()

if __name__ == '__main__':
    aCache=UserCache()
    aMessages=Messages()
    aInterface=Interface()
    aConsole=Console()
    aInfo=MyInfo()
    main()
