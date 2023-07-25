import os
import discord
from discord import app_commands

from io import BytesIO
from PIL import Image
import requests

from discord.ext import tasks
import asyncio
from keep_alive import keep_alive

import show


intents = discord.Intents.default()
intents.typing = False
intents.presences = True
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name = "makediscovery", description = "You have just discovered something new, and it is (format it 'a [type of thing] called [name]:'):", guild=discord.Object(id=1081397933276155977))
async def queuetheme(interaction, newtheme: str):
  show.theme = newtheme
  embedVar = discord.Embed(title=f'"{newtheme}" set as next discovery!', description="Subjects against OpenAI policy will not be generated, apologies.", color=0xffff00)
  await interaction.response.send_message(embed=embedVar)

success=True

@tasks.loop(minutes=3)
async def test():
  #await channel.send("test " + str(random.randint(0, 100)))
  #await RunRobeGet()
  global success
  channel = client.get_channel(1083846877163835412)
  try:
    write = await show.Write(channel)
    await show.tickUpCounter(client)
  #await channel.send(write)
    if (write != "None"):
      channel = client.get_channel(1083846877163835412)
      await channel.send("Breaking New Discovery:",file=discord.File(r'final.mp4'))
      success=True
  except Exception as e:
    channel = client.get_channel(1083846877163835412)
    print(e)
    if success:
      success=False
      await channel.send("There was an error generating...")
  show.writingFile=False


@client.event
async def on_ready():
  print("I'm in")
  print(client.user)
  #await tree.sync(guild=discord.Object(id=1052421062371061810))
  await tree.sync(guild=discord.Object(id=1081397933276155977))
  #r = brain.ask("Are you?")
  #await channel.send(str(r))
  #await channel.send(await sitcom.testFlan())
  channel = client.get_channel(1083846877163835412)
  write=""
  write = await show.Write(channel)
  await show.tickUpCounter(client)

  show.writingFile=False
  
  #await channel.send(write)
  if (write != "None"):
    channel = client.get_channel(1083846877163835412)
    await channel.send("Breaking New Discovery:",file=discord.File(r'final.mp4'))
  test.start()
  

@client.event
async def on_message(message):
  if message.author != client.user:
    #await message.channel.send("Sussy!")
    pass    
        
keep_alive()
my_secret = os.environ['DISCORD_BOT_SECRET']
client.run(my_secret)

