def GetPersonalityLine(c1, c2, c3, c1def, c2def, c3def, useThreeCharacter):
  text3 = f"and the last character is named {c3} and is {c3def},"

  if not useThreeCharacter:
    text3=""
  return f"one character is named {c1} and is {c1def}, another character is named {c2} and is {c2def}, {text3 }"

def GetSitcomPrompt(personality, length, data):
  return f'write a {data[0]} dialogue for a sitcom between two characters. include at least {length} words. {personality} but their personality is {data[1]} to the script. all characters are either in college or graduated from college. {data[2]} do not include stage directions. put "(laughs)" in a line of dialogue when you want the audience to laugh. put character names before dialogue. include a short 1 to 3 word title at the end formatted "Title: " followed by the one word title.'


def GetDramaPrompt(personality, length, data):
  return f'write an emotional sad dialogue for a drama show between two characters. include at least {length} words. {personality}. {data[0]} do not include stage directions. put character names before dialogue. include a short 1 to 3 word title at the end formatted "Title: " followed by the title.'

def GetMockumentaryPrompt(length,topic="object, place, or person"):
  return f'write a {length} word mockumentary about a fictitious {topic}. write about its history and its upsides and downsides. do not acknowledge this is fictitious. do not write about a real thing. make the fictitious subject funny. do not make paragraphs more than 80 words each. begin the response with the name of the subject matter formatted like this: "Subject: " and then the name of the subject.'

def GetReligionPrompt(length):
  return f'write a new fictitious religious text. make up a god for the text, and make it funny. include at least {length} words. start each chapter with "Chapter: "'