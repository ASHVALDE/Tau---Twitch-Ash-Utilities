from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
from tkinter import messagebox

from gtts import gTTS
import pygame

import time


USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
TARGET_CHANNEL = ""
pygame.init()
pygame.mixer.init()

# this will be called when the event READY is triggered, which will be on bot start
async def on_ready(ready_event: EventData):
    

    print('Bot is ready for work, joining channels')
    # join our target channel, if you want to join multiple, either call join for each individually
    # or even better pass a list of channels as the argument
    xd = await ready_event.chat.join_room(TARGET_CHANNEL)

    # you can do other bot initialization things in here


lastMessageAuthor = ""
mensajes = []
# this will be called whenever a message in a channel was send by either the bot OR another user
async def on_message(msg: ChatMessage):
    global lastMessageAuthor
    mensaje = msg.text
    if(lastMessageAuthor!=msg.user.name):
        mensaje = msg.user.name + " dice " + msg.text

    global userSpeaking
    numero = msg.user.name+"."+str( time.time())
    tts = gTTS(text=mensaje, lang = 'es')
    tts.save( numero+'.mp3')
    mensajes.append(numero)
    if(not pygame.mixer.music.get_busy()):
        pygame.mixer.music.load(numero+'.mp3')
        pygame.mixer.music.play()
        lastMessageAuthor = msg.user.name
        pygame.mixer.music.set_endevent(691) 

        

# this will be called whenever someone subscribes to a channel
async def on_sub(sub: ChatSub):
    print(f'New subscription in {sub.room.name}:\\n'
          f'  Type: {sub.sub_plan}\\n'
          f'  Message: {sub.sub_message}')


# this will be called whenever the !reply command is issued
async def test_command(cmd: ChatCommand):
    if len(cmd.parameter) == 0:
        await cmd.reply('you did not tell me what to reply with')
    else:
        await cmd.reply(f'{cmd.user.name}: {cmd.parameter}')


# this is where we set up the bot

async def twitch_init(APP_ID,APP_SECRET,TARGET_CHANNELx):
    global TARGET_CHANNEL
    TARGET_CHANNEL = TARGET_CHANNELx
    # set up twitch api instance and add user authentication with some scopes
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)
 
    # create chat instance
    chat = await Chat(twitch)


    # listen to when the bot is done starting up and ready to join channels
    chat.register_event(ChatEvent.READY, on_ready)
    # listen to chat messages
    chat.register_event(ChatEvent.MESSAGE, on_message)
    # listen to channel subscriptions
    chat.register_event(ChatEvent.SUB, on_sub)
    # there are more events, you can view them all in this documentation

    # you can directly register commands and their handlers, this will register the !reply command
    chat.register_command('reply', test_command)


    # we are done with our setup, lets start this bot up!
    chat.start()

    # lets run till we press enter in the console
    try:
        input('press ENTER to stop\\n')
    finally:
        # now we can close the chat bot and the twitch api client
        chat.stop()
        await twitch.close()

raiz = False
def twitchCheckSong(root):
    global raiz
    raiz = root
    
    twitchCheckSong2()

def twitchCheckSong2():
    global lastMessageAuthor
    for event in pygame.event.get():
        print(event.type)
        if event.type == 691:
            mensajes.pop(0)
            if(len(mensajes)!=0):
                
                pygame.mixer.music.load(mensajes[0]+'.mp3')
                pygame.mixer.music.play()
                lastMessageAuthor = mensajes[0].split(".")[0]
                pygame.mixer.music.set_endevent(691) 
    raiz.after(100, twitchCheckSong2)