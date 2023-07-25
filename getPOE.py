from POE import load_chat_id_map, clear_context, send_message, get_latest_message,get_latest_message_async, set_auth
import os
#Auth
async def GetPOEResponse(prompt,bot = "capybara"):
  set_auth('Quora-Formkey',os.environ['form'])
  set_auth('Cookie',os.environ['cookie'])
  
  chat_id = load_chat_id_map(bot)
  clear_context(chat_id)
  send_message(prompt,bot,chat_id)
  reply = await get_latest_message_async(bot)
  return reply