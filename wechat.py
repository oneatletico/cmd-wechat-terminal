# /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date     : 2019-07-25
# @Author   : Lucas Zhang
# @FileName : wechat.py
# @Software : VS Code


# --------------------
# packages
# --------------------
import time
import itchat
import _thread
import logging
from itchat.content import *


# --------------------
# variables
# --------------------
# user name of this account
username = str()
# last message FROM (receive msg from) and TO (send msg to)
last_from, last_to = str(), str()
# all WeChat friends and the last 5 WeChat contacts
all_friends, recent_friends = [], []
# thread resource lock
f_lock = _thread.allocate_lock()


# --------------------
# debug functions
# --------------------
# @itchat.msg_register(itchat.content.TEXT)
# def debug_msg(msg):
#     "monitor new message to call this function and show all info of message"
#     print(msg)


# --------------------
# release functions
# --------------------
def show_help():
    "print help guide in terminal"
    print(
        """
        Terminal WeChat
            developed by Lucas Zhang
            based on ItChat

        Command List
            all                         List all WeChat friends of this account
            list                        List all WeChat friends of this account
            recent                      List the last 5 WeChat contacts of this accound
            help                        Show this help guide
            exit                        Log out

            send <message>              Send a message to the last TO (you send msg to)
            reply <message>             Send a message to the last FROM (you receive msg from)
            send <message> | <name>     Send a message to a friend specified by name
            send <message> || <num>     Send a message to a friend specified by num
        """
    )

def get_time():
    "get time and format it"
    return time.strftime('%H:%M:%S')

def get_info():
    "get wechat friends list"
    global username, all_friends
    # get wechat friends set by itchat
    set_friends = itchat.get_friends(update=True)
    # get current user info
    user = set_friends[0]
    username = user['RemarkName'] or user['NickName']
    # traverse set and added name into all_friends list
    for friend in set_friends:
        friend_name = friend['RemarkName'] or friend['NickName']
        all_friends.append(friend_name)
    # sort list
    all_friends.sort()

def update_friends(friend_name):
    "update wechat friends list"
    global all_friends, recent_friends
    # lock data to ensure atomicity
    f_lock.acquire()
    # insert last friend name to front of list
    if friend_name in recent_friends: recent_friends.remove(friend_name)
    recent_friends.insert(0, friend_name)
    if friend_name in all_friends: all_friends.remove(friend_name)
    all_friends.insert(0, friend_name)
    # control recent list length
    if len(recent_friends) > 5:
        recent_friends.pop()
    # release lock after update data
    f_lock.release()

def send_msg(content, friend_name):
    "send message to friends"
    # check message type
    try:
        content.encode('utf-8', 'ignore')
    except Exception as e:
        print("[ERROR] Unsupported message type!")
    else:
        # send message
        try:
            friend = itchat.search_friends(friend_name)[0]
            friend.send(content)
        except BaseException as e:
            print("[ERROR] Unable to find this friend!")
        else:
            # output sent message
            time_ = get_time()
            print(f"[{time_}] {username} -> {friend_name} : {content}")
            # update friend list and last TO
            if all_friends: update_friends(friend_name)
            global last_to
            last_to = friend_name

def send_format(command):
    "format send/reply command"
    # send default set to last TO
    if command.startswith("send"):
        command = command.strip("send").strip()
        default = "TO"
    # reply default set to last FROM
    elif command.startswith("reply"):
        command = command.strip("reply").strip()
        default = "FROM"
    # exit function if there is error
    else:
        print("[ERROR] Unspecified Error!")
        return -1
    
    # use TO by number if specified
    if command.find("||") >= 0:
        message = command.split(sep = "||", maxsplit = 1)[0].strip()
        number = command.split(sep = "||", maxsplit = 1)[1].strip()
        # try to transfer number from string to int
        try:
            number = int(number)
        except Exception as e:
            print("[ERROR] The specified num format is incorrect!")
            return -1
        else:
            if number <= 0 or number > len(all_friends):
                print("[ERROR] The specified num is out of index!")
                return -1
            else:
                friend_name = all_friends[number - 1]
    # use TO by name if specified
    elif command.find("|") >= 0:
        message = command.split(sep = "|", maxsplit = 1)[0].strip()
        friend_name = command.split(sep = "|", maxsplit = 1)[1].strip()
    # not specified TO, set as default
    else:
        message = command
        global last_from, last_to
        # "send", set TO as name
        if default == "TO":
            if last_to:
                friend_name = last_to
            else:
                print("[WARN] No Last TO! Please specify reveiver")
                print("e.g. > send <message> | <receiver name>")
                return -1
        # "reply", set FROM as name
        else:
            if last_from:
                friend_name = last_from
            else:
                print("[WARN] No Last FROM! Please specify reveiver")
                print("e.g. > send <message> | <receiver name>")
                return -1
    # call function send message
    send_msg(message, friend_name)

def show_list(friends):
    "show friends list"
    if all_friends:
        for index, friend_name in enumerate(friends):
            index += 1
            print(f"{index}. {friend_name}")
    else:
        print("No friend in this list")

def cmd_ctrl():
    "handle and format cmd"
    # input command and format
    command = input("> ")
    command = command.strip()
    command_ = command.casefold()
    # skip space
    if command == "": return 0
    # print help guide in terminal
    elif command_ == "help": show_help()
    # exit the script
    elif command_ == "exit" or command_ == "logout": itchat.logout()
    # show current date and time
    elif command_ == "time": print(time.strftime('%H:%M:%S'))
    # show all wechat friends list
    elif command_ == "list" or command_ == "all": show_list(all_friends)
    # show recent wechat friends list
    elif command_ == "recent": show_list(recent_friends)
    # send message to friend
    elif command.startswith("send") or command.startswith("reply"): send_format(command)
    # invalid input
    else: print("[ERROR] Invalid Input!")

def launcher_loop():
    "get command from terminal"
    # loop for refresh info
    while 1:
        # get all friends list
        if not all_friends:
            try:
                get_info()
            except BaseException as e:
                time.sleep(2)
            else:
                print("Loading wechat friends list")
        else:
            break
    # loop for get command input
    while 1:
        # input and format command
        cmd_ctrl()

@itchat.msg_register(itchat.content.TEXT)
def receive_msg(msg):
    "monitor new message to call this function"
    # get message content
    content = msg['Text']
    # get message time
    time_ = get_time()
    # get message sender
    friend_name = msg['User']['RemarkName'] or msg['User']['NickName']
    # show received message
    if msg['FromUserName'] == msg['User']['UserName']:
        print(f"\n[{time_}] {friend_name} -> {username} : {content}\n> ", end='')
    # show sent message
    else:
        print(f"\n[{time_}] {username} -> {friend_name} : {content}\n> ", end='')
    # update friend list and last FROM
    if all_friends: update_friends(friend_name)
    global last_from
    last_from = friend_name

# main function
def main():
    "main function"
    # disable itchat debug log
    logging.disable(logging.DEBUG)
    # create a thread for monitor command
    _thread.start_new_thread(launcher_loop, ())
    # itchat login
    itchat.auto_login(hotReload=True)
    # itchat run
    itchat.run(True)

# main flow
if __name__ == '__main__':
    main()
