# bot.py
import os
import random
import urllib.request, json

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = "!")

#check if path is real
def getRealSound(path, filename):
    exts = {'wav', 'opus', 'm4a', 'mp3'}

    for ext in exts:
        if(os.path.exists(f"{path}{filename}.{ext}")):
            print (f"{path}{filename}.{ext}")
            return ext


#give user mana
def assignMana(amount, user):
    #first check if they are in the file
    with open('json/mana.json', 'r+') as manaFile:
        data = json.load(manaFile)

        for value in data:
            if(data[f"{value}"]['user'] == user):
                print("User in file")
                #if they are update amount
                data[f"{value}"]['mana'] = amount
                manaFile.seek(0)
                json.dump(data, manaFile, indent=2)
                manaFile.close()
                return
                
        #if not add to file
        print("User not in File")
        newEntry ={
            f"{user}":{
                "user" : f"{user}",
                "mana" : amount
                }
                }
        data.update(newEntry)
        manaFile.seek(0)
        json.dump(data, manaFile, indent=2)
        manaFile.close()


def useMana(user):
    #first check if they are in the file
    with open('json/mana.json', 'r+') as manaFile:
        data = json.load(manaFile)

        for value in data:
            if(data[f"{value}"]['user'] == user):
                print("User in file")
                #if they are update amount
                data[f"{value}"]['mana'] = data[f"{value}"]['mana'] - 1
                manaFile.seek(0)
                json.dump(data, manaFile, indent=2)
                manaFile.close()

def getMana(user):
     #first check if they are in the file
    with open('json/mana.json', 'r+') as manaFile:
        data = json.load(manaFile)

        for value in data:
            if(data[f"{value}"]['user'] == user):
                print("User in file")
                #if they are update amount
                if(data[f"{value}"]['mana'] <= 0):
                    manaFile.close()
                    return False
                else:
                    manaFile.close()
                    return True


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
            
            #print(dir(member))
            user = member.display_name.lower()

            #update mana
            assignMana(3, user)
            themeSoundsFilePath = "C:/gits/twitch-soundboard/theme_songs/"
            ext = getRealSound(themeSoundsFilePath, user)
            
            member.guild.voice_client.play(discord.FFmpegPCMAudio(f"{themeSoundsFilePath}{user}.{ext}"), after=lambda e: print('done', e))   
            
#bot joins the server
@bot.command(name="join", description="join a voice channel", pass_context=True,)
async def joinServer(ctx):
    voicechannel = ctx.author.voice.channel
    await voicechannel.connect()

#plays a sound !play snorlax
@bot.command(name="play", description="play a sound", pass_context=True,)
async def playSound(ctx):
    print(ctx.message.content)

    soundeffect = ctx.message.content.split('!play ')
    soundeffect = soundeffect[1]
    
    username = ctx.author.display_name.lower()

    canPlay = getSound(soundeffect,username)

    hasMana = getMana(username)

    if(canPlay == True):
        if(hasMana == True):

            soundsFilePath = "C:/gits/twitch-soundboard/"
            ext = getRealSound(soundsFilePath, soundeffect)

            print(f"trying to play {soundeffect}")

            ctx.voice_client.play(discord.FFmpegPCMAudio(f"{soundsFilePath}{soundeffect}.{ext}"), after=lambda e: print('done', e))
            useMana(username)
        else:
            await ctx.channel.send(f"@{username} you don't have any mana.")
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

@bot.command(name="perms", description="get owners of a sound", pass_context=True)
async def permissions(ctx):
    print(ctx.message.content)

    soundeffect = ctx.message.content.split('!perms ')
    soundeffect = soundeffect[1]

    with open('json/commands.json') as json_file:
        data = json.load(json_file)
        data = data['commands']
        
        for value in data:
            try:
                if(data[f"{value}"]['name'] == soundeffect):
                    permittedUsers = data[f"{value}"]['permitted_users']
            except KeyError:
                continue

    await ctx.channel.send(f"Users that own sound: {soundeffect}: {permittedUsers}")





#run
bot.run(TOKEN)



