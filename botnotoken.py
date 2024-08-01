import discord
from discord.ext import commands
import json   # json
import re     # regex
import time   # sleep
import typing
from urllib.request import Request, urlopen # HTML request
from http.cookiejar import CookieJar

#####
# Setup URL opener
import urllib.request

class SafeOpener(urllib.request.OpenerDirector):
  def __init__(self, handlers: typing.Iterable = None):
    super().__init__()
    handlers = handlers or (
      urllib.request.UnknownHandler,
      urllib.request.HTTPDefaultErrorHandler,
      urllib.request.HTTPRedirectHandler,
      urllib.request.HTTPSHandler,
      urllib.request.HTTPErrorProcessor,
      urllib.request.HTTPHandler,
      urllib.request.HTTPCookieProcessor,
    )

    for handler_class in handlers:
      self.add_handler(handler_class())

# KoV's guild swgoh ID
guildId = "nzYxnRYNRYCT8wRhEJcWpw"

request_urls = []
opener = SafeOpener()
urllib.request.install_opener(opener)

#403 fix
#https://stackoverflow.com/questions/13303449/urllib2-httperror-http-error-403-forbidden
httpOptions = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
#      'Connection': 'keep-alive',
      'method': 'get',
      'muteHttpExceptions': False,
  }

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()

@bot.tree.command(name="hello",description="Surely")
async def slash_command(interaction:discord.Interaction):
    await interaction.response.send_message("Hello There!")

@bot.tree.command(name="guildid",description="Gets basic guild info")
async def guild_slash_command(interaction:discord.Interaction):
        # Request general guild info
    site = "https://swgoh.gg/api/guild-profile/" + str(guildId)
    req = Request(url=site,headers=httpOptions)
    text = opener.open(req).read()
    basicGuildInfo = json.loads(text)
      #Extract Guild Name and Print
    await interaction.response.send_message(f"Guild name is " + basicGuildInfo["data"]["name"])

@bot.tree.command(name="has_slkr",description="test")
async def Username_return(interaction:discord.Interaction, allycode: int):
   site = "https://swgoh.gg/api/player/" + str(allycode)
   req = Request(url=site,headers=httpOptions)
   text = opener.open(req).read()
   


#Calculate percent armor boost from DCs and Abilites, print result as final Armor percentage
@bot.tree.command(name="armor_boost", description="Calculate Final Armor Value after DCs and Abilities")
async def defense_boost(interaction: discord.Interaction, base_armor: int, character_level: int, percent_defense_boost: int, percent_defense_boost2: typing.Optional[int] = 0, percent_defense_boost3: typing.Optional[int] = 0, percent_defense_boost4: typing.Optional[int] = 0):
    initial_defense = (base_armor * (character_level * 7.5)) / (100 - base_armor)
    new_defense = initial_defense + (initial_defense * (percent_defense_boost / 100)) + (initial_defense * (percent_defense_boost2 / 100)) + (initial_defense * (percent_defense_boost3 / 100)) + (initial_defense * (percent_defense_boost4 / 100))
    final_armor = (new_defense * 100) / (new_defense + (character_level * 7.5))
    await interaction.response.send_message(f"Final Armor Stat: {final_armor:,.2f}" + "%")

#Calcluate final offense in conquest after Zealous Ambition Boosts
@bot.tree.command(name="za_boost", description="Calculate final offense after ZA boosts")
async def za_command(interaction: discord.Interaction, 
                     base_offense: float, 
                     base_health: float, 
                     percent_za_boost: float, 
                     percent_za_boost2: typing.Optional[float] = 0.0, 
                     percent_za_boost3: typing.Optional[float] = 0.0, 
                     percent_za_boost4: typing.Optional[float] = 0.0, 
                     percent_za_boost5: typing.Optional[float] = 0.0, 
                     percent_za_boost6: typing.Optional[float] = 0.0):
    za_offense_boost = (base_offense + (base_health * (percent_za_boost / 100)) + (base_health * (percent_za_boost2 / 100)) + (base_health * (percent_za_boost3 / 100)) + (base_health * (percent_za_boost4 / 100)) + (base_health * (percent_za_boost5 / 100) + (base_health * (percent_za_boost6 / 100))))
    new_offense = base_offense + za_offense_boost
    await interaction.response.send_message(f"Final Offense after ZA Applied = {new_offense:,.0f}")

##Calclulates starting speed of Phasma with TW Omi Active, 5 F.O. Allies
@bot.tree.command(name="phasma_omi_speed", description="Calculate Starting Speed of Phasma Omi")
async def phasma_speed(interaction: discord.Interaction, phasma_base_speed: int):
   phasma_new_speed = ((phasma_base_speed + 100)/0.625)
   await interaction.response.send_message(f"Starting speed of Phasma with Omi Active is {phasma_new_speed:.1f}")

##Calculates effective HP based on Defense, and optionally compares a change in armor
@bot.tree.command(name="effective_hp_calculator", description="Calculate Effective HP based on Armor")
async def ehp_calc(interaction: discord.Interaction, base_hp: int, base_armor: int, new_armor: typing.Optional[int] = 0):
  effective_hp = (base_hp / (1 - (base_armor/100)))
  if new_armor == 0:
    await interaction.response.send_message(f"Effective HP is {effective_hp:,.0f}")
  if new_armor > 0:
     new_effective_hp = base_hp / (1-(new_armor/100))
     change_in_hp = new_effective_hp - effective_hp
     await interaction.response.send_message(f"New Effective HP is {new_effective_hp:,.0f}. This is an increase of {change_in_hp:,.0f}.")



execfile("discord_token.py")