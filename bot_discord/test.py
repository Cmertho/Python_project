import discord
import asyncio
import random

client = discord.Client()
text = ['ПУК', 'ЧООО', 'ПАШЕЛ ****', 'ТЫ ЧТО ШАКАЛ?']

@client.event
async def on_ready():
    print('Bot_connecting')

@client.event
async def on_message(message):
    if message.content.startswith('!ping'):
        await asyncio.sleep(1)
        await client.send_message(message.channel, random.choice(text))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

client.run('Youre bot token')
