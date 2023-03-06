#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:03:11 2023

@author: andrethieme
"""

#Versão atual com solicitação de episódio, a partir da proposta da Mah

import feedparser
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "token_@BotFather"
timers = {}
muralddg = 'codigo_numerico'
id_bot = 'codigo_numerico'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text= r'Oi! eu sou o dragão fofoqueiro da Garagem, você pode me contar qualquer coisa que eu vou encaminhar pro resto da garagem rapidinho!\n\nMas, antes de começar, vou te contar uma fofoca: Aprendi uma coisa nova enquanto estive fora, agora você pode me pedir qual o último episódio do DDG com o comando /episodio ou o endereço do feed com /feed')
                                   
                                   
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):                                   
    await context.bot.send_message(chat_id=update.effective_chat.id, text="""É simples demais: é só mandar uma mensagem!
Sua mensagem vai ser encaminhada pro Mural da Garagem e vamos responder nos nossos recadinhos. 
(Ou podemos manter só entre nós, se preferir. Só nos avisar)

Agora, tenho duas novidades:
Se quiser ver qual foi o último episódio lançado me manda um /episodio
Se quiser assinar o nosso feed, /feed
""")

async def feed(update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text= r'Você pode assinar esse feed no seu tocador de podcasts: https://dragoesdegaragem.com/podcast/dragoes-de-garagem/feed/')
    
async def episodio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    d = feedparser.parse('https://dragoesdegaragem.com/feed/podcast/')
    await context.bot.send_message(chat_id=update.effective_chat.id, text= f'{d.entries[0].link}\n{d.entries[0].description}')

async def forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) not in [muralddg]:
        await context.bot.forward_message(chat_id=muralddg, from_chat_id=update.effective_chat.id, message_id=update.effective_message.id)
        chat_id = update.effective_message.chat_id
        due = 15
        if remove_job_if_exists(str(chat_id), context):
            due = 5
        context.job_queue.run_once(mensagem, due, chat_id=chat_id, name=str(chat_id), data=due)
            
    elif update.effective_message.reply_to_message and str(update.effective_message.reply_to_message.from_user.username) in ['mecenasbot', 'dragoes_bot']: 
#se for no mural, e for reply pro bot, encaminha pra pessoa
        await context.bot.forward_message(chat_id=update.effective_message.reply_to_message.forward_from.id,
                    from_chat_id=muralddg,
                    message_id=update.effective_message.id)

def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

async def mensagem(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.send_message(job.chat_id, text= "Obrigado! Acabei de encaminhar 🐲")
  
    
if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    feed_handler = CommandHandler('feed', feed)
    help_handler = CommandHandler('help', help)
    episodio_handler = CommandHandler('episodio', episodio)
    forward_handler = MessageHandler(filters.ALL & (~filters.COMMAND), forward)
    application.add_handler(start_handler)
    application.add_handler(feed_handler)
    application.add_handler(help_handler)
    application.add_handler(forward_handler)
    application.add_handler(episodio_handler)
    
    application.run_polling()
