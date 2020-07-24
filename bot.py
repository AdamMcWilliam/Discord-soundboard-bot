# bot.py
import os
import random
import urllib.request, json
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = "!")

def playFromQueue(ctx, filePath):

    with open('queue.txt', 'r') as fin:
        first_sound = fin.readline()
        data = fin.read().splitlines(True)
        
    with open('queue.txt', 'w') as fout:
        fout.writelines(data[1:])

    print(first_sound)

    ctx.voice_client.play(discord.FFmpegPCMAudio(f"{filePath}"), after=lambda e: print('done', e))
    


def addToQueue(sound):     

        queueFileWrite = open("queue.txt", "a")
        queueFileWrite.write(sound)
        queueFileWrite.write("\n")
        queueFileWrite.close()


def getPokemon():
    pokemonNames = ['Bulbasaur','Ivysaur','Venusaur','Charmander',
    'Charmeleon','Charizard','Squirtle','Wartortle','Blastoise',
    'Caterpie','Metapod','Butterfree','Weedle','Kakuna','Beedrill',
    'Pidgey','Pidgeotto','Pidgeot','Rattata','Raticate','Spearow','Fearow',
    'Ekans','Arbok','Pikachu','Raichu','Sandshrew','Sandslash','Nidoran-F',
    'Nidorina','Nidoqueen','Nidoran-M','Nidorino','Nidoking','Clefairy','Clefable',
    'Vulpix','Ninetales','Jigglypuff','Wigglytuff','Zubat','Golbat','Oddish','Gloom',
    'Vileplume','Paras','Parasect','Venonat','Venomoth','Diglett','Dugtrio','Meowth',
    'Persian','Psyduck','Golduck','Mankey','Primeape','Growlithe','Arcanine','Poliwag',
    'Poliwhirl','Poliwrath','Abra','Kadabra','Alakazam','Machop','Machoke','Machamp','Bellsprout',
    'Weepinbell','Victreebel','Tentacool','Tentacruel','Geodude','Graveler','Golem','Ponyta','Rapidash',
    'Slowpoke','Slowbro','Magnemite','Magneton','Farfetchd',
    'Doduo','Dodrio','Seel','Dewgong','Grimer','Muk','Shellder',
    'Cloyster','Gastly','Haunter','Gengar','Onix','Drowzee','Hypno',
    'Krabby','Kingler','Voltorb','Electrode','Exeggcute','Exeggutor','Cubone',
    'Marowak','Hitmonlee','Hitmonchan','Lickitung','Koffing','Weezing','Rhyhorn','Rhydon','Chansey','Tangela'
    ,'Kangaskhan','Horsea','Seadra','Goldeen','Seaking','Staryu','Starmie','Mr. Mime','Scyther','Jynx','Electabuzz'
    ,'Magmar','Pinsir','Tauros','Magikarp','Gyarados','Lapras','Ditto','Eevee','Vaporeon','Jolteon','Flareon','Porygon'
    ,'Omanyte','Omastar','Kabuto','Kabutops','Aerodactyl','Snorlax','Articuno','Zapdos','Moltres','Dratini','Dragonair'
    ,'Dragonite','Mewtwo','Mew']

    return pokemonNames


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
        
        for value in data:
            try:
                if(data[f"{value}"]['name'] == sound):
                    permittedUsers = data[f"{value}"]['permitted_users']
                    for j in permittedUsers:
                        if(j == user):
                            print('Sound owned.')
                            return True
            except KeyError:
                continue
        
        print('sound not owned.')
        return False

#Is sound accepted by community
def getSoundPopularity(sound):

    with open('json/sfx_votes.json') as json_file:
        data = json.load(json_file)
        data = data['sfx_votes']

        for value in data:
            try:
                if(data[f"{value}"]['command'] == sound):
                    supporters = data[f"{value}"]['supporters']
                    detractors = data[f"{value}"]['detractors']
            except KeyError:
                continue
                
    #count and compare
    supportersLength = len(supporters)
    detractorsLength = len(detractors)

    if supportersLength >= detractorsLength:
        return True
    else:
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


#test playing from queue
@bot.command(name="playtest", description = "just testing", pass_context=True)
async def playtest(ctx):
    playFromQueue(ctx, filePath)


#pokemonGuessing Game
@bot.command(name="pokemon", description = "Starts pokemon game", pass_context=True)
async def pokemonStart(ctx):

    pokemonNames = getPokemon()

    #check if pokemon already been chosen
    pokemonFile = open("pokemon.txt", 'r+')
    contents  = pokemonFile.read()
    print(f"contents of file {contents}")
    if not contents:
        start = True
        randomPokemon = random.choice(pokemonNames)
    else:
        start = False
        randomPokemon = contents

    print(randomPokemon)

    #write random pokemon to file
    pokemonFile = open("pokemon.txt", 'w+')
    pokemonFile.write(randomPokemon)

    soundsFilePath = "C:/gits/twitch-soundboard/"

    ext = getRealSound(soundsFilePath, randomPokemon)

    if(start):
        ctx.voice_client.play(discord.FFmpegPCMAudio(f"C:/gits/twitch-soundboard/pokewho.m4a"), after=lambda e: ctx.voice_client.play(discord.FFmpegPCMAudio(f"{soundsFilePath}{randomPokemon}.{ext}"), after=lambda e: print('done', e)))
    else:
        ctx.voice_client.play(discord.FFmpegPCMAudio(f"{soundsFilePath}{randomPokemon}.{ext}"), after=lambda e: print('done', e))


#guess a pokemon
@bot.command(name="guess", description = "make a guess of the pokemon", pass_context=True)
async def pokemonGuess(ctx):
    
    username = ctx.author.display_name.lower()
    pokemonNames = getPokemon()

    #get guess from user
    guess = ctx.message.content.split('!guess ')
    guess = guess[1].title()

    #get current pokemon
    pokemonFile = open("pokemon.txt", 'r+')
    contents  = pokemonFile.read()

    if not contents:
        #if no pokemon start game
        await pokemonStart(ctx)
    else:
        #compare guess
        if guess == contents:
            #user wins
            #report win
            await ctx.channel.send(f"@{username} You won!: {guess} was the correct answer.")
            ctx.voice_client.play(discord.FFmpegPCMAudio(f"C:/gits/twitch-soundboard/pokewin.opus"), after=lambda e: print('done', e))

            #clear file
            pokemonFile = open("pokemon.txt", 'w+')
            pokemonFile.write("")

        else:
            #user loses

            #check if real pokemon
            if guess not in pokemonNames:
                await ctx.channel.send(f"@{username} {guess} is not a valid pokemon.")
                
            #report wrong
            else:
                await ctx.channel.send(f"@{username} your guess of {guess} is wrong.")


#bot joins the server
@bot.command(name="join", description="join a voice channel", pass_context=True,)
async def joinServer(ctx):
    voicechannel = ctx.author.voice.channel
    await voicechannel.connect()

#plays a sound !play snorlax
@bot.command(name="play", description="play a sound", pass_context=True,)
async def playSound(ctx):
    
    soundeffect = ctx.message.content.split('!play ')
    soundeffect = soundeffect[1]
    username = ctx.author.display_name.lower()

    canPlay = getSound(soundeffect,username)
    hasMana = getMana(username)
    isPopular = getSoundPopularity(soundeffect)

    if canPlay:
        if hasMana:
            if isPopular:
                
                soundsFilePath = "C:/gits/twitch-soundboard/"
                ext = getRealSound(soundsFilePath, soundeffect)
                print(f"trying to play {soundeffect}")
                #ctx.voice_client.play(discord.FFmpegPCMAudio(f"{soundsFilePath}{soundeffect}.{ext}"), after=lambda e: print('done', e))
                filePath = f"{soundsFilePath}{soundeffect}.{ext}"
                useMana(username)
                addToQueue(soundeffect)
                playFromQueue(ctx, filePath)
            else:
                await ctx.channel.send(f"@{username} The people have spoken and everyone hates this sound, im not playing it.")
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
    await ctx.channel.send(url)

@bot.command(name="perms", description="get owners of a sound", pass_context=True)
async def permissions(ctx):
    
    username = ctx.author.display_name.lower()

    soundeffect = ctx.message.content.split('!perms ')
    try:
        soundeffect = soundeffect[1]
    except IndexError:
        soundeffect = ""
        pass
    
    with open('json/commands.json') as json_file:
            data = json.load(json_file)
            data = data['commands']

    #if there is a soundeffect
    if soundeffect:
        for value in data:
            try:
                if(data[f"{value}"]['name'] == soundeffect):
                    permittedUsers = data[f"{value}"]['permitted_users']
            except KeyError:
                continue

        await ctx.channel.send(f"Users that own sound: {soundeffect}: {permittedUsers}")
    
    #if just !perms they want the sound they own
    else:
        ownedSounds = []

        for value in data:
            try:
                if username in data[f"{value}"]['permitted_users']:
                    #add to array
                    ownedSounds.append(data[f"{value}"]['name'])
            except KeyError:
                continue

        await ctx.channel.send(f"@{username}: Your owned sounds: {ownedSounds}")





#run
bot.run(TOKEN)



