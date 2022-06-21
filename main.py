from telebot import telebot, TeleBot, custom_filters
import os
import folder.memory as memory
import vk_api
from time import sleep
import asyncio
from folder.bomber import mainBomber
import folder.language as language
from folder.config import TELEBOTTOKEN, VKTOKEN

bot = TeleBot(TELEBOTTOKEN)
vkapistop = False

async def VKAPI(message):
    global vkapistop
    try:
        #vk token
        vk_auth = vk_api.VkApi(token=VKTOKEN)
        vk = vk_auth.get_api()
        bot.send_message(message.chat.id, text=language.AUTHORIZATION_SUCCESSFULLY)
    except:
        bot.send_message(message.chat.id, text=language.AUTHORIZATION_FAILED)

    num = 1000
    while True:
        if vkapistop == True:
            vk.status.set(text=f'https://oukilove.github.io/')
            bot.send_message(message.chat.id, text=language.STATUS_DEAD)
            vkapistop = False
            break
        if num <= 0:
            num = 1000
        vk.status.set(text=f"{num} - 7")
        num-=7
        sleep(60)
    return

@bot.message_handler(chat_id=[955953291], commands=['start'])
def start(message):
    bot.send_message(chat_id=message.chat.id, text='Hello!')

@bot.message_handler(chat_id=[955953291], commands=['help'])
def help(message):
    bot.send_message(chat_id=message.chat.id, text=language.COMMAND)
    bot.send_message(chat_id=message.chat.id, text=language.HELP_START)
    bot.send_message(chat_id=message.chat.id, text=language.HELP_HELP)
    bot.send_message(chat_id=message.chat.id, text=language.HELP_LANGUAGE)
    bot.send_message(chat_id=message.chat.id, text=language.HELP_VKAPISTART)
    bot.send_message(chat_id=message.chat.id, text=language.HELP_VKAPISTOP)
    bot.send_message(chat_id=message.chat.id, text=language.HELP_LOADING)
    bot.send_message(chat_id=message.chat.id, text=language.HELP_BOMBER)
    bot.send_message(chat_id=message.chat.id, text=language.HELP_BOTSTOP)

@bot.message_handler(chat_id=[955953291], content_types=['text'])
def main(message):
    if message.text == 'lRU':
        try:
            language.language = 'RU'
            bot.send_message(chat_id=message.chat.id, text='Язык изменен на RU')
        except:
            bot.send_message(chat_id=message.chat.id, text='Language not changed')
    
    if message.text == 'lEN':
        try:
            language.language = 'EN'
            bot.send_message(chat_id=message.chat.id, text='Language changed to EN')
        except:
            bot.send_message(chat_id=message.chat.id, text='Language not changed')

    global vkapistop
    if message.text == 'Vkapistart':
        bot.send_message(chat_id=message.chat.id, text=language.VKAPI_START)
        try:
            asyncio.new_event_loop().run_until_complete(VKAPI(message))
        except:
            bot.send_message(chat_id=message.chat.id, text=language.ERROR)

    if message.text == 'Vkapistop':
        try:
            bot.send_message(chat_id=message.chat.id, text=language.VKAPI_STOP)
            vkapistop = True
            bot.send_message(chat_id=message.chat.id, text=language.VKAPI_WAIT)
        except:
            bot.send_message(chat_id=message.chat.id, text=language.ERROR)

    if message.text == 'Loading':
        try:
            proc_used = memory.cpu()
            bot.send_message(message.chat.id, text=language.LOADING_PROCESSOR + str(proc_used) + '%')
            mem_used = memory.mem()
            bot.send_message(message.chat.id, text=language.LOADING_RAM + str(mem_used))
            diskused = memory.disk()
            bot.send_message(message.chat.id, text=language.LOADING_USED + str(diskused) + language.LOADING_DISK)
        except:
            bot.send_message(message.chat.id, text=language.ERROR)

    if message.text == 'Bomber':
        bot.send_message(message.chat.id, text=language.BOMBER_START)
        try:
            bot.register_next_step_handler(message, mainBomber)
        except:
            bot.send_message(message.chat.id, text=language.ERROR)
    
    if message.text == 'Botstop':
        bot.send_message(chat_id=message.chat.id, text=language.BOT_STOP)
        try:
            bot.stop_polling()
        except:
            bot.send_message(chat_id=message.chat.id, text=language.ERROR)


bot.add_custom_filter(custom_filters.ChatFilter())
bot.polling(non_stop=True)