# bot.py
import os
import random
import urllib.request, json


import discord
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
bot = commands.Bot(command_prefix = "!")


#can user play the sound
def getSound(sound, user):

    with open('json/commands.json') as json_file:
        data = json.load(json_file)
        data = data['commands']
        
        #url = "https://mygeoangelfirespace.city/db/commands.json"

        #response = urllib.request.urlopen(url)
        #print(len(data))
        #data = json.loads(response.read())
        for value in data:
            try:
                #print(data[f"{value}"]['name'])
                if(data[f"{value}"]['name'] == sound):
                    permittedUsers = data[f"{value}"]['permitted_users']
                    #print(permittedUsers)
                    for j in permittedUsers:
                        if(j == user):
                            print('Sound owned.')
                            return True
            except KeyError:
                continue
        
        print('sound not owned.')
        return False



#if user joins voice chat, play their theme song
@bot.event
async def on_voice_state_update(member, before, after):
    if member.display_name.lower() != 'chat_theif':
        if before.channel is None and after.channel is not None:
            if after.channel.name == 'General':
                #print(dir(member))
                user = member.display_name.lower()

                themeSoundsFilePath = "C:/gits/twitch-soundboard/theme_songs/"
    
                fileExists = os.path.exists(f"{themeSoundsFilePath}{user}.wav")
                fileExt = os.path.splitext(f"{themeSoundsFilePath}{user}.wav")
                if(fileExists == False):
                    fileExists = os.path.exists(f"{themeSoundsFilePath}{user}.opus")
                    fileExt = os.path.splitext(f"{themeSoundsFilePath}{user}.opus")
                    if(fileExists == False):
                        fileExists = os.path.exists(f"{themeSoundsFilePath}{user}.m4a")
                        fileExt = os.path.splitext(f"{themeSoundsFilePath}{user}.m4a")
                        if(fileExists == False):
                            fileExists = os.path.exists(f"{themeSoundsFilePath}{user}.mp3")
                            fileExt = os.path.splitext(f"{themeSoundsFilePath}{user}.mp3")
    
                member.guild.voice_client.play(discord.FFmpegPCMAudio(f"{themeSoundsFilePath}{user}{fileExt[1]}"), after=lambda e: print('done', e))   
            
#bot joins the server
@bot.command(name="joinServer", description="join a voice channel", pass_context=True,)
async def joinServer(ctx):
    voicechannel = discord.utils.get(ctx.guild.channels, name='General')
    await voicechannel.connect()

#plays a sound !play snorlax
@bot.command(name="play", description="play a sound", pass_context=True,)
async def playSound(ctx):
    print(ctx.message.content)

    soundeffect = ctx.message.content.split('!play ')
    soundeffect = soundeffect[1]
    
    username = ctx.author.display_name.lower()

    canPlay = getSound(soundeffect,username)

    if(canPlay == True):

        soundsFilePath = "C:/gits/twitch-soundboard/"

        fileExists = os.path.exists(f"{soundsFilePath}{soundeffect}.wav")
        fileExt = os.path.splitext(f"{soundsFilePath}{soundeffect}.wav")
        if(fileExists == False):
            fileExists = os.path.exists(f"{soundsFilePath}{soundeffect}.opus")
            fileExt = os.path.splitext(f"{soundsFilePath}{soundeffect}.opus")
            if(fileExists == False):
                fileExists = os.path.exists(f"{soundsFilePath}{soundeffect}.m4a")
                fileExt = os.path.splitext(f"{soundsFilePath}{soundeffect}.m4a")
                if(fileExists == False):
                    fileExists = os.path.exists(f"{soundsFilePath}{soundeffect}.mp3")
                    fileExt = os.path.splitext(f"{soundsFilePath}{soundeffect}.mp3")


        print(fileExt)
        print(f"trying to play {soundeffect}")

        ctx.voice_client.play(discord.FFmpegPCMAudio(f"{soundsFilePath}{soundeffect}{fileExt[1]}"), after=lambda e: print('done', e))
    else:
        await ctx.channel.send(f"@{username} you don't have access to sound: {soundeffect}.")

#Bot returns link to users website
@bot.command(name="me", description="get users website", pass_context=True)
async def me(ctx):

    #print(dir(ctx.author.display_name))
    
    website ="https://mygeoangelfirespace.city/" 

    #get users username   
    username = ctx.author.display_name.lower()

    url = website + username + ".html"

    print(url)
    await ctx.channel.send(url)


#run
bot.run(TOKEN)