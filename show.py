import requests
import random
from gtts import gTTS
import os
import gc
import nouns
import asyncio
import ffmpy3
import sample
import discord
import render
from pydub import AudioSegment
import prompts
import pathlib
import urllib
import getPOE
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from replit import db
import re
#os.environ["IMAGEIO_FFMPEG_EXE"] = "mpeg/ffmpeg"
from moviepy.editor import *

headers = {"Authorization": "Bearer v1.3f1e7e39e674b52ca48c10014606a115a61bf0500c18d126c58040e12fd30beb"}

archetype = ["funny", "absurd", ""]
fonts = ["comic.ttf", "ARLRDBD.TTF", "georgia.ttf"]
dataIndex = 0
writingFile=False

doingAudioGen = False

total = 0
theme = ""
format = "sitcom"
formatSubtitles = {
  "sitcom": "Society Guy Funny Moment:",
  "drama": "Touching Your Heart:"
}

async def tickUpCounter(client):
  
  count = 0
  if not "SGCount" in list(db.keys()):
    count = 1
  else:
    count = db["SGCount"]+1
  db["SGCount"]=count
  await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="Great Discovery #"+str(count)))

def query(URL, payload):
  response = requests.post(URL, headers=headers, json=payload)
  return response.json()


async def getGPT():
  global theme
  t = random.choice(["place","object","invention","object","invention","discovery"])
  if t == "object":
    t = random.choice(nouns.adjectives) + " " + random.choice(nouns.nouns)
  if t == "place":
    t = random.choice(nouns.adjectives) + " " + random.choice(nouns.locations)
  if t == "invention":
    t = random.choice(nouns.nouns) + " " + random.choice(nouns.nouns)
  if theme != "":
    t = theme
    theme = ""
  prompt = prompts.GetMockumentaryPrompt(400,topic = t)    

  response = ""

  useSample = False

  print(prompt)
  
  if useSample:
    response = sample.example
  else:

    #Below is POE :)
    response = await getPOE.GetPOEResponse(prompt)

  global total
  total += 1
  total = total % 5
  if total == 0:
    #chatbot.clear_conversations()
    pass
  print(response[0:100])
  return response


language = 'en'
scriptLength = 5
imageCount = 8


def createAudio(txt, fileName, api="espeak", voice="f1"):
  global doingAudioGen
  doingAudioGen = True
  myobj = gTTS(text=txt, lang=language, slow=False)
  myobj.save(fileName+".mp3")
  doingAudioGen = False
  return fileName + ".mp3"


def createImage(charName, fileName, text=""):
  img = Image.new("RGB", (800, 400), (0,0,0))
  img2 = Image.open(f"{charName}.png")
  #I1 = ImageDraw.Draw(img)
  size = 275#random.randint(25, 300)
  img2 = img2.resize((size, size))
  try:
    img.paste(img2, (262, 0), img2)
  except:
    img.paste(img2, (262, 0))

  if text != "":
    img = appendText(img, text)

  img.save(fileName + ".png")


def createImageNew(fileName, text=""):
  img = Image.open(f"baseImages/{random.randint(0,imageCount-1)}.png")
  #I1 = ImageDraw.Draw(img)
  img = img.resize((800, 400))
  if text != "":
    img = appendText(img, text)

  img.save(fileName + ".png")


def createOutro():
  img = Image.new("RGB", (800, 400), (0,0,0))

  # Call draw Method to add 2D graphics in an image
  I1 = ImageDraw.Draw(img)
  fnt = ImageFont.truetype("fonts/ARLRDBD.TTF", 80)
  fnt2 = ImageFont.truetype("fonts/ARLRDBD.TTF", 40)
  # Add Text to an image
  msg = "Mockery in Motion"
  lx = I1.textlength(msg, font=fnt)
  lx2 = I1.textlength("Made using ChatGPT and Python", font=fnt2)
  lx3 = I1.textlength("https://discord.gg/U3Muh2Bvqf", font=fnt2)
  lx /= 2
  lx2 /= 2
  lx3 /= 2
  #ly /= 2
  I1.text((img.size[0] / 2 - lx, img.size[1] / 2),
          msg,
          font=fnt,
          fill=(255, 255, 255))
  I1.text((img.size[0] / 2 - lx2, img.size[1] / 2 + 100),
          "Made using ChatGPT and Python",
          font=fnt2,
          fill=(255, 255, 255))
  I1.text((img.size[0] / 2 - lx3, img.size[1] / 2 - 50),
          "https://discord.gg/U3Muh2Bvqf",
          font=fnt2,
          fill=(255, 255, 255))
  img.save("images/outro.png")


def createTitle(text):
  img = Image.new("RGB", (800, 400), (0,0,0))

  # Call draw Method to add 2D graphics in an image
  I1 = ImageDraw.Draw(img)
  fnt = ImageFont.truetype("fonts/ARLRDBD.TTF", 60)
  fnt2 = ImageFont.truetype("fonts/ARLRDBD.TTF", 40)
  # Add Text to an image
  msg = text
  lx = I1.textlength(msg, font=fnt)
  lx2 = I1.textlength("New Discovery:", font=fnt2)
  lx /= 2
  lx2 /= 2
  #ly /= 2
  #I1.text((img.size[0] / 2 - lx, img.size[1] / 2),
  #        msg,
  #        font=fnt,
  #        fill=(255, 255, 255))
  offset = 0
  for line in wrap_text(msg, 750, fnt):
    lx = I1.textlength(line, font=fnt)
    lx /= 2
    I1.text((img.size[0] / 2 - lx, img.size[1] / 2 + offset),
            line,
            font=fnt,
            fill=(255, 255, 255))
    offset += 65
  I1.text((img.size[0] / 2 - lx2, img.size[1] / 2 - 100),
          "New Discovery:",
          font=fnt2,
          fill=(255, 255, 255))
  img.save("images/title.png")


def slicer(my_str, sub):
  index = my_str.find(sub)
  if index != -1:
    return my_str[(index + 1):]
  else:
    return my_str


def getInParentheses(tex):
  if "(" in tex and ")" in tex:
    return tex[tex.find("(") + 1:tex.find(")")]
  return tex


def cleanParentheses(tex):
  return re.sub("[\(\[].*?[\)\]]", "", tex)


def wrap_text(text, width, font):
  text_lines = []
  text_line = []
  text = text.replace('\n', ' [br] ')
  words = text.split()
  font_size = font.getsize(text)

  for word in words:
    if word == '[br]':
      text_lines.append(' '.join(text_line))
      text_line = []
      continue
    text_line.append(word)
    w, h = font.getsize(' '.join(text_line))
    if w > width:
      text_line.pop()
      text_lines.append(' '.join(text_line))
      text_line = [word]

  if len(text_line) > 0:
    text_lines.append(' '.join(text_line))
  return text_lines


def appendText(img, text):
  I1 = ImageDraw.Draw(img)

  fnt = ImageFont.truetype("fonts/ARLRDBD.TTF", 20)
  # Add Text to an image
  msg = text
  offset = 0
  for line in wrap_text(msg, 750, fnt):
    lx = I1.textlength(line, font=fnt)
    lx /= 2
    I1.text((img.size[0] / 2 - lx, img.size[1] / 2 + 75 + offset),
            line,
            font=fnt,
            fill=(255, 255, 255))
    offset += 25

  return img


recentMsg = None


async def Write(channel):
  
  message = await channel.send("Beginning film generation (API request)")
  global recentMsg, dataIndex
  dataIndex = random.randint(0, len(fonts) - 1)
  recentMsg = message

  result = ""

  
  print("Getting GPT Response")
  totalText = await getGPT()
  print("Parsing GPT Response")
  await message.edit(content="Parsing returned script (TTS and image generation)")

  if totalText == "":
    await message.delete()
    return "None"

  charToAddTo = 0

  allLines = totalText.split("\n")
  allLines[:] = [item for item in allLines if item != '' and item != '\n']
  subData = {}

  z = 0
  #Handles laugh track
  for item in allLines:
    v = item
    item = cleanParentheses(v)
    allLines[z] = item
    subData[item] = getInParentheses(v)
    z += 1

  allLines[:] = [item for item in allLines if item != '' and item != '\n']

  

  summary = slicer(allLines[0], ":")
  summary = summary.replace("-", "").replace("_", "").replace("*", "").replace(
    '"', "").replace("[", "").replace("]", "").replace("(",
                                                       "").replace(')', "")
  summary = summary.replace(".", "").replace('"', "")
  summary = summary.title()

  await message.edit(content="AI-Generating 2D images")
  try:
    await MakeImages(summary)  #Makes the AI generated image for the result
  except:
    pass

  allLines.pop(0)
  
  fileNames = []
  z = 0
  #createImages(useThreeCharacter,f"characterImages/{cName1}.png",f"characterImages/{cName2}.png",f"characterImages/{cName3}.png")
  imgIndex = 0
  await message.edit(content="Adding subtitles")
  for item in allLines:
    tex = item.replace("-", "").replace("_", "").replace(
      "*", "").replace('"', "") + "\n" #slicer(item, ":")
    result += tex

    sub = ""
    if item in list(subData.keys()):
      sub = subData[item]

    
    if (tex != "" and tex != "\n"):
      fileNames.append(str(z))
      createImage("Generated"+str(imgIndex), "images/" + str(z), text=tex.rstrip('\n'))
      createAudio(tex,"audio/" + str(z))
      #createImageNew("images/" + str(z), text=n+": "+tex.rstrip('\n'))
      charToAddTo = (charToAddTo + 1) % 2
    z += 1
    imgIndex = (imgIndex+1)%4

  createTitle(summary.replace(".", ""))
  createOutro()
  clips = []
  clipsA = []

  await message.edit(content="Creating Audio")

  clips.append(ImageClip("images/title.png").set_duration(4))
  clipsA.append(AudioClip(make_frame=lambda t: 0, duration=4))

  for file in fileNames:
    audio = MP3("audio/" + file + ".mp3")  #MP3("audio/" + file + ".mp3")
    clips.append(
      ImageClip("images/" + file +
                ".png").set_duration(float(audio.info.length) + 1))
    clipsA.append(AudioFileClip("audio/" + file + ".mp3"))
    clipsA.append(AudioClip(make_frame=lambda t: 0, duration=1))

  clips.append(ImageClip("images/outro.png").set_duration(4))
  clipsA.append(AudioClip(make_frame=lambda t: 0, duration=4))

  final_clip = concatenate_audioclips(clipsA)

  gc.collect()

  global writingFile

  if writingFile:
    asyncio.sleep(2)
                  
  writingFile = True
                  
  print("Making clip")
  await message.edit(content="Mixing video")
  concat_clip = concatenate_videoclips(clips, method="compose")
  new_audioclip = CompositeAudioClip([final_clip])
  concat_clip.audio = new_audioclip

  print("Saving clip")

  concat_clip.write_videofile("final.mp4", fps=4)
  while (os.path.getsize('final.mp4') / (1024*1024.0)) > 7:
    await message.edit(content="Downsizing video file to fit 8MB maximum")
    clip = VideoFileClip("final.mp4")
    clip_resized = clip.resize((clip.size[0]*0.75,clip.size[1]*0.75))
    clip_resized.write_videofile("final.mp4")
    
  if (len(result) > 2000):
    result = result[0:1900] + " \n\n(The rest was truncated due to size)"
  await message.delete()
  return totalText


async def MakeImages(prompt):
  url = "https://api.neural.love/v1/ai-art/generate"
  payload = {
    "amount": 4,
    "isPublic": True,
    "isPriority": False,
    "isHd": False,
    "steps": 25,
    "cfgScale": 7.5,
    "prompt": "" + prompt,
    "style": "debug",
    "layout": "square",
    "negativePrompt": "woman, people"
  }
  headers = {
    "accept":
    "application/json",
    "content-type":
    "application/json",
    "authorization":
    "Bearer v1.90b4f1889fc4c9c24488068c902e919d11110ee515bcf03d5afbe0865ddc0694"
  }
  response = requests.post(url, json=payload, headers=headers)
  data = response.json()
  orderId = data["orderId"]
  #print(orderId)
  url2 = "https://api.neural.love/v1/ai-art/orders/" + orderId
  #print(url2)
  headers2 = {
    "accept":
    "application/json",
    "authorization":
    "Bearer v1.90b4f1889fc4c9c24488068c902e919d11110ee515bcf03d5afbe0865ddc0694"
  }
  count = 0
  while True:
    await asyncio.sleep(3)

    response2 = requests.get(url2, headers=headers2)

    count += 1

    data2 = response2.json()
    if data2["status"]["isReady"]:
      
      for i in range(4):
        pth = f"Generated{i}.png"
        my_file = pathlib.Path(pth)
        if my_file.is_file():
          os.remove(pth)
        urllib.request.urlretrieve(data2["output"][i]["full"],
                                   pth)
      break
    elif data2["status"]["code"] == 998:
      break
    elif count > 10:
      break
    else:
      await asyncio.sleep(4)