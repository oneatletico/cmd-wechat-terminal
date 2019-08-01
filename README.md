# cmd-wechat-terminal 
WeChat running on the command line, can send and receive messages, based on itchat

可运行在命令行的微信，能够发送和接收消息，基于ItChat开发

## Features
- Log in WeChat in Terminal by scan QR code
- Show WeChat friends list
- Show WeChat recent contacts list
- Receive WeChat messages and show in command line
- Send messages to WeChat friends by the specified name / num

## How To Run
``` bash
# clone this repository
git clone git@github.com:oneatletico/cmd-wechat-terminal.git
# enter this repository
cd cmd-wechat-terminal
# install dependencies
pip install itchat
# run wechat.py directly
./wechat.py
```

## How To Use
``` bash
all                         # List all WeChat friends of this account
list                        # List all WeChat friends of this account
recent                      # List the last 5 WeChat contacts of this accound
help                        # Show this help guide
exit                        # Log out
send <message>              # Send a message to the last TO (you send msg to)
reply <message>             # Send a message to the last FROM (you receive msg from)
send <message> | <name>     # Send a message to a friend specified by name
send <message> || <num>     # Send a message to a friend specified by num
```

## Demo
``` bash
Login successfully as Lucas Zhang
Loading wechat friends list

[13:55:17] Leo ->  : Hi
> recent
1. Leo
> send Hello || 1
[13:55:43]  -> Leo : Hello
```
