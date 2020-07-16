# bot.py
import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
bot = commands.Bot(command_prefix = "!")

#if user joins voice chat, play their theme song
@bot.event
async def on_voice_state_update(member, before, after):
    if member.display_name.lower() != 'chat_theif':
        if before.channel is None and after.channel is not None:
            if after.channel.name == 'General':
                #print(dir(member))
                user = member.display_name.lower()
    
                fileExists = os.path.exists(f"C:/gits/twitch-soundboard/theme_songs/{user}.wav")
                fileExt = os.path.splitext(f"C:/gits/twitch-soundboard/theme_songs/{user}.wav")
                if(fileExists == False):
                    fileExists = os.path.exists(f"C:/gits/twitch-soundboard/theme_songs/{user}.opus")
                    fileExt = os.path.splitext(f"C:/gits/twitch-soundboard/theme_songs/{user}.opus")
                    if(fileExists == False):
                        fileExists = os.path.exists(f"C:/gits/twitch-soundboard/theme_songs/{user}.m4a")
                        fileExt = os.path.splitext(f"C:/gits/twitch-soundboard/theme_songs/{user}.m4a")
                        if(fileExists == False):
                            fileExists = os.path.exists(f"C:/gits/twitch-soundboard/theme_songs/{user}.mp3")
                            fileExt = os.path.splitext(f"C:/gits/twitch-soundboard/theme_songs/{user}.mp3")
    
                member.guild.voice_client.play(discord.FFmpegPCMAudio(f"C:/gits/twitch-soundboard/theme_songs/{user}{fileExt[1]}"), after=lambda e: print('done', e))   
            
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

    fileExists = os.path.exists(f"C:/gits/twitch-soundboard/{soundeffect}.wav")
    fileExt = os.path.splitext(f"C:/gits/twitch-soundboard/{soundeffect}.wav")
    if(fileExists == False):
        fileExists = os.path.exists(f"C:/gits/twitch-soundboard/{soundeffect}.opus")
        fileExt = os.path.splitext(f"C:/gits/twitch-soundboard/{soundeffect}.opus")
        if(fileExists == False):
            fileExists = os.path.exists(f"C:/gits/twitch-soundboard/{soundeffect}.m4a")
            fileExt = os.path.splitext(f"C:/gits/twitch-soundboard/{soundeffect}.m4a")
            if(fileExists == False):
                fileExists = os.path.exists(f"C:/gits/twitch-soundboard/{soundeffect}.mp3")
                fileExt = os.path.splitext(f"C:/gits/twitch-soundboard/{soundeffect}.mp3")
    

    print(fileExt)
    print(f"trying to play {soundeffect}")

    ctx.voice_client.play(discord.FFmpegPCMAudio(f"C:/gits/twitch-soundboard/{soundeffect}{fileExt[1]}"), after=lambda e: print('done', e))


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